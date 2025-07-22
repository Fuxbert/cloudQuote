import json
import requests
import currency_converter
from currency_converter import CurrencyConverter
import textwrap

line = ("-" * 75)

with open('banner.txt', 'r') as file:
    banner = file.read()
    print(banner)

print("  \033[1mThank you for using Cloud Quote!\033[0m")
print(textwrap.fill("Please mind this is a beta and some features might not be supported in current state. The project will be maintained regularly to catch up with latest developments and enhancements on Equinix terraform provider.", width = 90, initial_indent="  ", subsequent_indent="  "))
print()
print("  Please check <README.mk> for more details and guidance.")
print()
print()

print("  Please provide the path to the tfplan.json file (PATH/TO/FILE.json)")
path = input("  - Default: tfplan.json (in active folder): ")
if path == "":
    path = '../JSONs/tfplan.json'
    print(textwrap("Reminder: to generate tfplan file in JSON format the following commands should be used: 'terraform plan -out=tfplan.binary && terraform show -json tfplan.binary > <PATH/TO/FILE.json> && rm tfplan.binary", width = 90, initial_indent="  ", subsequent_indent="  "))
print()
print("  What is your desired currency to be displayed?")
local_currency = input("  - Please use ISO 4217 code (EUR, USD, etc). Default: EUR: ")
if local_currency == "":
    local_currency = "EUR"
print()
fcr = 0; ne = 0; vc = 0; cost = 0; total = 0; assets = 0; fcr_sub = 0; ne_sub = 0; vc_sub = 0

filters = {
    "product_type": {  
        "property": "/type",
        "operator": "=",
        "values": [] # FCR / VC / EIA (roadmap)
        },
    "account_number": {
        "property": "/account/accountNumber",
        "operator": "=",
        "values": []
        },
    "eia_connection_type": {
        "property": "/service/connection/type",
        "operator": "=",
        "values": ["IA_C"]
        },
    "eia_bandwidth": {
        "property": "/service/connection/aSide/accessPoint/port/physicalPort/speed",
        "operator": "=",
        "values": []
        },
    "eia_port_qty": {
        "property": "/service/connection/aSide/accessPoint/port/physicalPortQuantity",
        "operator": "=",
        "values": [1]
        },
    "eia_redundancy_type": {
        "property": "/service/type",
        "operator": "=",
        "values": ["SINGLE_PORT"]
        },
    "eia_billing_type": {
        "property": "/service/billing",
        "operator": "=",
        "values": ["BURST_BASED"]
        },
    "eia_usecase": {
        "property": "/service/useCase",
        "operator": "=",
        "values": ["MAIN"]
        },
    "eia_ap_type": {
        "property": "/service/connection/aSide/accessPoint/type",
        "operator": "=",
        "values": []
        },
    "eia_location": {
        "property": "/service/connection/aSide/accessPoint/location/ibx",
        "operator": "=",
        "values": []
        },
    "eia_bandwidth": {
        "property": "/service/minBandwidthCommit",
        "operator": "=",
        "values": []
        },
    "eia_ip_block": {
        "property": "/ipBlock/type",
        "operator": "=",
        "values": ["IA_IP_BLOCK"]
        },
    "eia_ip_location": {
        "property": "/ipBlock/location/ibx",
        "operator": "=",
        "values": []
        },
    "eia_ip_prefix_length": {
        "property": "/ipBlock/ipv4/prefixLength",
        "operator": "=",
        "values": []
        },
    "fcr_location": {
        "property": "/router/location/metroCode",
        "operator": "=",
        "values": []
        },
    "fcr_package": {
        "property": "/router/package/code",
        "operator": "IN",
        "values": []
        },
    "vc_type": {   
        "property": "/connection/type",
        "operator": "=",
        "values": [] # EVPL_VC, EPL_VC, IPWAN_VC, IP_VC, ACCESS_EPL_VC, EVPLAN_VC, EPLAN_VC, EIA_VC, IA_VC, EC_VC
        },
    "term_length": {
        "property": "/termLength",
        "operator": "=",
        "values": []
    },
    "bandwidth": {   
        "property": "/connection/bandwidth",
        "operator": "IN",
        "values": [] # NUMBER
        },
    "a_side_ap_type": {   
        "property": "/connection/aSide/accessPoint/type",
        "operator": "=",
        "values": [] # CLOUD_ROUTER / COLO / VD
        },
    "a_side_location": {       
        "property": "/connection/aSide/accessPoint/location/metroCode",
        "operator": "=",
        "values": [] # METRO CODE
        },
    "a_side_port_uuid": {
        "property": "/connection/aSide/accessPoint/port/uuid",
        "operator": "=",
        "values": []
        },
    "buyout": {   
        "property": "/connection/aSide/accessPoint/port/settings/buyout",
        "operator": "=",
        "values": [] # TRUE / FALSE
        },
    "z_side_location": {   
        "property": "/connection/zSide/accessPoint/location/metroCode",
        "operator": "=",
        "values": [] # METRO CODE
        },
    "z_side_ap_type": {
        "property": "/connection/zSide/accessPoint/type",
        "operator": "=",
        "values": [] # COLO / SP / NETWORK / CHAINGROUP???
        },
    "z_side_sp_uuid": {
        "property": "/connection/zSide/accessPoint/profile/uuid",
        "operator": "=",
        "values": [] # STRING
        },
    "ntw_scope": {
        "property": "/connection/zSide/accessPoint/network/scope",
        "operator": "=",
        "values": [] # LOCAL / REGIONAL / GLOBAL 
        }
    }

general_filter = [
    filters['a_side_ap_type'],
    filters['z_side_ap_type'],
    filters['product_type'],
    filters['vc_type'],
    filters['term_length'],
    filters['bandwidth'],
    ]
a_side_filter = {
    "port": [
        filters['a_side_location'],
        filters['buyout']
        ],
    "fcr": [
        filters['a_side_location']
        ],
    "vd": [
        filters['a_side_location']]
    }
z_side_filter = {
    "port": [
        filters['z_side_location']
        ],
    "vd": [
        filters['z_side_location']
        ],
    "sp": [
        filters['z_side_location'],
        filters['z_side_sp_uuid']
        ],
    "ntw": [
        filters['ntw_scope']
        ]
    }

token = None
url = "https://api.equinix.com/oauth2/v1/token"
# Read Client ID / Client Secret from variables section
with open(path, 'r') as tfplan:
    config = json.load(tfplan)
    client_id = config['variables']['client_id']['value']
    if client_id is None:
        client_id = input("Please provide your Fabric Client ID for authentication: ")
    client_secret = config['variables']['client_secret']['value']
    if client_secret is None:
        client_secret = input("Please provide your Fabric Client ID for authentication: ")
# prepare API Call
headers = {
    "content-type": "application/json"
    }
data = {
    "client_id": (client_id),
    "client_secret": (client_secret),
    "grant_type": "client_credentials",
    "password_encoding": "none"
    }
response = requests.post(url, headers=headers, data=json.dumps(data))
# Check the response
if response.status_code == 200:
    #global token
    token = (response.json()['access_token'])
else:
    print("Error:", response.status_code, response.text)
    print("Fehler liegt bei get_token!")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
    }

# ------------------------------------------------------------------------------------------------------
# Collect Assets from ../JSONs/tfplan.json

try:
    with open(path, 'r') as file:
        tfplan = json.load(file)
    
    resources = tfplan.get('planned_values', {}).get('root_module', {}).get('resources', [])
    tf_config = tfplan.get('configuration', {}).get('root_module', {}).get('resources', [])
    for resource in resources:
        resource_type = resource.get('type')
        resource_values = resource.get('values', {})
        resource_address = resource.get('address')
        
    
# ------------------------------------------------------------------------------------------------------
# Collect FCRs
        if resource_type == 'equinix_fabric_cloud_router':
            print(line)
            data['type'] = resource_type
            name = resource_values.get('name')
            packages = resource_values.get('package', [])
            locations = resource_values.get('location', [])
            orders = resource_values.get('order', [])
            fcr = fcr + 1
            assets = assets + 1 
            
            if packages and locations and orders:
                package_code = packages[0].get('code')
                metro = locations[0].get('metro_code')
                term_length = orders[0].get('term_length')
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = {
                    "filter": { 
                        "and": [
                            {
                                "property": "/type",
                                "operator": "=",
                                "values": ["CLOUD_ROUTER_PRODUCT"]
                                },
                            {
                                "property": "/router/location/metroCode",
                                "operator": "=",
                                "values": [metro]
                                },
                                {
                                "property": "/termLength",
                                "operator": "IN",
                                "values": [term_length]
                                },
                            {
                                "property": "/router/package/code",
                                "operator": "IN",
                                "values": [package_code]
                                }
                            ]
                        }
                    }

                    # Make the POST request
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    fcr_sub = fcr_sub + cost
                    print("|", f"Fabric Cloud Router {fcr} ({name}) in {metro}:".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("Error:", response.status_code, response.text)

# ------------------------------------------------------------------------------------------------------
# Collect VIRTUAL DEVICEs
        elif resource_type == 'equinix_network_device': 
            print(line)
            type = resource_type
            name = resource_values.get('hostname')
            account_number = resource_values.get('account_number')
            software_package = resource_values.get('package_code')
            vendor_package = resource_values.get('type_code')
            metro_code = resource_values.get('metro_code')
            core_count = resource_values.get('core_count')
            term_length = resource_values.get('term_length')
            secondary_device = resource_values.get('secondary_device')
            
            ne = ne + 1
            assets = assets + 1 

            # Define the URL
            url = "https://api.equinix.com/ne/v1/prices"

            # Define the headers
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
                }

            # Define the search parameters
            params = {
                "accountNumer": account_number,
                "metro": metro_code,
                "core": core_count,
                "vendorPackage": vendor_package,
                "softwarePackage": software_package,
                "termLength": term_length
                }
            # Make the GET request
            response = requests.get(url, headers=headers, params=params)

            # Check the response
            if response.status_code == 200:
                currency = response.json()['primary']['currency']
                cost = float(CurrencyConverter().convert((response.json()['primary']['charges'][0]['monthlyRecurringCharges']), currency, local_currency))
                print("|", f"Cost for Virtual Device {ne} ({name}) in {metro_code}:".ljust(len(line) - 4), "|")
                print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                ne_sub = ne_sub + cost
                total = total + cost
            else:
                print("  --- Sorry, something went wrong! ---")
                print("Error:", response.status_code, response.text)
                
            if secondary_device:
                sec_account_number = secondary_device[0].get('account_number')
                sec_metro_code = secondary_device[0].get('metro_code')
                sec_name = secondary_device[0].get('hostname')
                
                ne = ne + 1
                assets = assets + 1

                # Define the URL
                url = "https://api.equinix.com/ne/v1/prices"

                # Define the headers
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                    }

                # Define the search parameters
                params = {
                    "accountNumer": sec_account_number,
                    "metro": sec_metro_code,
                    "core": core_count,
                    "vendorPackage": vendor_package,
                    "softwarePackage": software_package,
                    "termLength": term_length
                    }

                # Make the GET request
                response = requests.get(url, headers=headers, params=params)

                # Check the response
                if response.status_code == 200:
                    currency = response.json()['primary']['currency']
                    cost = float(CurrencyConverter().convert(((response.json()['primary']['charges'][0]['monthlyRecurringCharges'])), currency, 'EUR'))
                    print(line)
                    print("|", f"Virtual Device {ne} ({name}) in {sec_metro_code}:".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                    total = total + cost
                    ne_sub = ne_sub + cost
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# ------------------------------------------------------------------------------------------------------
# Collect VCs        
        if resource_type == 'equinix_fabric_connection':
            print(line)
            vc = vc + 1
            assets = assets + 1
            name = resource_values['name']

            filters['product_type']['values'] = ["VIRTUAL_CONNECTION_PRODUCT"]
            filters['vc_type']['values'] = [resource_values['type']]
            filters['term_length']['values'] = [str(resource_values['order'][0]['term_length'])]
            filters['bandwidth']['values'] = [str(resource_values.get('bandwidth'))]

            a_side = resource_values.get('a_side', []) 
            a_side_ap = a_side[0].get('access_point', [])
            filters['a_side_ap_type']['values'] = [a_side_ap[0].get('type')]

            z_side = resource_values.get('z_side', [])
            z_side_ap = z_side[0].get('access_point', [])
            filters['z_side_ap_type']['values'] = [z_side_ap[0]['type']]

# -------------------------------- Port to Port: --------------------------------
            if filters['a_side_ap_type']['values'] ==  ["COLO"] and filters['z_side_ap_type']['values'] ==  ["COLO"]:  
# A-Side
                a_side_port_uuid = a_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{a_side_port_uuid}"
                response = requests.get(url, headers = headers)

                filters['a_side_location']['values'] = [response.json()['location']['metroCode']]              
                filters['buyout']['values'] = [(str(response.json()['settings']['buyout']).lower())]
# Z-Side    
                z_side_port_uuid = z_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{z_side_port_uuid}"
                response = requests.get(url, headers = headers)
                filters['z_side_location']['values'] = [response.json()['location']['metroCode']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['port'] + z_side_filter['port']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                        currency = response.json()['data'][0]['currency']
                        cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                        vc_sub = vc_sub + cost
                        total = total + cost
                        print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                        print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# --------------------------------- Port to SP: ---------------------------------           
            elif filters['a_side_ap_type']['values'] ==  ["COLO"] and filters['z_side_ap_type']['values'] ==  ["SP"]:  
# A-Side
                a_side_port_uuid = a_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{a_side_port_uuid}"
                response = requests.get(url, headers = headers)
                
                filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                filters['buyout']['values'] = [(str(response.json()['settings']['buyout']).lower())]
# Z-Side
                filters['z_side_sp_uuid']['values'] = [z_side_ap[0]['profile'][0]['uuid']]
                filters['z_side_location']['values'] = [z_side_ap[0]['location'][0]['metro_code']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['port'] + z_side_filter['sp']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# ------------------------------ Port to Network: -------------------------------
            elif filters['a_side_ap_type']['values'] ==  ["COLO"] and filters['z_side_ap_type']['values'] ==  ["NETWORK"]:  
# A-Side
                a_side_port_uuid = a_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{a_side_port_uuid}"
                response = requests.get(url, headers = headers)
                filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                filters['buyout']['values'] = [str(response.json()['settings']['buyout']).lower()]
# Z-Side
                network = z_side_ap[0]['network'][0]
                if network.get('uuid') is not None:
                    ntw_uuid = network['uuid']
                    url = f"https://api.equinix.com/fabric/v4/networks/{ntw_uuid}"
                    response = requests.get(url, headers = headers)
                    filters['ntw_scope']['values'] = [str(response.json()['scope'])]
                else:
                    vc_address = resource_address
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        
                        if config.get('address') == vc_address:
                            ntw_address = config_expressions['z_side'][0]['access_point'][0]['network'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource.get('address') == ntw_address:
                                    resource_values = resource.get('values', {})
                                    filters['ntw_scope']['values'] = [str(resource_values.get('scope'))]
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['port'] + z_side_filter['ntw']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# -------------------------------- FCR to Port: ---------------------------------
            elif filters['a_side_ap_type']['values'] == ["CLOUD_ROUTER"] and filters['z_side_ap_type']['values'] == ["COLO"]:
# A-Side
                router = a_side_ap[0]['router'][0]
                if router == {}:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            fcr_address = config_expressions['a_side'][0]['access_point'][0]['router'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == fcr_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    fcr_uuid = router['uuid']  
                    url = f"https://api.equinix.com/fabric/v4/routers/{fcr_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                    else:
                        print("  --- Sorry, something went wrong! ---")
                        print("Error:", response.status_code, response.text)
# Z-Side
                z_side_port_uuid = z_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{z_side_port_uuid}"
                response = requests.get(url, headers = headers)
                filters['z_side_location']['values'] = [response.json()['location']['metroCode']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['fcr'] + z_side_filter['port']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# --------------------------------- FCR to VD: ----------------------------------
            elif filters['a_side_ap_type']['values'] ==  ["CLOUD_ROUTER"] and filters['z_side_ap_type']['values'] ==  ["VD"]:  
# A-Side
                router = a_side_ap[0]['router'][0]
                vc_address = resource.get('address')
                if router == {}:
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            fcr_address = config_expressions['a_side'][0]['access_point'][0]['router'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == fcr_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                                    #print("test 552")
                else:            
                    fcr_uuid = router['uuid']  
                    url = f"https://api.equinix.com/fabric/v4/routers/{fcr_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                        #print("test 559")
                    else: 
                        print("  Error:", response.status_code, response.text)
# Z-Side
                #print(z_side_ap)
                vd = z_side_ap[0]['virtual_device'][0]
                vd_uuid = vd.get('uuid')
                if vd_uuid is not None:
                    url = f"https://api.equinix.com/ne/v1/devices/{vd_uuid}"
                    response = requests.get(url, headers = headers)
                    filters['z_side_location']['values'] = [str(response.json()['metroCode'])]
                else:
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            vd_references = config_expressions['z_side'][0]['access_point'][0]['virtual_device'][0]['uuid']['references']
                            vd_address = vd_references[len(vd_references) - 1]
                            if any("second" in vd_ref for vd_ref in vd_references):
                                for resource in resources:
                                        if resource.get('address') == vd_address:
                                            filters['z_side_location']['values'] = [str(resource['values']['secondary_device'][0]['metro_code'])]
                            else:
                                for resource in resources:
                                    if resource_address == vd_address:
                                        filters['z_side_location']['values'] = [str(resource['values']['metro_code'])]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['fcr'] + z_side_filter['vd']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                        currency = response.json()['data'][0]['currency']
                        cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                        total = total + cost
                        vc_sub = vc_sub + cost
                        print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                        print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# ------------------------------ FCR to Network: --------------------------------
            elif filters['a_side_ap_type']['values'] ==  ["CLOUD_ROUTER"] and filters['z_side_ap_type']['values'] ==  ["NETWORK"]:  
# A-Side
                router = a_side_ap[0]['router'][0]
                if router == {}:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            fcr_address = config_expressions['a_side'][0]['access_point'][0]['router'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource_address == fcr_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    fcr_uuid = router['uuid']  
                    url = f"https://api.equinix.com/fabric/v4/routers/{fcr_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                    else:
                        print("  --- Sorry, something went wrong! ---")
                        print("  Error:", response.status_code, response.text)

# Z-Side
                network = z_side_ap[0]['network'][0]
                if network.get('uuid') is not None:
                    ntw_uuid = network['uuid']
                    url = f"https://api.equinix.com/fabric/v4/networks/{ntw_uuid}"
                    response = requests.get(url, headers = headers)
                    filters['ntw_scope']['values'] = [str(response.json()['scope'])]
                else:
                    vc_address = resource_address
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        
                        if config.get('address') == vc_address:
                            ntw_address = config_expressions['z_side'][0]['access_point'][0]['network'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource.get('address') == ntw_address:
                                    resource_values = resource.get('values', {})
                                    filters['ntw_scope']['values'] = [str(resource_values.get('scope'))]
                                    
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['fcr'] + z_side_filter['ntw']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                        currency = response.json()['data'][0]['currency']
                        cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                        total = total + cost
                        vc_sub = vc_sub + cost
                        print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                        print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print(response.status_code, response.text)

# --------------------------------- FCR to SP: ----------------------------------
            elif filters['a_side_ap_type']['values'] ==  ["CLOUD_ROUTER"] and filters['z_side_ap_type']['values'] ==  ["SP"]:
# A-Side
                router = a_side_ap[0]['router'][0]
                if router == {}:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            fcr_address = config_expressions['a_side'][0]['access_point'][0]['router'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == fcr_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    fcr_uuid = router['uuid']  
                    url = f"https://api.equinix.com/fabric/v4/routers/{fcr_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['location']['metroCode']]
                    else: 
                        print(response.status_code, response.text)
# Z-Side
                filters['z_side_sp_uuid']['values'] = [z_side_ap[0]['profile'][0]['uuid']]
                filters['z_side_location']['values'] = [z_side_ap[0]['location'][0]['metro_code']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['fcr'] + z_side_filter['sp']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# -------------------------------- VD to Port: ---------------------------------
            elif filters['a_side_ap_type']['values'] == ["VD"] and filters['z_side_ap_type']['values'] == ["COLO"]:
# A-Side
                vd_uuid = a_side_ap[0]['virtual_device'][0]['uuid']
                if vd_uuid is None:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            vd_address = config_expressions['a_side'][0]['access_point'][0]['virtual_device'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == vd_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    url = f"https://api.equinix.com/ne/v1/devices/{vd_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['metroCode']]
                    else:
                        print("  --- Sorry, something went wrong! ---")
                        print("Error:", response.status_code, response.text)
#Z-Side
                z_side_port_uuid = z_side_ap[0]['port'][0]['uuid']
                url = f"https://api.equinix.com/fabric/v4/ports/{z_side_port_uuid}"
                response = requests.get(url, headers = headers)
                filters['z_side_location']['values'] = [response.json()['location']['metroCode']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['vd'] + z_side_filter['port']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print("  Error:", response.status_code, response.text)

# --------------------------------- VD to Network: ----------------------------------
            elif filters['a_side_ap_type']['values'] == ["VD"] and filters['z_side_ap_type']['values'] == ["NETWORK"]:
# A-Side
                vd_uuid = a_side_ap[0]['virtual_device'][0]['uuid']
                if vd_uuid is None:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            vd_address = config_expressions['a_side'][0]['access_point'][0]['virtual_device'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == vd_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    url = f"https://api.equinix.com/ne/v1/devices/{vd_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['metroCode']]
                    else:
                        print("  --- Sorry, something went wrong! ---")
                        print("Error:", response.status_code, response.text)
# Z-Side
                network = z_side_ap[0]['network'][0]
                if network.get('uuid') is not None:
                    ntw_uuid = network['uuid']
                    url = f"https://api.equinix.com/fabric/v4/networks/{ntw_uuid}"
                    response = requests.get(url, headers = headers)
                    filters['ntw_scope']['values'] = [str(response.json()['scope'])]
                else:
                    vc_address = resource_address
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        
                        if config.get('address') == vc_address:
                            ntw_address = config_expressions['z_side'][0]['access_point'][0]['network'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource.get('address') == ntw_address:
                                    resource_values = resource.get('values', {})
                                    filters['ntw_scope']['values'] = [str(resource_values.get('scope'))]
                                    
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['vd'] + z_side_filter['ntw']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                        currency = response.json()['data'][0]['currency']
                        cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                        total = total + cost
                        vc_sub = vc_sub + cost
                        print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                        print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else:
                    print("  --- Sorry, something went wrong! ---")
                    print(response.status_code, response.text)

# ------------------------------- VD to SP: -------------------------------
            elif filters['a_side_ap_type']['values'] == ["VD"] and filters['z_side_ap_type']['values'] == ["SP"]:
# A-Side
                vd_uuid = a_side_ap[0]['virtual_device'][0]['uuid']
                if vd_uuid is None:
                    vc_address = resource.get('address')
                    for config in tf_config:
                        config_expressions = config.get('expressions', {})
                        if config.get('address') == vc_address:
                            vd_address = config_expressions['a_side'][0]['access_point'][0]['virtual_device'][0]['uuid']['references'][1]
                            for resource in resources:
                                if resource['address'] == vd_address:
                                    filters['a_side_location']['values'] = [str(resource['values']['location'][0]['metro_code'])]
                else:            
                    url = f"https://api.equinix.com/ne/v1/devices/{vd_uuid}"
                    response = requests.get(url, headers = headers)
                    if response.status_code == 200:
                        filters['a_side_location']['values'] = [response.json()['metroCode']]
                    else:
                        print("  --- Sorry, something went wrong! ---")
                        print("Error:", response.status_code, response.text)
# Z-Side
                filters['z_side_sp_uuid']['values'] = [z_side_ap[0]['profile'][0]['uuid']]
                filters['z_side_location']['values'] = [z_side_ap[0]['location'][0]['metro_code']]
                
                url = "https://api.equinix.com/fabric/v4/prices/search"
                data = { "filter": {"and": general_filter + a_side_filter['fcr'] + z_side_filter['sp']}}
                response = requests.post(url, headers=headers, data=json.dumps(data, indent=2))
                if response.status_code == 200:
                    currency = response.json()['data'][0]['currency']
                    cost = float(CurrencyConverter().convert((response.json()['data'][0]['charges'][0]['price']), currency, local_currency))
                    total = total + cost
                    vc_sub = vc_sub + cost
                    print("|", f"{resource_values['type']} Fabric VC {vc} ({name}):".ljust(len(line) - 4), "|")
                    print("|", (f"{cost:.2f} " + local_currency).rjust(len(line) - 4), "|")
                else: 
                    print(response.status_code, response.text)

# ----------------------------------------------- WRAP-UP ----------------------------------------------

    print(line)
    print()
    print(f"Successfully processed", assets, "resources")
    print()
    
    if fcr_sub != 0:
        print(f"Costs for Fabric Cloud Routers: | {fcr_sub:.2f} {local_currency}")
    if ne_sub != 0:
        print(f"Costs for Network Edge Devices: | {ne_sub:.2f} {local_currency}")
    if vc_sub != 0:
        print(f"Costs for Fabric VCs:           | {vc_sub:.2f} {local_currency}")
    print()
    print(f"Total Cost of project:          | {total:.2f} {local_currency}")

        
except FileNotFoundError:
    print("Error: tfplan.json file not found")
except json.JSONDecodeError:
    print("Error: Invalid JSON format in tfplan.json")
except Exception as e:
    print(f"An error occurred: {str(e)}")