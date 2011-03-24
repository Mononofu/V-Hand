#!/bin/python

import serial
import time
import sys
from optparse import OptionParser

class PseudoSerial:
    def readline(self):
        return "0 0 0 0 0 0"
    def close(self):
        pass
    
class App(object):
    def __init__(self):
        self.parser = OptionParser(version="%prog 0.1")

    def parse_commandline(self):

        self.parser.add_option("-p",
                               "--port",
                               dest="port",
                               default="/dev/ttyUSB0",
                               help="Port to lisen on" )


        (self.options, self.args) = self.parser.parse_args()

    def test_countdown(self, runtime):
        for i in range(runtime, 0, -1):
            sys.stdout.write( "\r%d" % i )
            sys.stdout.flush()
            time.sleep(1.0)
        print "\r "


    def measure_value(self, runtime, pin):
        counter = 0
        sum = 0

        
        l = self.ser.readline()
        begin = time.time()
        
        while time.time() < begin + runtime:
            try:
                l = self.ser.readline()
                values = l.replace(" \r\n", "").split(" ")
                sum += int( values[pin] )
                counter += 1
            except ValueError:
                pass

        return sum / counter



        
    def run(self):
        self.parse_commandline()
        
        self.ser = PseudoSerial()
        try:
            self.ser = serial.Serial(self.options.port, 115200, timeout=1)
        except serial.SerialException as ex:
            print ex

        time.sleep(1.5)
        self.ser.readline()

        for c, p in {'x': 7, 'y': 6, 'z': 5}.iteritems():
            print "Hold device so %s-axis is perpendicular to gravity" % c
            self.test_countdown(5)
            perp = self.measure_value(5, p)

            print "Hold device so %s-axis is parallel to gravity" % c
            self.test_countdown(5)
            para = self.measure_value(5, p)

            print para - perp
        
            
            
if __name__ == "__main__":
    app = App()
    app.run()
