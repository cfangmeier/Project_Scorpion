#!/usr/bin/python
import Adafruit_MCP230xx as MCP

class Puck:
    address = 0
    mcp = None
    caldata = {}
    current_weight = 0
    led_state = [0,0,0,0]
    


def init_puck(address, caldata):
    mcp = MCP.Adafruit_MCP230XX(address, 16) # MCP23017
    
    for i in range(0,4): mcp.config(i,mcp.OUTPUT); mcp.output(i,0)
    for i in range(5,8): mcp.config(i,mcp.OUTPUT); mcp.output(i,1)
    for i in range(8,16): mcp.config(i,mcp.INPUT)
    
    puck = Puck()
    puck.mcp = mcp
    puck.address = address
    puck.caldata = caldata
    return puck

def _pole_adc(mcp):
    mcp.output(7,0)
    mcp.output(7,1)
    mcp.output(6,0)
    mcp.output(5,0)
    #8 MSBs should be available on pins 8-15
    result = mcp.inputU8(1);

    mcp.output(5,1)
    mcp.output(6,1)

    mcp.output(6,0)
    mcp.output(5,0)
    #2 LSBs should be available on pins 14-15

    lsbs = mcp.inputU8(1);
    result = (result << 2) | (lsbs >> 6)

    mcp.output(5,1)
    mcp.output(6,1)

    return result


def get_weight(puck):
    adc_value = _pole_adc(puck.mcp)
    offset = puck.caldata['offset']
    empty = puck.caldata['empty']
    ratio = puck.caldata['ratio']
    weight = offset + (adc_value - empty) * ratio
    puck.current_weight = weight
    return weight

def set_leds(puck, red, green, blue, white):
    data = [red,green,blue,white]
    if(data != puck.led_state):
        puck.mcp.output(0,blue)
        puck.mcp.output(1,green)
        puck.mcp.output(2,red)
        puck.mcp.output(3,white)
        puck.led_state = data
