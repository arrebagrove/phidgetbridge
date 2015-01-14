import socket
import time
import random

#Porta ed indirizzo server
port = 11111
#ipaddr = socket.gethostbyname(socket.gethostname())
ipaddr = "127.0.0.1"

array = [0.]*4

#Creazione socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((ipaddr, port))
serversocket.listen(2)

print("Apertura socket di rete con tipo connessione TCP")
print("Indirizzo server: " + ipaddr)
print("In ascolto sulla porta ", port)

connection, address = serversocket.accept()

print("Connessione con client ", address, " stabilita.")

while True:      
   #Scorro la matrice per colonne
   for i in range(0,4):
       array[i] = str(random.uniform(0.0,1.0))
   stringa = "{\"cmd\":\"GET\",\"values\":["+array[0]+","+array[1]+","+array[2]+","+array[3]+"],\"props\":{\"rate\":0.5,\"altro\":\"qualcosa\"}}"
   try:
      #Send è asincrona(default) ma con receive bloccate è sincrona
      connection.send(stringa.encode())
      
      #Receive bloccante
      ack = connection.recv(2).decode()
      print(stringa)

      #time.sleep(0.1)
   except socket.error as exc:
      print("Client disconnesso : ",exc)
      connection.shutdown(1)
      connection.close()
      #In attesa di una nuova richiesta
      connection, address = serversocket.accept()

      print("Connessione con client ", address, " stabilita.")
      
serversocket.shutdown(1)
serversocket.close()
