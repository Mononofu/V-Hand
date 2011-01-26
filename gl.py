#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pygame + PyOpenGL version of Nehe's OpenGL lesson04
# Paul Furber 2001 - m@verick.co.za

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import time
import sys
import re
import math
from scipy.integrate import trapz
import numpy as np

class Rotations(object):
    def __init__(self):
        self.base_rot = np.array([0, 0, 0])
        self.last_rots = []
        self.rot_cache = []

    def reset(self, x = 0, y = 0, z = 0):
        self.base_rot = np.array([x*3333, y*3333, z*3333])
        self.last_rots = []
        self.rot_cache = []
        
    def integrate(self):
        if len( self.last_rots) > 2:
            x_rots = []
            y_rots = []
            z_rots = []
            time = []
            for xyz in self.last_rots:
                x_rots.append(xyz[0])
                y_rots.append(xyz[1])
                z_rots.append(xyz[2])
                time.append(xyz[3])

            x_rot = trapz(x_rots, x = time)
            y_rot = trapz(y_rots, x = time)
            z_rot = trapz(z_rots, x = time)

            self.rot_cache = self.base_rot + np.array([x_rot, y_rot, z_rot])

            return np.array([x_rot, y_rot, z_rot])
        else:
            self.rot_cache = self.base_rot

            return np.array([0,0,0])
    
    def add(self, x_rot, y_rot, z_rot, timestamp):
        if len(self.last_rots) > 200:
            self.base_rot += self.integrate()
            self.last_rots = []
        self.last_rots.append([x_rot, y_rot, z_rot, timestamp])
        self.rot_cache = []

    def get(self):
        if len( self.rot_cache ) == 0:
            self.integrate()
        return self.rot_cache / 3333
            

class PseudoSerial:
    def readline(self):
        return "0 0 0 0 0 0"
    def close(self):
        pass
   
port = "/dev/ttyUSB0"
oneG = 70.0
ser = PseudoSerial()
try:
    ser = serial.Serial(port, 115200, timeout=1)
except serial.SerialException as ex:
    print ex
    
rtri = rquad = 0.0

class Display(object):
    def __init__(self):
        self.rot = Rotations()
        self.last_rot_reset = pygame.time.get_ticks()

        self.sum = 0
        self.count = 0
    
    def resize(self, (width, height)):
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def init(self):
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        rtri = 0.0
        rquad = 0.0

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glLoadIdentity()
        glTranslatef(0, 0, -6.0)

        glRotatef(self.rot.get()[0], 0.0, 0.0, 1.0)
        glRotatef(self.rot.get()[1], 1.0, 0.0, 1.0)
        glRotatef(self.rot.get()[2], 0.0, 1.0, 0.0)
        glRotatef(0, 0.0, 0.0, 1.0)

        glColor3f(0.5, 0.5, 1.0)
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glColor3f(1.0, 0.5, 0.5)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glEnd()

    def step(self):
        line = ser.readline()
        res = re.findall("(\d+)+", line)

        if len(res) > 7:
            x_acc = float(res[5]) - 2615
            y_acc = float(res[7]) - 2669
            z_acc = float(res[6]) - 2614
            
            """self.sum += z_acc
            self.count += 1

            if self.count > 1000:
                print self.sum / 1001
                sys.exit()"""
            print "gravity: %f : %f : %f" % (x_acc, y_acc, z_acc)

            x_rot = (int(res[4]) - 2048)
            y_rot = (int(res[3]) - 2030)
            z_rot = (int(res[2]) - 2048)

            if abs(x_rot) < 10:
                x_rot = 0
            if abs(y_rot) < 10:
                y_rot = 0
            if abs(z_rot) < 10:
                z_rot = 0

            print "rotation: %f : %f : %f" % (x_rot, y_rot, z_rot)

            self.rot.add( x_rot, y_rot, z_rot, pygame.time.get_ticks() )

            if self.last_rot_reset < (pygame.time.get_ticks() - 1000):
                if abs(x_rot) < 10 and abs(y_rot) < 10 and abs(z_rot) < 10:
                    xrot = yrot = zrot = 0
                    tresh = 0.1
                    if abs(y_acc) + abs(z_acc) > tresh:
                        xrot = -1 * math.atan2(y_acc, z_acc) / math.pi * 180
                    if abs(x_acc) + abs(z_acc) > tresh:
                        yrot = math.atan2(x_acc, z_acc) / math.pi * 180
                    if abs(x_acc) + abs(y_acc) > tresh:
                        zrot = math.atan2(y_acc, x_acc) / math.pi * 180
                    self.rot.reset(xrot, yrot, zrot)
                    self.last_rot_reset = pygame.time.get_ticks()
                
            print self.rot.get()
        else:
            sys.exit()

        self.draw()

    def run(self):

        video_flags = OPENGL|DOUBLEBUF

        pygame.init()
        pygame.display.set_mode((640,480), video_flags)

        self.resize((640,480))
        self.init()

        frames = 0
        self.ticks = pygame.time.get_ticks()
        while 1:
            event = pygame.event.poll()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                break
            elif event.type == KEYDOWN and event.key == K_r:
                self.rot.reset()

            self.step()
            pygame.display.flip()
            frames = frames+1

        ser.close() 
        print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-self.ticks))


def main():
    disp = Display()
    disp.run()
    
if __name__ == '__main__': main()

