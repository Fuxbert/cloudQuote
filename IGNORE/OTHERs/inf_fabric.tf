resource "equinix_fabric_network" "ip_wan_emea" {
  name  = "IP-WAN-EMEA"
  type  = "IPWAN"
  scope = "REGIONAL"
  notifications {
    type   = "ALL"
    emails = var.emails
  }
  project {
    project_id = var.project_id
  }
}
resource "equinix_fabric_network" "evplan_emea" {
  name  = "REGIONAL-EVPLAN-EMEA"
  type  = "EVPLAN"
  scope = "REGIONAL"
  notifications {
    type   = "ALL"
    emails = var.emails
  }
  project {
    project_id = var.project_id
  }
}


resource "equinix_fabric_cloud_router" "fcr_fr"{
  name = "Router-FR"
  type = "XF_ROUTER"
  notifications{
    type = "ALL"
    emails = var.emails
  }
  order {
    purchase_order_number = ""
    term_length = 12    
    }
  location {
    metro_code = var.metro_map.FR.code
    }
  package {
    code = "STANDARD"
    }
  project {
    project_id = var.project_id
    }
  account {
    account_number = var.metro_map.FR.cba_nr
    }
}
resource "equinix_fabric_cloud_router" "fcr_am"{
  name = "Router-AM"
  type = "XF_ROUTER"
  notifications{
    type = "ALL"
    emails = var.emails
  }
  order {
    purchase_order_number = ""
    }
  location {
    metro_code = "AM"
    }
  package {
    code = "STANDARD"
    }
  project {
    project_id = var.project_id
    }
  account {
    account_number = var.metro_map.AM.cba_nr
    }
}


resource "equinix_fabric_connection" "vd_fr_port_fr" {
  name = "FR-VD-FR-Port"
  type = "EVPL_VC"
  notifications {
    type   = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  order {
    purchase_order_number = "1-323292"
  }
  a_side {
    access_point {
      type = "VD"
      virtual_device {
        type = "EDGE"
        uuid = var.devices.FR.prim[0]
      }
      interface {
        type = "NETWORK"
        id = 7
      }
    }
  }
  z_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.prim[0]
      }
      link_protocol {
        type       = "DOT1Q"
        vlan_s_tag = "200"
      }
    }
  }
}
resource "equinix_fabric_connection" "vd_fr_evplan_emea" {
  name = "FR-VD-FR-Port"
  type = "EVPL_VC"
  notifications {
    type   = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  order {
    purchase_order_number = "1-323292"
  }
  a_side {
    access_point {
      type = "VD"
      virtual_device {
        type = "EDGE"
        uuid = var.devices.FR.prim[0]
      }
      interface {
        type = "NETWORK"
        id = 7
      }
    }
  }
  z_side {
    access_point {
      type = "NETWORK"
      network {
        uuid = equinix_fabric_network.evplan_emea.uuid
      }
    }
  }
}
resource "equinix_fabric_connection" "vd_fr_sp_fr" {
  name = "FR-VD-FR-Port"
  type = "EVPL_VC"
  notifications {
    type   = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  order {
    purchase_order_number = "1-323292"
  }
  a_side {
    access_point {
      type = "VD"
      virtual_device {
        type = "EDGE"
        uuid = var.devices.FR.prim[0]
      }
      interface {
        type = "NETWORK"
        id = 7
      }
    }
  }
  z_side {
    access_point {
      type = "SP"
      authentication_key = "<aws_account_id>"
      seller_region = "eu-central-1"
      profile {
        type = "L2_PROFILE"
        uuid = "69ee618d-be52-468d-bc99-00566f2dd2b9"
      }
      location {
        metro_code = var.metro_map.FR.code
      }
    }
  }
}


resource "equinix_fabric_connection" "fcr_fr_ipwan_emea"{
  name = "fcr-fr-ipwan-emea"
  type = "IPWAN_VC"
  notifications{
    type = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_fr.uuid
      }
    }
  }
  z_side {
    access_point {
      type = "NETWORK"
      network {
        uuid = equinix_fabric_network.ip_wan_emea.uuid
      }
    }
  }
}
resource "equinix_fabric_connection" "fcr_am_ipwan_emea"{
  name = "fcr-am-ipwan-emea"
  type = "IPWAN_VC"
  notifications{
    type = "ALL"
    emails = var.emails
  }
  bandwidth = var.bandwidth
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = "e27dd359-2a94-4c3d-9dbf-759e6cf24dd7"
      }
    }
  }
  z_side {
    access_point {
      type = "NETWORK"
      network {
        uuid = "20fcdd6b-fb4d-457e-8714-9519335ef50a"
      }
    }
  }
}
resource "equinix_fabric_connection" "fcr_fr_port_fr_prim"{
  name = "FCR > prim Port FR"
  type = "IP_VC"
  notifications {
    type = "ALL"
    emails = var.emails
    }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_fr.uuid
        }
      }
    }
  z_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.prim[0]
        }
      link_protocol {
        type = "DOT1Q"
        vlan_tag = "100"
        }
      location {
        metro_code = "FR"
        }
      }
    }
}
resource "equinix_fabric_connection" "fcr_fr_port_fr_sec"{
  name = "FCR > sec Port FR"
  type = "IP_VC"
  notifications {    
    type = "ALL"
    emails = var.emails
    }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_fr.uuid
        }
      }
    }
  z_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.sec[0]
        }
      link_protocol {
        type = "DOT1Q"
        vlan_tag = "100"
        }
      location {
        metro_code = "FR"
        }
      }
    }
}
resource "equinix_fabric_connection" "fcr_fr_vd_fr"{
  name = "FCR FR > VD FR"
  type = "IP_VC"
  notifications {    
    type = "ALL"
    emails = var.emails
    }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_fr.uuid
        }
      }
    }
  z_side {
    access_point {
      type = "VD"
      virtual_device {
        uuid = var.devices.FR.prim[0]
        type = "EDGE"
        }
      interface {
        type = "CLOUD"
        id = 8
        }
      link_protocol {
        type = "DOT1Q"
        vlan_tag = "100"
        }
      }
    }
}
resource "equinix_fabric_connection" "fcr_am_vd_am"{
  name = "FCR AM > sec VD AM"
  type = "IP_VC"
  notifications {    
    type = "ALL"
    emails = var.emails
    }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_am.uuid
        }
      }
    }
  z_side {
    access_point {
      type = "VD"
      virtual_device {
        uuid = equinix_network_device.c8kv-redundant.secondary_device[0].uuid
        type = "EDGE"
        }
      interface {
        type = "CLOUD"
        id = 8
        }
      link_protocol {
        type = "DOT1Q"
        vlan_tag = "200"
        }
      }
    }
}
resource "equinix_fabric_connection" "fcr_fr_sp"{
  name = "FCR > AWS FR"
  type = "IP_VC"
  notifications {    
    type = "ALL"
    emails = var.emails
    }
  bandwidth = 50
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "CLOUD_ROUTER"
      router {
        uuid = equinix_fabric_cloud_router.fcr_fr.uuid
        }
      }
    }
  z_side {
    access_point {
      type = "SP"
      authentication_key = "<aws_account_id>"
      seller_region = "eu-central-1"
      profile {
        type = "L2_PROFILE"
        uuid = "69ee618d-be52-468d-bc99-00566f2dd2b9"
      }
      location {
        metro_code = var.metro_map.FR.code
      }
    }
  }
}

resource "equinix_fabric_connection" "port_fr_port_fr" {
  name = "Port FR > Port FR"
  type = "EVPL_VC"
  notifications {
    type = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  order {
    purchase_order_number= ""
  }
  a_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.prim[0]
      }
      link_protocol {
        type = "DOT1Q"
        vlan_s_tag = "100"

      }
    }
  }
  z_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.sec[0]
      }
      link_protocol {
        type = "DOT1Q"
        vlan_s_tag = "100"
      }
    }
  }
}
resource "equinix_fabric_connection" "port_fr_sp_fr" {
  name = "FR-Port-FR-AWS-SP"
  type = "EVPL_VC"
  notifications {
    type = "ALL"
    emails = var.emails
  }
  bandwidth = 50
  redundancy { priority= "PRIMARY" }
  order {
    purchase_order_number= "1-323929"
  }
  a_side {
    access_point {
      type= "COLO"
      port {
        uuid = var.ports.FR.prim[0]
      }
      link_protocol {
        type = "DOT1Q"
        vlan_s_tag = "105"
      }
    }
  }
  z_side {
    access_point {
      type = "SP"
      authentication_key = "<aws_account_id>"
      seller_region = "eu-central-1"
      profile {
        type = "L2_PROFILE"
        uuid = "69ee618d-be52-468d-bc99-00566f2dd2b9"
      }
      location {
        metro_code = var.metro_map.FR.code
      }
    }
  }

  additional_info = [
    { key = "accessKey", value = "<aws_access_key>" },
    { key = "secretKey", value = "<aws_secret_key>" }
  ]
}
resource "equinix_fabric_connection" "port_fr_evplan_emea"{
  name = "fcr-fr-ipwan-emea"
  type = "EVPL_VC"
  notifications{
    type = "ALL"
    emails = var.emails
  }
  bandwidth = 500
  order {
    purchase_order_number = ""
    }
  a_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.prim[0]
      }
    }
  }
  z_side {
    access_point {
      type = "NETWORK"
      network {
        uuid = equinix_fabric_network.evplan_emea.uuid
      }
    }
  }
}

/*
resource "equinix_fabric_connection" "port2token" {
  name = "FR-port-2-FR-token"
  type = "EVPL_VC"
  notifications {
    type   = "ALL"
    emails = ["example@equinix.com", "test1@equinix.com"]
  }
  bandwidth = 50
  order {
    purchase_order_number = "1-323292"
  }
  a_side {
    access_point {
      type = "COLO"
      port {
        uuid = var.ports.FR.prim[0]
      }
      link_protocol {
        type       = "DOT1Q"
        vlan_s_tag = "100"
      }
    }
  }
  z_side {
    service_token {
      uuid = "8bdb6a14-c811-4aaa-9c2f-5a03e0737755"
    }
  }
}
*/