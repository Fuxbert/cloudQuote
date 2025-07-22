# cloudQuote

This project will provide pricing information on Equinix Digital Infrastructure resources. In order to gain access to the Equinix API, which will eventually provide the cost, you will need active Equinix Fabric Client Credentials. Please visit https://docs.equinix.com/equinix-api/developer-settings for more information.

---

## Initial Problem:
Customers will not know the overall **cost of resources / infrastructure** deployed via Terraform, unless they do investigation or rebuild in Equinix Solution Builder in parallel.

Currently, _Equinix Solution Builder_ provides the cost, but not the deployment while _Terrform Provider Equinix_ will provide the deployment, but not the cost.

This project is set to close the gap until _Solution Builder_ will be enabled to transform a Design into breathing infrastructure.

### Current Version as of 07/21/2025
**What's in Scope?**
Project cloudQuote will provide cost for:
- Equinix Fabric Cloud Routers
- Equinix Network Edge Devices
- Equinix Fabric Virtual Connections:
  - Cloud Routers to 
    - Fabric Ports
    - Network Edge
    - Service Profiles (CSPs etc.)
    - Networks (IP-WAN)
  - Fabric Ports to
    - Fabric Port
    - Service Profiles
    - Networks (EVP-LAN / EP-LAN / E-Tree / EP-Tree)
  - Network Edge Devices to
    - Fabric Ports
    - Service Profiles
    - Networks (EVP-LAN)

**What's not?**
Currently, Project cloudQuote will neglect the following options:
- Equinix Internet Access (no resource in terraform available)
- Network Edge Device Linking Groups
- Equinix Fabric VC to / from Token

**The following prerequisites are to be met before the tool can be used:**
- Create Equinix Developer App / Client Credentials
- install terraform and create terraform script
- create tfplan file in JSON-format 
  (to do so, run following commands: 
  'terraform plan -out=tfplan.binary'
  'terraform show -json tfplan.binary > <path/to/tfplan.json>' 
  You will need to specify the location of the tfplan.json file)
- install Python in latest version



### Note:
The cost provided is bound to a specific billing account. Conditions may vary between different accounts, please contact your Equinix Account Executive for more details.

This project is of experimental nature and not maintained regularly.
Based on changes within Equinix terraform provider and API documentation, the project owner will keep the code up to date wherever possible. The result is **not** to be seen as an official / binding quotation

