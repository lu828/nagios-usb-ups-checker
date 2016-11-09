#!/usr/bin/python
import json
import re,sys,commands,os
import optparse
import urllib2
import simplejson,urllib
import socket
#from swf.movie import SWF
__author__ = 'Meir Finkelstine'
__version__= '0.9'
#
#
# 0.5 adding check for printing comments or not
# 0.6 adding graph results
# 0.8 adding host check alive  

debug = False
#Exit Code      Status
# 0     OK
# 1     WARNING
# 2     CRITICAL
# 3     UNKNOWN


j = []

j = json.loads('{"inVolt":"179.4V","model":"ON-LINE", "upsTemp":"25.9C","status":"Normal","inFreq":"49.9Hz","outVolt":"229.9V","outFreq":"49.9Hz","loadPercent":"0%","batV":"40.8V","batCapacity":"100%"}')

def get_num(x):
    
    if debug : print "value %s" %x
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))

def checkAlive(host,port):
    status = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5) 
    try:
        s.connect((host, port))
        s.shutdown(2)
        if debug :
            print "Success connecting to "
            print host + " on port: " + str(port)
    except:
        msgA =  "CRITICAL - Host %s OFFLINE unable to open socket" %host
        #sys.exit(2)
        pass
     


def main():
    """ Main plugin """
    ( host, dev, port, comments ) = parse_args()
    port = 15178

    

    url = 'http://%s:%s/0?json' %(host,port)
    usbUrls = {
        'oldVP' : 'http://%s:%s/0?json',
        'newVP' : 'http://%s:%s/ViewPower/#'
    }

    if port != 15178 : 
        print "oldVP"
        url = usbUrls['oldVP'] %(host,port )
    else:
        print "newVP"
        url = usbUrls['newVP'] %(host,port )
    
    checkAlive(host,port)

    #print rls['oldVP'] %(host,port )
    print url   
    checkAlive(host,port)
    
    if port != 15178 : 
        try :
            j = simplejson.load(urllib.urlopen(url))
        except:
            print "CRITICAL - %s Unable to retrive json file " %host
            sys.exit(2)
    

    sys.exit(4)

    if debug :    print "host %s \ndevice %s \nurl %s \njson data \n\n %s" %(host, dev, url,j )

    if dev == "model":
        if debug : print "you have choosed module = %s jsonValue %s" %(dev, j['model'])
        information_module(j['model'],comments)
    elif dev == "upstemp":
        if debug : print "you have choosed upstemp = %s jsonValue %s" %(dev, j['upsTemp'])
        iformation_upstemp(j['upsTemp'],comments)
    elif dev == "ivoltage":
        if debug : print "you have choosed ivoltage = %s jsonValue %s" %(dev,j['inVolt'])
        input_voltage(j['inVolt'],comments)
    elif dev == "ifreq":
        if debug : print "you have choosed ifreq = %s jsonValue %s" %(dev, j['inFreq'])
        input_freq(j['inFreq'],comments)
    elif dev == "ovoltage":
        if debug : print "you have choosed ovoltage = %s jsonValue %s" %(dev, j['outVolt'])
        output_voltage(j['outVolt'],comments)
    elif dev == "ofreq":
        if debug : print "you have choosed ofreq = %s jsonValue %s" %(dev, j['outFreq'])
        output_freq(j['outFreq'],comments)
    elif dev == "oload":
        if debug : print "you have choosed oload = %s jsonValue %s" %(dev, j['loadPercent'])
        output_load(j['loadPercent'],comments)
    elif dev == "bvoltage":
        if debug : print "you have choosed bvoltage = %s jsonValue %s" %(dev, j['batV'])
        battery_voltage(j['batV'],comments)
    elif dev == "bcapacity":
        if debug : print "you have choosed bcapacity = %s jsonValue %s" %(dev, j['batCapacity'])
        battery_capacity(j['batCapacity'],comments)
    else:
        print "you have choosed unknown device = %s" %dev

def information_module(module,comments):
    if module == "ON-LINE":
        print "OK - module status is %s|'module status is'=%s " %( module, module)
        sys.exit(0)
    elif module == "SELF_TEST":
        if comments:
            print "WARNING - module status is %s comments %s |'module status is'=%s " % (module,comments,module)
        else:
            print "WARNING - module status is %s |'module status is'=%s " % (module,module)
        sys.exit(1)
    elif module == "":
        if comments:
            print "CRITICAL - module status is %s comments %s |'module status is'=%s " % (module,comments,module)
        else:
            print "CRITICAL - module status is %s |'module status is'=%s " % (module,module)
        sys.exit(2)
    else:
        print "UKNOWN - module status is %s|'module status is'=%s " % (module,module)
        sys.exit(3)

def iformation_upstemp(upstemp,comments):
    # iformation_upstemp = 29N 35 W 35 C

    upstemp = get_num(upstemp)
    if int(upstemp) >= 0 and int(upstemp) <= 54.9:
        print "OK - UPS Temperture is %s|'UPS Temperture is'=%s" %(upstemp,upstemp)
        sys.exit(0)
    elif int(upstemp)  >= 55 and int(upstemp) <= 59.9:
        if comments:
            print "WARNING - UPS Temperture is %s comments %s |'UPS Temperture is'=%s" %(upstemp,comments,upstemp)
        else:
            print "WARNING - UPS Temperture is %s|'UPS Temperture is'=%s" %(upstemp,upstemp)
        sys.exit(1)
            
    elif int(upstemp) > 60:
        if comments:
            print "CRITICAL - UPS Temperture is %s comments %s | 'UPS Temperture is'=%s" %(upstemp,comments,upstemp)
        else:
            print "CRITICAL - UPS Temperture is %s |'UPS Temperture is'=%s" %(upstemp,upstemp)
        sys.exit(2)
    else:
        print "UKNOWN - UPS Temperture is %s|'UPS Temperture is'=%s" %(upstemp,upstemp)
        sys.exit(3)

def input_voltage(inputVoltage,comments):

    input_voltage = get_num(inputVoltage)

    if int(input_voltage) >= 200 and int(input_voltage) <= 240 :
        print "OK - Input Voltage is %s|'Input Voltage is'=%s" %( input_voltage,input_voltage)
        sys.exit(0)
    elif int(input_voltage)  >= 241 and int(input_voltage) <= 260 or int(input_voltage) < 180:
        if comments:
            print "WARNING - Input Voltage is %s comments %s | 'Input Voltage is'=%s" %(input_voltage,comments,input_voltage)
        else:
            print "WARNING - Input Voltage is %s | 'Input Voltage is'=%s " %(input_voltage,input_voltage)
        sys.exit(1)
    elif int(input_voltage) >= 261 or int(input_voltage) <= 200 :
        if comments:
            print "CRITICAL - Input Voltage is %s comments %s | 'Input Voltage is'=%s" %(input_voltage,comments,input_voltage)
        else:
            print "CRITICAL - Input Voltage is %s | 'Input Voltage is'=%s" %( input_voltage,input_voltage)
        sys.exit(2)
    else:
        print "UKNOWN - Input Voltage is %s| 'Input Voltage is'=%s" %( input_voltage,input_voltage)
        sys.exit(3)
def input_freq(inputFreq,comments):

    input_freq = get_num(inputFreq)

    if int(input_freq) < 55:
        print "OK - Input Freq is %s| 'Input Freq is'=%s" %(input_freq,input_freq)
        sys.exit(0)
    elif int(input_freq) <= 60:
        if comments:
            print "WARNING - Input Freq is %s comments %s |'Input Freq is'=%s" %(input_freq,comments,input_freq)
        else:
            print "WARNING - Input Freq is %s|'Input Freq is'=%s" %(input_freq,input_freq)
        sys.exit(1)
    elif int(input_freq) > 60:
        if comments:
            print "CRITICAL - Input Freq is %s comments %s |'Input Freq is'=%s" %(input_freq, comments,input_freq)
        else:
            print "CRITICAL - Input Freq is %s |'Input Freq is'=%s" %(input_freq,input_freq)
        sys.exit(2)
    else:
        print "UKNOWN - Input Freq is %s|'Input Freq is'=%s" %(input_freq,input_freq)
        sys.exit(3)

def output_voltage(outVoltage,comments):
    output_voltage = get_num(outVoltage)
    if int(output_voltage) < 235:
        print "OK - Output Voltage is %s|'Output Voltage is'=%s" %(output_voltage,output_voltage)
        sys.exit(0)
    elif int(output_voltage)  >= 235 and int(output_voltage)  <= 240:
        if comments:
            print "WARNING - Output Voltage is %s comments %s|'Output Voltage is'=%s" %( output_voltage, comments,output_voltage)
        else:
            print "WARNING - Output Voltage is %s |'Output Voltage is'=%s" %(output_voltage,output_voltage)
        sys.exit(1)
    elif int(output_voltage) > 240:
        if comments:
            print "CRITICAL - Output Voltage is %s comments %s|'Output Voltage is'=%s" %( output_voltage, comments,output_voltage)
        else:    
            print "CRITICAL - Output Voltage is %s|'Output Voltage is'=%s" %(output_voltage,output_voltage)
        sys.exit(2)
    else:
        print "UKNOWN - Output Voltage is %s|'Output Voltage is'=%s" %(output_voltage,output_voltage)
        sys.exit(3)

def output_freq(outFreq,comments):
    # output_freq                   = 55W  60C          outFreq
    # output_freq = get_num(j['outFreq'])
    output_freq = get_num(outFreq)
    if int(output_freq) < 55:
        print "OK - Output Freq is %s|'Output Freq is'=%s" %(output_freq, output_freq)
        sys.exit(0)
    elif int(output_freq) >= 55 and int(output_freq) <= 60 :
        if comments:
            print "WARNING - Output Freq is %s comments %s|'Output Freq is'=%s " %(output_freq, comments,output_freq)
        else:
            print "WARNING - Output Freq is %s |'Output Freq is'=%s" %(output_freq, output_freq)
        sys.exit(1)
    elif int(output_freq) > 60:
        if comments:
            print "CRITICAL - Output Freq is %s comments %s|'Output Freq is'=%s " %(output_freq, comments,output_freq)
        else:
            print "CRITICAL - Output Freq is %s|'Output Freq is'=%s" %(output_freq, output_freq)
        sys.exit(2)
    else:
        print "UKNOWN - Output Freq is %s|'Output Freq is'=%s" %(output_freq, output_freq)
        sys.exit(3)

def output_load(outLoad,comments):
    # output_load                       = 30N 31-40W 40C    loadPercent
    output_load = get_num(outLoad)
    #output_load = get_num(j['loadPercent'])
    if int(output_load) < 30:
        print "OK - Output Load is %s|'Output Load is'=%s" %(output_load,output_load)
        sys.exit(0)
    elif int(output_load)  >= 31 and int(output_load) <= 40 :
        if commnts:
            print "WARNING - Output Load is %s comments %s |'Output Load is'=%s" %(output_load, comments,output_load)
        else:
            print "WARNING - Output Load is %s |'Output Load is'=%s" %(output_load,output_load)
        sys.exit(1)
    elif int(output_load) > 40 :
        if comments:
            print "CRITICAL - Output Load is %s comments %s |'Output Load is'=%s" %(output_load, comments,output_load)
        else:
            print "CRITICAL - Output Load is %s comments %s|'Output Load is'=%s" %(output_load,output_load)
        sys.exit(2)
    else:
        print "UKNOWN - Output Load is %s|'Output Load is'=%s" %(output_load,output_load)
        sys.exit(3)
def battery_voltage(batteryVoltage,comments):
    # battery_voltage    = 50-40N 39-25W 24C    batV
    battery_voltage = get_num(batteryVoltage)
    #battery_voltage = get_num(j['batV'])
    if int(battery_voltage) >= 40 and int(battery_voltage) <= 60 :
        print "OK - Battay Voltage is %s|'Battay Voltage is'=%s" %( battery_voltage,battery_voltage)
        sys.exit(0)
    elif int(battery_voltage) >= 25 and int(battery_voltage) <= 39 :
        if comments:
            print "WARNING - Battay Voltage is %s comments %s|'Battay Voltage is'=%s " %( battery_voltage, comments,battery_voltage)
        else:
            print "WARNING - Battay Voltage is %s|'Battay Voltage is'=%s" %( battery_voltage,battery_voltage)
        sys.exit(1)
    elif int(battery_voltage) <= 24:
        if comments :
            print "CRITICAL - Battay Voltage is %s comments %s|'Battay Voltage is'=%s " %( battery_voltage, comments,battery_voltage)
        else:
            print "CRITICAL - Battay Voltage is %s|'Battay Voltage is'=%s" %( battery_voltage,battery_voltage)
        sys.exit(2)
    else:
        print "UKNOWN - Battay Voltage is %s|'Battay Voltage is'=%s" %( battery_voltage,battery_voltage)
        sys.exit(3)

def battery_capacity(batteryCapacity,comments):
    # battery_capacity   = 100-70N 69-30W 29-0C batCapacity
    battery_capacity = get_num(batteryCapacity)
    
    if int(battery_capacity) >= 70 and int(battery_capacity) <= 100 :
        print "OK - Battay Capacity is %s|'Battay Capacity is'=%s" %(battery_capacity,battery_capacity)
        sys.exit(0)
    elif int(battery_capacity) >= 30 and int(battery_capacity) <= 69:
        if comments:
            print "WARNING - Battay Capacity is %s comments %s|'Battay Capacity is'=%s " %( battery_capacity, comments,battery_capacity)
        else:
            print "WARNING - Battay Capacity is %s |'Battay Capacity is'=%s" %(battery_capacity,battery_capacity)
        sys.exit(1)
    elif int(battery_capacity) < 30 :
        if comments:
            print "CRITICAL - Battay Capacity is %s comments %s|'Battay Capacity is'=%s " %( battery_capacity, comments,battery_capacity)
        else:
            print "CRITICAL - Battay Capacity is %s |'Battay Capacity is'=%s" %(battery_capacity,battery_capacity)
        sys.exit(2)
    else:
        print "UKNOWN - Battay Capacity is %s|'Battay Capacity is'=%s" %(battery_capacity,battery_capacity)
        sys.exit(3)
def parse_args():
    if debug : print "Start extracting cli arguments\n"
    usage = "usage: %prog [options] arg1 arg2\
            \n\n\tdevice name Brif Description\
            \n\tmodel         : status ONLINE|SELF_TEST etc\
            \n\tupstemp       : UPS Temperture\
            \n\tivoltage      : Input Voltage \
            \n\tifreq         : Input Freq \
            \n\tovoltage      : Output Voltage\
            \n\tofreq         : Output Freq\
            \n\toload         : Output Load\
            \n\tbvoltage      : Battery Voltage\
            \n\tbcapacity     : Battery Capacity"

    #parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-H", "--host", dest="hostname",
                        type="string", help="specify hostname to run on")
    parser.add_option("-d", "--devname", dest="device", type="string",help="device name")
    parser.add_option("-p", "--port", dest="port",type="int", help="Enter Remote Port Number", default=8888)
    parser.add_option("-c", "--comment", dest="comments", type="string", help="Add Comments to display on Warnings/Critical Messages")
    (options, args) = parser.parse_args()

    if ( options.hostname is None )  or ( options.device is None ) :
        parser.error("incorrect number of arguments")
    return options.hostname, options.device, options.port, options.comments


def openLocalLogFile(file):
    print "opening log file"


if __name__ == '__main__':
    main()

