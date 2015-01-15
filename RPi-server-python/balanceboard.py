"""
Micro Load Cell Test

__author__ = ['Daniele Costarella', 'Giovanni Toscano']
__date__ = '18-Dev-2012'
__version__ = '0.0.1'
"""

import random # test
import socket
import threading
import json
from time import sleep
from Phidgets.Devices.Bridge import *

""" Network config """
# set port (default: 11111)
port = 11111
#ipaddr = socket.gethostbyname(socket.gethostname())
ipaddr = "0.0.0.0"

# socket init
# type: TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ipaddr, port))
serversocket.listen(5)

count = 0
array = [0.]*4

props = {"delay": 1.0, "others" : ""}


print("Micro Load Cell Test")

print("Apertura socket TCP")
print("Indirizzo Bind: " + ipaddr)
print("In ascolto sulla porta ", port)

""" Init and open device """


def phidget_init():
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
    dev.setEnabled(0, 1)
    dev.getEnabled(0)
    dev.setEnabled(1, 1)
    dev.getEnabled(1)
    dev.setEnabled(2, 1)
    dev.getEnabled(2)
    dev.setEnabled(3, 1)
    dev.getEnabled(3)
    dev.setDataRate(1000)
    dev.setGain(0, 2)
    sleep(0.5)
    dev.setGain(1, 3)
    sleep(0.5)
    dev.setGain(2, 4)
    sleep(0.5)
    dev.setGain(3, 5)
    sleep(0.5)

    return dev


#dev = phidget_init()
dev = 0;

#
#
#

# Information Display Function
def displayDeviceInfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (
        dev.isAttached(), dev.getDeviceName(), dev.getSerialNum(), dev.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of bridge inputs: %i" % (dev.getInputCount()))
    print("Data Rate Max: %d" % (dev.getDataRateMax()))
    print("Data Rate Min: %d" % (dev.getDataRateMin()))
    print("Current Data Rate: %d" % (dev.getDataRate()))
    print("Input Value Max: %d" % (dev.getBridgeMax(0)))
    print("Input Value Min: %d" % (dev.getBridgeMin(0)))

def setProperties(jsonObj):
    props['delay'] =(json.loads(jsonObj)["delay"])

def clientthread(connection):
   while True:
      try:
         cmd = connection.recv(5).decode()
         if len(cmd) > 0:
            print("Comando ",cmd, " ricevuto.")
            if(cmd == "READ"):
               for i in range(0,4):
                  array[i] = str(random.uniform(0.0,1.0))
               stringa = "{\"values\":["+array[0]+","+array[1]+","+array[2]+","+array[3]+"],\"props\":{\"delay\":"+str(props['delay'])+"}}"
               #Send è asincrona(default) ma con receive bloccate è sincrona
               connection.send(stringa.encode())
               #ACK
               ack = connection.recv(2).decode()
               print(stringa)
               sleep(props['delay'])
            if(cmd == "SET"):
               connection.send("OK".encode())
               jsonObj = connection.recv(256).decode()
               setProperties(jsonObj)
               #print(jsonObj)
               #delay =(json.loads(jsonObj)["rate"])
      except socket.error as exc:
         print("Client disconnesso : ",exc)
         connection.shutdown(1)
         connection.close()

#displayDeviceInfo()

# Get a data point from Analog Port 0
#print("Value: " + str(dev.getBridgeValue(0)))

if __name__ == '__main__':
    while True:
        conn, addr = serversocket.accept()
        print("Connesso con client " + addr[0] + ":" + str(addr[1]))
        threading.Thread(
            target=clientthread,
            args=((conn,)),
        ).start() 
serversocket.shutdown(1)
serversocket.close()


""" Close and Delete """
#dev.closePhidget()
