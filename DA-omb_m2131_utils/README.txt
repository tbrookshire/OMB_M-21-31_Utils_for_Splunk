OMB M-21-31 - Utils

Author: Thomas Brookshire
Email: thomas.brookshire@protonmail.com
License: GPLv3

App Dependencies:
  These aren't necessarily needed for tracking compliance with this app. One or two dashboards or panels may not work without the "Network Diagram Viz", but neither of these apps are technically needed for the basic functionality of this app to be available. They either make a task a little easier or grant the ability to use advanced functionality within this app (e.g., the Gap Analysis dashboard)

  1. Splunk App for Lookup File Editing (aka "Lookup Editor") - For easily updating lookups within the Splunk UI
  2. Network Diagram Viz - For visualizations


Dashboards:
  OMB M-21-31 - Auto. Data Inventory
    Grants insight into the environment's data sources by automatically generating a data inventory from the queries documented during deep dives for each OMB M-21-31 check. The categories are based on the "log_category" field in the "omb-m2131" lookup, while the subcategories are based on a mix of the "required_data_category" and "required_data" fields, where appropriate.
  OMB M-21-31 - Breakdown
    Helps organizations track OMB M-21-31 compliance progress at a high level and explore associated data.
  OMB M-21-31 - General Usage
    Describes how to use this app for tracking OMB M-21-31 compliance progress.
  OMB M-21-31 - Getting Started
    Helps guide the Splunk administrator on creating the lookup(s) needed for tracking OMB M-21-31 compliance progress with this app
  OMB M-21-31 - Knowledge Object Reference
    Gives details on the lookups that come with the app and information about their fields.
  OMB M-21-31 - Search Memo
    Filter the OMB M-21-31 PDF extracted contents
