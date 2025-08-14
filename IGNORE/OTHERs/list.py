import json
import requests

device_data = { "address": "equinix_network_device.c8kv-redundant",
    "type": "equinix_network_device",
    "name": "c8kv-single",
    "values": {
        "account_number": "133899",
        "core_count": 2,
        "hostname": "rtr-fr-prim",
        "metro_code": "FR",
        "name": "tf-c8kv-prim",
        "secondary_device": [{
            "account_number": "127154",
            "hostname": "rtr-am-sec",
            "metro_code": "AM",
            "name": "tf-c8kv-sec",
            }],
        "term_length": 1,
        "type_code": "C8000V",
        }
    }

vc_config = { 
    "address": "equinix_fabric_connection.fcr_am_vd_am",
    "mode": "managed",
    "type": "equinix_fabric_connection",
    "name": "fcr_am_vd_am",
    "provider_config_key": "equinix",
    "expressions": {
        "a_side": [{
            "access_point": [{
                "router": [{
                    "uuid": {
                        "references": [
                            "equinix_fabric_cloud_router.fcr_am.uuid",
                            "equinix_fabric_cloud_router.fcr_am"
                            ]
                        }
                    }],
                }]
            }],
        "bandwidth": {
            "constant_value": 50
            },
        "z_side": [{
            "access_point": [{
                "virtual_device": [{
                    "uuid": {
                        "references": [
                            "equinix_network_device.c8kv-redundant.secondary_device[0].uuid",
                            "equinix_network_device.c8kv-redundant.secondary_device[0]",
                            "equinix_network_device.c8kv-redundant.secondary_device",
                            "equinix_network_device.c8kv-redundant"
                            ]
                        }
                    }]
                }]
            }]
        },
    }

exp = vc_config.get('expressions', {})
z_side = exp['z_side'][0]['access_point'][0]
vd = z_side.get('virtual_device', [])




references = vd[0]['uuid']['references']

print(len(references))


if any("secondary" in reference for reference in references):
    print("Yep", references[len(references) - 1])
