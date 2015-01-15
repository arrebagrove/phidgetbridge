using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;


namespace it.protomgroup.wallt {
   public class Properties {

      [JsonProperty("delay")]
      public float Delay { get; set; }

      public Properties(float delay) {
          Delay = delay;
      }

   }
}
