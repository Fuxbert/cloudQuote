# cloudQuote

**cloudQuote** is a Python-based utility designed to provide **cost estimation** for infrastructure deployed via **Terraform** on the **Equinix Digital Services** platform.

While the **Equinix Solution Builder** offers pricing without deployment capabilities, and the **Equinix Terraform Provider** enables deployment without pricing, cloudQuote bridges that gap — allowing users to forecast infrastructure costs directly from their Terraform plans.

---

## 🚀 Project Purpose

Equinix customers often face a blind spot: understanding the cost of infrastructure provisioned via Terraform requires manually reconstructing the setup in Solution Builder. cloudQuote solves this by analyzing your Terraform JSON plan and querying the Equinix API for real-time pricing data.

---

## 📦 Currently Supported Resources (as of 2025-07-21)

cloudQuote calculates monthly pricing for:

### Equinix Fabric
- **Cloud Routers**
- **Virtual Connections**:
  - Cloud Router ➜ Fabric Port
  - Cloud Router ➜ Network Edge
  - Cloud Router ➜ Service Profile (CSP)
  - Cloud Router ➜ IP-WAN (Network)
  - Fabric Port ➜ Fabric Port
  - Fabric Port ➜ Service Profile
  - Fabric Port ➜ EVP-LAN / EP-LAN / E-Tree / EP-Tree
  - Network Edge ➜ Fabric Port / Service Profile / EVP-LAN

### Equinix Network Edge
- **Virtual Devices** (with or without secondary devices)

### Equinix Precision Time

---

## 🚫 Currently Out of Scope

The following are **not yet supported**:

- Equinix Internet Access (no Terraform resource available)
- Network Edge Device Linking Groups
- Fabric VCs to/from Token endpoints

---

## ⚙️ Prerequisites

Before using cloudQuote, ensure you have:

1. An active Equinix account with Fabric access
2. **Equinix API Client Credentials**  
   [📘 How to get them](https://docs.equinix.com/equinix-api/developer-settings)
3. **Terraform** installed and configured
4. A valid `tfplan` file in JSON format:
   ```bash
   terraform plan -out=tfplan.binary
   terraform show -json tfplan.binary > path/to/tfplan.json
5. Python 3.9+ installed

6. currencyconverter, requests, and other dependencies (see requirements.txt)

## 📌 Notes & Disclaimers

- Costs are **billing-account-specific**. For account-based pricing terms, contact your Equinix Account Executive.
- This tool is **experimental** and maintained on a best-effort basis.
- Pricing estimates provided by cloudQuote are **not binding** and should not be treated as an official quote.

---

## 📄 License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributions

Feedback, bug reports, and pull requests are welcome! Just note that cloudQuote is not an official Equinix product.

---

## 🙏 Acknowledgments

This tool builds on:

- [Equinix Fabric API](https://developer.equinix.com/docs)
- [Equinix Terraform Provider](https://registry.terraform.io/providers/equinix/equinix/latest/docs)
