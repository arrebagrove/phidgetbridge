"""
Micro Load Cell Test

__author__ = ['Daniele Costarella', 'Giovanni Toscano']
__date__ = '18-Dev-2012'
__version__ = '0.0.1'
"""

import random # test
import socket
import thread
from time import sleep
from Phidgets.Devices.Bridge import *

""" Network config """
# set port (default: 11111)
port = 11111
#ipaddr = socket.gethostbyname(socket.gethostname())
ipaddr = "127.0.0.1"

# socket init
# type: TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ipaddr, port))
serversocket.listen(1)

count = 0
array = [0.]*4

print("Micro Load Cell Test")

print("Apertura socket di rete con tipo connessione TCP")
print("Indirizzo server: " + ipaddr)
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
connection, address = serversocket.accept()
print("Connessione con client ", address, " stabilita.")


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


#displayDeviceInfo()

# Get a data point from Analog Port 0
#print("Value: " + str(dev.getBridgeValue(0)))


def waitCommand():
    while 1:
        received = connection.recv(1024).decode()
        if not received: pass
        else: print(received)
        sleep(0.5)


if __name__ == '__main__':
    thread.start_new_thread(waitCommand,())
    while (1):
        try:
            for i in range(0,4):
                #array[i] = dev.getBridgeValue(i)
                array[i] = str(random.uniform(0.0,1.0))
            jsonstring = "{\"cmd\":\"GET\",\"values\":["+array[0]+","+array[1]+","+array[2]+","+array[3]+"],\"props\":{\"rate\":0.5}}"

            #Send e' asincrona(default) ma con receive bloccate e' sincrona
            connection.send(jsonstring.encode())
            #Receive bloccante
            ack = connection.recv(2).decode()
            print(jsonstring)
            count = count + 1
            print("Numero pacchetto: "+str(count))
            sleep(1)

        except KeyboardInterrupt or socket.error as exc:
            serversocket.shutdown(1)
            serversocket.close()
            print("Client disconnesso : ",exc)
            #In attesa di una nuova richiesta
            connection, address = serversocket.accept()
            print("Connessione con nuovo client ", address, " stabilita.")


""" Close and Delete """
#dev.closePhidget()