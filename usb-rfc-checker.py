import sys
import optparse
import serial.tools.list_ports
__author__ = 'Meir Finkelstine'
__version__= '0.1'
#
#
# 0.1 initial script

debug = False
#Exit Code      Status
# 0     OK
# 1     WARNING
# 2     CRITICAL
# 3     UNKNOWN

def main(comments):
    #comments = parse_args()
    ports = list(serial.tools.list_ports.comports())
    rfidstatus = [ "connected" , "disconnected" ]
    checkRFID = False
    for port_no, description, address in ports:
        if 'Prolific' in description:
            checkRFID = True
            
    if checkRFID == True:
        print "OK - %s %s |'RFID Reader is'=\"%s\"" %(comments[1],rfidstatus[0],rfidstatus[0])
        sys.exit(0)
    else:
        print "CRITICAL - %s %s |'RFID Reader is'=\"%s\"" %(comments[1],rfidstatus[1],rfidstatus[1])
        sys.exit(2)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv)
    else:
        print "Error No arguments were passed"
        sys.exit(100)
    