import serial
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
                               action="store_true",
                               dest="port",
                               default="/dev/ttyUSB0",
                               help="Port to lisen on" )

        self.parser.add_option("-l",
                               "--lines",
                               action="store_true",
                               dest="lines",
                               default=1000,
                               help="Number of lines to store" )
        
        self.parser.add_option("-f",
                               "--file",
                               action="store_true",
                               dest="file",
                               default="ser.in",
                               help="Filename to save data" )

        (self.options, self.args) = self.parser.parse_args()

    def run(self):
        self.parse_commandline()

        ser = PseudoSerial()
        try:
            ser = serial.Serial(self.options.port, 115200, timeout=1)
        except serial.SerialException as ex:
            print ex

        f = open(self.options.file, 'w')
        for _ in range(self.options.lines):
            f.write( ser.readline() )
            
            
        
                

            
if __name__ == "__main__":
    app = App()
    app.run()
