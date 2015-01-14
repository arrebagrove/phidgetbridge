"""
Micro Load Cell Test

__author__ = 'Daniele Costarella'
__date__ = '18-Dev-2012'
__version__ = '0.0.1'
"""

from time import sleep
from Phidgets.Devices.Bridge import *

count = 0

print("Micro Load Cell Test")

""" Init and open device """

# create object
try:
    dev = Bridge()
except RuntimeError as e:
    print("Runtime Error: %s" % e.message)

# open device
try:
    dev.openPhidget()
    sleep(1)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.detail))
    exit(1)
    

""" wait for attachment (pluggin in) of the Phidget """
print("Waiting for attachment... "),
dev.waitForAttach(10000)
print("Detected " + dev.getDeviceName() + " ;)")

dev.isAttached()
dev.setEnabled(0,1)
dev.getEnabled(0)

dev.setEnabled(1,1)
dev.getEnabled(1)

dev.setEnabled(2,1)
dev.getEnabled(2)

dev.setEnabled(3,1)
dev.getEnabled(3)

dev.setDataRate(1000)

dev.setGain(0,2)
sleep(0.5)
dev.setGain(1,3)
sleep(0.5)
dev.setGain(2,4)
sleep(0.5)
dev.setGain(3,5)
sleep(0.5)


print("Gain Up DX: " + str(dev.getGain(0)))
print("Gain Low DX: " + str(dev.getGain(1)))
print("Gain Up SX: " + str(dev.getGain(2)))
print("Gain Low SX: " + str(dev.getGain(3)))


#Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (dev.isAttached(), dev.getDeviceName(), dev.getSerialNum(), dev.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (dev.getInputCount()))
    print("Data Rate Max: %d" % (dev.getDataRateMax()))
    print("Data Rate Min: %d" % (dev.getDataRateMin()))
    print("Current Data Rate: %d" % (dev.getDataRate()))
    print("Input Value Max: %d" % (dev.getBridgeMax(0)))
    print("Input Value Min: %d" % (dev.getBridgeMin(0)))



displayDeviceInfo()

# Get a data point from Analog Port 0
#print("Value: " + str(dev.getBridgeValue(0)))

while(1):
    try:
        print("%d:\t(Up DX: %f, Low DX: %f - Up SX: %f, Low SX: %f)" % (count, dev.getBridgeValue(0), dev.getBridgeValue(1), dev.getBridgeValue(2), dev.getBridgeValue(3)))
        #print(dev.getBridgeValue(0))
        count = count + 1
        sleep(1)
    except KeyboardInterrupt:
        """ Close and Delete Object"""
        dev.closePhidget()
        
""" Close and Delete """
#dev.closePhidget()
