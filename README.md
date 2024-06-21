# OMB_M-21-31_Utils_for_Splunk

# Table of Contents:
* Purpose
* Compatibility
* Installation Instructions
  * Custom capability & role
  * Dependencies
* Upgrade Instructions
* Support
* Dashboards & Screenshots

# Purpose:
Splunk dashboards and utilities for tracking OMB M-21-31 compliance at a high-level. 

This is the final product of what was presented during the Splunk .conf23 session "_SEC1817B - How Centers for Disease Control (CDC) Leverages the Power of OMB M-21-31 for More Than Just Compliance_" by Andrew Dayton & Thomas Brookshire ([recording](https://conf.splunk.com/files/2023/recordings/SEC1817B.mp4), [slides](https://conf.splunk.com/files/2023/slides/SEC1817B.pdf)). 

What this app does NOT do:
1. Make your organization compliant,
2. Automatically analyze your data to estimate current compliance,
3. Display compliance on an asset-level

What this app DOES do:
1. Help perform a much faster assessment at a very high-level,
2. Identify gaps,
3. More efficient reporting and analysis,
5. Provide really awesome features after a deep dive is performed (e.g., the dashboard `Auto. Data Inventory`).

# Compatibility:
* Splunk Enterprise, Splunk Cloud, Splunk GovCloud
* Platform Version: 9.2, 9.1, 9.0

# Installation Instructions:
Either play around with the dashboards using the `omb-m2131-status-demo` lookup or create your own status lookup for tracking by using the `Getting Started` dashboard. 

### Custom capability & role
Creating a new status lookup with the `Getting Started` dashboard or `m2131getstatus` custom search command, will require the user to have the `omb_m2131_create_status_lookup` custom capability. This capability is assigned to the `omb_m2131_maintainer` and `admin` roles by default. The dashboard was intentionally configured to be visible to users even though they may not have the capability or role. Feel free to change that visibility as needed for your own environment.

## Dependencies:
These aren't necessarily needed for tracking compliance with this app. One or two dashboards or panels may not work without the "Network Diagram Viz", but neither of these apps are _technically_ needed for the basic functionality of this app to be available. They either make a task a little easier or grant the ability to use advanced functionality within this app (e.g., the `Gap Analysis` dashboard)

1. Splunk App for Lookup File Editing (aka "Lookup Editor") ([splunkbase](https://splunkbase.splunk.com/app/1724)) - For easily updating lookups within the Splunk UI
2. Network Diagram Viz ([splunkbase](https://splunkbase.splunk.com/app/4438))- For visualizations


# Upgrade Instructions:
## From app version 1.5.1 to 1.7.x
The version of the m2131 pdf lookup is different than the version of the app, as it should be. If upgrading the app from version 1.5.1 OR if your the status lookup is using the m2131 lookup version 1.2.3, then make sure you use the appropriate `omb-m2131-upgrade_status_lookup-from_123-to_140` macro. If upgrading a status lookup that includes a group name in the lookup definition name, then use the `omb-m2131-upgrade_status_lookup-from_123-to_140(1)` macro and specify the name of the lookup as the argument. See the `Macros` section in the dashboard `Knowledge Object Reference` for more information.

# Support:
Support is made on a best-effort basis. The only updates I intend on making to this app are for fixing bugs. I am currently the sole developer for this app and I've already spent a year of personal time on this app. I released it _way_ later than I anticipated all because of my own personal standards. I'm burnt out. I don't plan on adding any new features to this app, barring a wild hair. If you find a bug or logic issue, then please let me know or submit a pull request.


# Dashboards:

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

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/cc2faff3-18d8-46d1-8164-415388541dc2)


## Search Memo
Filter the OMB M-21-31 PDF extracted contents

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/7df5a6c4-3287-4802-9ffe-35332cefa0e8)


## Getting Started
![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/cb327760-cc04-4bab-a9fe-1d5e5f9b11da)

![image](https://github.com/tbrookshire/OMB_M-21-31_Utils_for_Splunk/assets/86690101/37f5935f-1c62-4c4a-9835-2b65e9038b8f)


## Dashboards Not Pictured:
1. `Knowledge Object Reference` - Helps guide the Splunk administrator on creating the lookup(s) needed for tracking OMB M-21-31 compliance progress with this app
2. `General Usage` -  Describes how to use this app for tracking OMB M-21-31 compliance progress.


