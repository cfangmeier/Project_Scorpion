#!/usr/bin/python
import Adafruit_MCP230xx as MCP
import time
import numpy as np

def setup_io():
    mcp = MCP.Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017
    mcp.config(5,mcp.OUTPUT); mcp.output(5,1)
    mcp.config(6,mcp.OUTPUT); mcp.output(6,1)
    mcp.config(7,mcp.OUTPUT); mcp.output(7,1)
    
    mcp.config(8, mcp.INPUT); #mcp.pullup(8, 1)
    mcp.config(9, mcp.INPUT); #mcp.pullup(9, 1)
    mcp.config(10,mcp.INPUT); #mcp.pullup(10,1)
    mcp.config(11,mcp.INPUT); #mcp.pullup(11,1)
    mcp.config(12,mcp.INPUT); #mcp.pullup(12,1)
    mcp.config(13,mcp.INPUT); #mcp.pullup(13,1)
    mcp.config(14,mcp.INPUT); #mcp.pullup(14,1)
    mcp.config(15,mcp.INPUT); #mcp.pullup(15,1)
    
    
    mcp.config(0,mcp.OUTPUT); mcp.output(0,0)
    mcp.config(1,mcp.OUTPUT); mcp.output(1,0)
    mcp.config(2,mcp.OUTPUT); mcp.output(2,0)
    mcp.config(3,mcp.OUTPUT); mcp.output(3,0)


    mcp.output(5,1)
    mcp.output(6,1)
    mcp.output(7,1)

    mcp.output(7,0); pause("convst_n pushed down")
    mcp.output(7,1); pause("convst_n pushed up")
    return mcp

def pause(message = ""):
    #print message
    #raw_input()
    #time.sleep(0.01)
    pass

def pole_adc(mcp):

    mcp.output(7,0); pause("convst_n pushed down")
    mcp.output(7,1); pause("convst_n pushed up")
    mcp.output(6,0); pause("cs_n pushed down")
    mcp.output(5,0); pause("rd_n pushed down")
    #8 MSBs should be available on pins 8-15
    result = mcp.inputU8(1);
    #print "MSBs: ", bin(result)


    mcp.output(5,1); pause("rd_n pushed up")
    mcp.output(6,1); pause("cs_n pushed up")

    mcp.output(6,0); pause("cs_n pushed down")
    mcp.output(5,0); pause("rd_n pushed down")
    #2 LSBs should be available on pins 14-15

    lsbs = mcp.inputU8(1);
    #print "LSBs: ", bin(lsbs)
    result = (result << 2) | (lsbs >> 6)

    mcp.output(5,1); pause("rd_n pushed up")
    mcp.output(6,1); pause("cs_n pushed up\nCYCLE COMPLETE\n\n")

    return result


def stat_test(mcp, n = 200):
    samples = []
    while n != 0:
        samples.append(pole_adc(mcp))
        n -= 1
    samples = np.array(samples)
    print np.mean(samples)
    print np.std(samples)
    print np.max(samples), " ",np.min(samples)


def set_leds(mcp, red, green, blue, white):
    mcp.output(0,blue)
    mcp.output(1,green)
    mcp.output(2,red)
    mcp.output(3,white)

def led_indication():
    mcp = setup_io()
    
    while True:
        value = pole_adc(mcp)
        if value < 160: set_leds(mcp,0,0,0,0)
        elif value < 190: set_leds(mcp,1,0,0,0)
        elif value < 210: set_leds(mcp,1,1,0,0)
        elif value < 240: set_leds(mcp,1,1,1,0)
        else: set_leds(mcp,1,1,1,1)
        

def log_weight(interval,iterations,filename):
    f = open(filename,'w')
    mcp = setup_io()
    for i in range(iterations):
        value = pole_adc(mcp)
        line = "%(val)03d\n" % {"val":value}
        f.write(line)
        time.sleep(interval)
    f.close()
    

def flash_leds():
    mcp = setup_io()
   

    while True: 
        set_leds(mcp,0,0,0,1)
        time.sleep(0.3)
        set_leds(mcp,1,0,0,0)
        time.sleep(0.3)
        set_leds(mcp,0,1,0,0)
        time.sleep(0.3)
        set_leds(mcp,0,0,1,0)
        time.sleep(0.3)

if __name__ == '__main__':
    led_indication()





