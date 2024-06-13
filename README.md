# OMB_M-21-31_Utils_for_Splunk
Splunk dashboards and utilities for tracking compliance at a high-level with OMB M-21-31

# Purpose:
What this app does NOT do:
1. Make your organization compliant.
2. Automatically analyze your data to estimate current compliance.

What this app DOES do:
1. Help perform a much faster assessment at a very high-level,
2. Identify gaps,
3. More efficient reporting and analysis,
5. Provide really awesome features after a deep dive is performed (e.g., the dashboard `Auto. Data Inventory`).

# Installation Instructions
Either play around with the dashboards using the `omb-m2131-status-demo` lookup or create your own status lookup for tracking by using the `Getting Started` dashboard.

# Upgrade Instructions
## From app version 1.5.1 to 1.7.13
If upgrading the app from version 1.5.1 OR if your the status lookup is using the m2131 lookup version 1.2.3, then make sure you use the appropriate `omb-m2131-upgrade_status_lookup-from_123-to_140` macro. If upgrading a status lookup that includes a group name in the lookup definition name, then use the `omb-m2131-upgrade_status_lookup-from_123-to_140(1)` macro and specify the name of the lookup as the argument. See the `Macros` section in the dashboard `Knowledge Object Reference` for more information.

# Dashboards

## Breakdown
Helps organizations track OMB M-21-31 compliance progress at a high level and explore associated data.

### Breakdown - Overview
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/4910cde7-bb9f-4fcf-984c-55c89ac3df80)

### Breakdown - Categories
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/ce678b43-f426-40ce-a2b4-5297ba2e01ae)

### Breakdown - Gaps
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/837f4113-9a0d-48d6-b935-3ab099c2a5cd)

### Breakdown - Statistics
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/0bc14aa5-4898-4816-b5ed-606bb91d7fba)

### Breakdown - Validation
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/7bee9a74-9d07-46f0-b57d-02b86ae30de8)


## Auto. Data Inventory
_(Only works after performing a deep dive. See `Phase 2` on the `General Usage` dashboard for more info)_

Grants insight into the environment's data sources by automatically generating a data inventory from the queries documented during deep dives for each OMB M-21-31 check. The categories are based on the "log_category" field in the "omb-m2131" lookup, while the subcategories are based on a mix of the "required_data_category" and "required_data" fields, where appropriate.

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/c7e4f442-8d5c-43d9-9586-a571c1766e4d)

### Auto. Data Inventory - Drilldown
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/daa090fb-c1bf-4698-bec4-1aad4689d50b)



## Gap Analysis
Helps visualize the current state of compliance and areas that need improvement.

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/2fa94296-07e8-408b-bd00-485a05da241e)


## Search Memo
Filter the OMB M-21-31 PDF extracted contents

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/7df5a6c4-3287-4802-9ffe-35332cefa0e8)


## Getting Started
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/cb327760-cc04-4bab-a9fe-1d5e5f9b11da)

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/37f5935f-1c62-4c4a-9835-2b65e9038b8f)


## Dashboards Not Pictured:
1. `Knowledge Object Reference` - Helps guide the Splunk administrator on creating the lookup(s) needed for tracking OMB M-21-31 compliance progress with this app
2. `General Usage` -  Describes how to use this app for tracking OMB M-21-31 compliance progress.


