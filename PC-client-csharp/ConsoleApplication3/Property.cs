using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;


namespace it.protomgroup.wallt {
   public class Property {

      [JsonProperty("rate")]
      public float Rate { get; set; }

   }
}
