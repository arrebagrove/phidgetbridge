using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Collections;
using it.protomgroup.wallt;


namespace it.protomgroup.wallt
{
   public class BalanceObj
   {
      public const int UpperLeft  = 0;
      public const int UpperRight = 1;
      public const int LowerLeft  = 2;
      public const int LowerRight = 3;

      [JsonProperty("cmd")]
      public string Cmd { get; set; }

      [JsonProperty("values")]
      public float[] Values { get; set; }

      [JsonProperty("props")]
      public Property Props { get; set; }
   }
}
