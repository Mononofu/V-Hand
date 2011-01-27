import serial
import time
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
                               default=1000,
                               help="Number of lines to store" )

        
        self.parser.add_option("-t",
                               "--time",
                               dest="time",
                               type="int",
                               default=-1,
                               help="Number of seconds to listen" )
        
        self.parser.add_option("-f",
                               "--file",
                               dest="file",
                               default="ser.in",
                               help="Filename to save data" )

        (self.options, self.args) = self.parser.parse_args()

    def run(self):
        self.parse_commandline()
        count = 0

        ser = PseudoSerial()
        try:
            ser = serial.Serial(self.options.port, 115200, timeout=1)
        except serial.SerialException as ex:
            print ex

        f = open(self.options.file, 'w')

        if self.options.time > 0:
            start = time.time()
            while time.time() < ( start + self.options.time ):
                f.write( ser.readline() )
                count += 1
                
        else:
            for _ in range(self.options.lines):
                f.write( ser.readline() )
                count += 1

        f.close()
        print "wrote %d lines" % count
            
            
if __name__ == "__main__":
    app = App()
    app.run()
