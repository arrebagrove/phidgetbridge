using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace it.protomgroup.wallt
{
   class BalanceReaderTest
   {

      static void Main()
      {
         while (true)
         {
            BalanceReader reader = new BalanceReader("127.0.0.1", 11111);
            int i = 0;
            while (!reader.IsClosed())
            {
               BalanceObj bObj = reader.read();
               Console.WriteLine(bObj.Values[BalanceObj.UpperLeft]);
               Console.WriteLine(bObj.Values[BalanceObj.UpperRight]);
               Console.WriteLine(bObj.Values[BalanceObj.LowerLeft]);
               Console.WriteLine(bObj.Values[BalanceObj.LowerRight]);
               Console.WriteLine(bObj.Props.Rate);
               i++;
               //Conta fino a 10 e poi chiudi il reader
               
               if (i == 1000)
                  reader.Close();
               else
                  System.Threading.Thread.Sleep(100);
            }
         }
      }
   }
}