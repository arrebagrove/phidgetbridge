using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;


namespace it.protomgroup.wallt {
   public class Properties {

      [JsonProperty("rate")]
      public float Rate { get; set; }

      public Properties(float rate) { 
           Rate = rate;
      }

   }
}
