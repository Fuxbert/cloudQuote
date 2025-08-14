variable "client_id" {
  description = "fabric client id for authentication"
  default = ""
  sensitive = true
}

variable "client_secret" {
  description = "fabric client id for authentication"
  default = ""
  sensitive = true
}

variable "project_id" {
  description = "Fabric Project-ID"
  default = "e6be59d9-62c0-4140-aad6-150f0700203c"
}

variable "emails" {
  description = "list of notification email recipients"
  default = ["someone@domain.com"]
}

variable "ports" {
  description = "list out existing ports to be used with new infrastructure"
  default = {
    FR = {
      name_prim = "EQX-TESTPOINT-FR6-CX-01"
      prim = ["924ac976-a879-8791-2be0-3eea8c00a394"]
      name_sec = "EQX-TESTPOINT-FR6-CX-SEC-01"
      sec = ["924ac976-a87a-87a1-2be0-3eea8c00a394"]
      }
    AM = {
      name_prim = "EQX-TESTPOINT-AM3-CX-PRI-01"
      prim = ["66284add-86d3-6d30-b4e0-30ac094f8af1"]
      nme_sec = "EQX-TESTPOINT-AM3-CX-SEC-01"
      sec = ["66284add-99eb-9eb0-b4e0-30ac094f8af1"]
      }
    LD = {
      prim = [""]
      sec = [""]
      }
    MA = {
      prim = [""]
      sec = [""]
      }
    PA = {
      prim = [""]
      sec = [""]
      }
    }
}

variable "devices" {
  description = "list out existing virtual devices to be used with new infrastructure"
  default = {
    FR = {
      prim = ["e7838605-de1f-4ee5-8e2c-082e6d853764"]
      sec = [""]
      }
    AM = {
      prim = [""]
      sec = [""]
      }
    LD = {
      prim = [""]
      sec = [""]
      }
    MA = {
      prim = [""]
      sec = [""]
      }
    PA = {
      prim = [""]
      sec = [""]
      }
  }
}

variable "metro_map" {
  description = "map metro codes to countries"
  default = {
    FR = {
      metro_name = "Frankfurt"
      region = "EMEA"
      country = "Germany"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133899"
      code = "FR"
      }
    HH = {
      metro_name = "Hamburg"
      region = "EMEA"
      country = "Germany"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133899"
      }
    MU = {
      metro_name = "Munich"
      region = "EMEA"
      country = "Germany"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133899"
      }
    AM = {
      metro_name = "Amsterdam"
      region = "EMEA"
      country = "The Netherlands"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "127154"
      }
    LD = {
      metro_name = "London"
      region = "EMEA"
      country = "United Kingdom"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133721"
      }
    MA = {
      metro_name = "Manchester"
      region = "EMEA"
      country = "United Kingdom"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133721"
      }
    MD = {
      metro_name = "Madrid"
      region = "EMEA"
      country = "Spain"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "330274"
      }
    DB = {
      metro_name = "Dublin"
      region = "EMEA"
      country = "Ireland"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "306247"
      }
    ML = {
      metro_name = "Milan"
      region = "EMEA"
      country = "Italy"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133024"
      }
    GV = {
      metro_name = "Geneva"
      region = "EMEA"
      country = "Switzerland"
      cba_type = "global"
      currency = "CHF"
      cba_nr = "664689"
      }
    ZH = {
      metro_name = "Zurich"
      region = "EMEA"
      country = "Switzerland"
      cba_type = "global"
      currency = "CHF"
      cba_nr = "664689"
      }
    PA = {
      metro_name = "Paris"
      region = "EMEA"
      country = "France"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133724"
      }
    BX = {
      metro_name = "Bordeaux"
      region = "EMEA"
      country = "France"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "133724"
      }
    BA = {
      metro_name = "Barcelona"
      region = "EMEA"
      country = "Spain"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "330274"
      }
    LS = {
      metro_name = "Lison"
      region = "EMEA"
      country = "Portugal"
      cba_type = "local"
      currency = "EUR"
      cba_nr = "330124"
      }
    SO = {
      metro_name = "Sofia"
      region = "EMEA"
      country = "Bulgaria"
      cba_type = "local"
      currency = "USD"
      cba_nr = "528841"
      }
    IL = {
      metro_name = "Istanbul"
      region = "EMEA"
      country = "Turkey"
      cba_type = "local"
      currency = "USD"
      cba_nr = "310427"
      }
  }
}

variable "bandwidth" {
  description = "use for alternative bandwidth source"
  default = 200
}