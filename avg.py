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

        self.parser.add_option("-l",
                               "--lines",
                               dest="lines",
                               type="int",
                               default=-1,
                               help="Number of lines to listen for" )

        
        self.parser.add_option("-t",
                               "--time",
                               dest="time",
                               type="int",
                               default=-1,
                               help="Number of seconds to listen" )
        
        self.parser.add_option("-f",
                               "--file",
                               dest="file",
                               default="",
                               help="File to read from" )

        (self.options, self.args) = self.parser.parse_args()

    def run(self):
        self.parse_commandline()

        
        
        if self.options.time > 0:

            ser = PseudoSerial()
            try:
                ser = serial.Serial(self.options.port, 115200, timeout=1)
            except serial.SerialException as ex:
                print ex

            time.sleep(1.5)
            ser.readline()
            averages = [0 for _ in range(len(ser.readline().replace(" \r\n", "").split(" ")))]
            counter = 0
        
            begin = time.time()
            
            while time.time() < begin + self.options.time:
                try:
                    l = ser.readline()
                    values = l.replace(" \r\n", "").split(" ")
                    for i in range(len(values)):
                        averages[i] += int( values[i] )
                    counter += 1
                except ValueError:
                    pass

            i = 0
            for v in averages:
                print "%2d  %4d" % (i, v / counter)
                i += 1
            
        elif self.options.lines > 0:
            for _ in range(self.options.lines):
                line = "%f:" % ( time.time() - start )
                line += ser.readline()
                f.write( line )
                
                count += 1

            pass
        elif len(self.options.file) > 0:
            pass
        else:
            self.parser.print_help()
            sys.exit()

        
            
            
            
if __name__ == "__main__":
    app = App()
    app.run()

