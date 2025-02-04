# infoblox-rapid7
A collection of tools and templates for integrating the Infoblox NIOS platform to Rapid7

## NIOS Ecosystem Templates

| Name | Purpose |
| --- | --- |
| `Rapid7_Nexpose_Login.json.txt` | Rapid7 Login Template |
| `Rapid7_Nexpose_Logout.json.txt` | Rapid7 Logout Template |
| `Rapid7_Nexpose_Assets.json.txt` | Rapid7 Assets Template |
| `Rapid7_Nexpose_Security.json.txt` | Rapid7 Security Templatae ||
| `Rapid7_Nexpose_Session.json.txt` | Rapid7 Session Template |

| Name | Description |
| --- | --- |
| `R7_create_EAs.php` | PHP script to create Infoblox Extensible Attributes |
| `ibx-r7-ea.py` | Python script to create Infoblox EA, Retreive R7 Sites and Templates |

## Rapid7 Extensible Attribute Notes 

* R7_LastScan and R7_SyncedAt are updated by the assets management template
* R7_AddByHostname adds Host records to R7 Site
* R7 EAs should be created as recommended, with inheiritance enabled.

| Name | Description | Type |
| --- | --- | --- |
| `R7_AddByHostname` | Defines if a host should be synced with Rapid7 Nexpose  a hostname. The hostname should be resolvable by Nexpose | ENUM | 
| `R7_LastScan` | Contains a date when an asset was scanned last time by a request from Infoblox | DATE | 
| `R7_SyncedAt` | Contains date/time when the object was synchronized | DATE |
| `R7_NetToSite` | Defines if a network should be added to a site. | ENUM | 
| `R7_RangeToSite` | Defines if a range should be added to a site | ENUM | 
| `R7_ScanOnAdd` | Defines if an asset should be scanned immediately after creation | ENUM | 
| `R7_ScanOnEvent` | Defines if an asset should be scanned if RPZ or DNS Tunneling events are triggered | ENUM | 
| `R7_ScanTemplate` | Defines which Rapid7 Nexpose/ InsightVM scan template to use| ENUM |
| `R7_Sync` | Defines if an object should be synced with Rapid7 Nexpose | ENUM |
| `R7_Site` | Defines a Rapid7 Site Name | ENUM | 
| `R7_SiteID` | Contains an internal site ID | INTEGER |

