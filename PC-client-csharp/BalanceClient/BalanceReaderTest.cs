using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace it.protomgroup.wallt {
   class BalanceReaderTest {

      static void Main() {
         BalanceReader reader = new BalanceReader("127.0.0.1", 11111);

         Properties props = new Properties(2.0f);
         reader.setProperties(props);

         int i = 0;
         while (!reader.IsClosed()) {
            BalanceObj bObj = reader.readBalanceObj();
            Console.WriteLine(bObj.Values[BalanceObj.UpperLeft]);
            Console.WriteLine(bObj.Values[BalanceObj.UpperRight]);
            Console.WriteLine(bObj.Values[BalanceObj.LowerLeft]);
            Console.WriteLine(bObj.Values[BalanceObj.LowerRight]);
            Console.WriteLine(bObj.Props.Delay);
            i++;
            //Conta fino a 10 e poi chiudi il reader

            if (i == 5)
               reader.Close();
            //else
            //   System.Threading.Thread.Sleep(1000);
         }
      }
   }
}