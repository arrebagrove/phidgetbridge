using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using Newtonsoft.Json;


namespace it.protomgroup.wallt {

   class BalanceReader {
      private byte[] bytes = new byte[256];
      private string strJson = "";
      private Socket receiver;
      private int port;

      private IPAddress ipAddr;
      private IPEndPoint remoteEP;

      private bool closed = true;

      public BalanceReader(string ipAddress, int portNumber) {
         try {
            port = portNumber;
            ipAddr = IPAddress.Parse(ipAddress);
            remoteEP = new IPEndPoint(ipAddr, port);

            receiver = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            try {
               receiver.Connect(remoteEP);
               Console.WriteLine("Client connesso a {0}", receiver.RemoteEndPoint.ToString());
               closed = false;
               strJson = "";
            } catch (Exception e) {
               Console.WriteLine("Connessione con client {0}:{1} non riuscita: {2} ", ipAddr, port, e.ToString());
               Console.Read();
            }
         } catch (FormatException fe) {
            Console.WriteLine("Indirizzo IP {0} non valido: {1}", ipAddress, fe.ToString());
            Console.Read();
         } catch (SocketException se) {
            Console.WriteLine("Impossibile inizializzare la connessione: ", ipAddress, se.ToString());
            Console.Read();
         }
      }

      public BalanceObj read() {
         BalanceObj ret = null;
         try {
            int bytesRec = receiver.Receive(bytes);
            strJson = Encoding.ASCII.GetString(bytes, 0, bytesRec);

            byte[] ack = Encoding.ASCII.GetBytes("OK");
            int bytesSent = receiver.Send(ack);

            Console.WriteLine("[Read]Byte ricevuti = {0}", bytesRec);
            Console.WriteLine("[Read]Stringa JSON ricevuta = {0}", strJson);
            ret = JsonConvert.DeserializeObject<BalanceObj>(strJson);
         } catch (ArgumentNullException ane) {
            Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
            Close();
         } catch (SocketException se) {
            Console.WriteLine("SocketException : {0}", se.ToString());
            Close();
         } catch (Exception e) {
            Console.WriteLine("Unexpected exception : {0}", e.ToString());
            Close();
         }
         return ret;
      }

      public bool IsClosed() {
         return (closed == true);
      }

      public void Close() {
         receiver.Shutdown(SocketShutdown.Both);
         receiver.Close();

         closed = true;
      }
   }
}
