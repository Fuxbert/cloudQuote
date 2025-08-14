resource "equinix_network_acl_template" "new_acl" {
  name        = "NACL for project CLoudQuote"
  description = "Dummy ACL template"
  project_id = var.project_id
  inbound_rule {
    subnet  = "0.0.0.0/0"
    protocol = "IP"
    src_port = "any"
    dst_port = "any"
    description = "inbound rule description"
    }
  inbound_rule {
    subnet  = "0.0.0.0/0"
    protocol = "UDP"
    src_port = "any"
    dst_port = "any"
    }
}

resource "equinix_network_device" "c8kv-redundant" {
  name            = "tf-c8kv-prim"
  metro_code      = "FR"
  type_code       = "C8000V"
  self_managed    = true
  byol            = true
  package_code    = "network-essentials"
  notifications   = var.emails
  hostname        = "rtr-fr-prim"
  account_number  = var.metro_map.FR.cba_nr
  version         = "17.06.01a"
  core_count      = 2
  term_length     = 1
  ssh_key {
    username = "test-username"
    key_name = "valid-key-name"
  }
  acl_template_id = equinix_network_acl_template.new_acl.id
  secondary_device {
    name = "tf-c8kv-sec"
    metro_code = "AM"
    hostname = "rtr-am-sec"
    notifications = var.emails
    account_number = var.metro_map.AM.cba_nr
  }
}