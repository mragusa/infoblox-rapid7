# infoblox-rapid7
A collection of tools, notes, and templates for integrating the Infoblox NIOS platform with Rapid7

## Overview
Summary of notes from Infoblox Rapid7 integration based on the [Infoblox Deployment Guide](https://insights.infoblox.com/resources-deployment-guides/infoblox-deployment-guide-outbound-api-integration-with-rapid7-nexpose)

## NIOS Ecosystem Templates

| Name | Purpose |
| --- | --- |
| `Rapid7_Nexpose_Login.json.txt` | Rapid7 Login Template |
| `Rapid7_Nexpose_Logout.json.txt` | Rapid7 Logout Template |
| `Rapid7_Nexpose_Assets.json.txt` | Rapid7 Assets Template |
| `Rapid7_Nexpose_Security.json.txt` | Rapid7 Security Templatae |
| `Rapid7_Nexpose_Session.json.txt` | Rapid7 Session Template |

## NIOS Rapid7 Tools
| Name | Description |
| --- | --- |
| `R7_create_EAs.php` | PHP script to create Infoblox Extensible Attributes |
| `ibx-r7-ea.py` | Python script to create Infoblox EA, retreive R7 Sites and templates |

## Infoblox User Permissions
* All Hosts - RW
* All DHCP v4/v6 Fixed Addresses and Reservations - RW
* All IPv4/IPv6 Networks - RW

## Rapid7 User Permissions
*	Specify Scan Targets
*	Start Unscheduled Scans
*	“Site Access” to Sites being used


## Rapid7 Extensible Attribute Notes 

> [!WARNING]
> R7_LastScan and R7_SyncedAt are updated by the assets management template. These extensible attributes should never be updated manually.

> [!CAUTION]
> DHCP ranges should not be synced with Rapid7 due to the amount of traffic that can potentially cause issues with rabbitmq. The parent network should be configured to sync instead.

* R7_AddByHostname adds Host records to R7 Site
* All attributes should be set with “Enable Inheritance”
* All attributes should be set as “recommended” except R7_SyncedAt and R7_LastScan

### Rapid7 Extensible Attribute Table
| Name | Default | Description | Type |
| --- | --- | --- | --- |
| `R7_AddByHostname` | False | Defines if a host should be synced with Rapid7 Nexpose  a hostname. The hostname should be resolvable by Nexpose | ENUM | 
| `R7_LastScan` | None | Contains a date when an asset was scanned last time by a request from Infoblox | DATE | 
| `R7_SyncedAt` | None | Contains date/time when the object was synchronized | DATE |
| `R7_NetToSite` | True | Defines if a network should be added to a site. | ENUM | 
| `R7_RangeToSite` | False | Defines if a range should be added to a site | ENUM | 
| `R7_ScanOnAdd` | True | Defines if an asset should be scanned immediately after creation | ENUM | 
| `R7_ScanOnEvent` | False | Defines if an asset should be scanned if RPZ or DNS Tunneling events are triggered | ENUM | 
| `R7_ScanTemplate` | <Scan Template> | Defines which Rapid7 Nexpose/ InsightVM scan template to use| ENUM |
| `R7_Sync` | True | Defines if an object should be synced with Rapid7 Nexpose | ENUM |
| `R7_Site` | <R7 Site> | Defines a Rapid7 Site Name | ENUM | 
| `R7_SiteID` | None | Contains an internal site ID | INTEGER |


## Script Details
### ibx-r7-ea.py
```
$ ./ibx-r7-ea.py --help
Usage: ibx-r7-ea.py [OPTIONS]

Options:
  Rapid7 Server Options:
    --rapid7host TEXT          Rapid7 Server
    --rapid7user TEXT          Rapid7 User
  Rapid7 Actions:
    --sites                    List Rapid7 Sites
    --templates                List Rapid7 Scan Templates
  Infoblox Grid Options:
    --grdmgr TEXT              Infoblox Grid Master
    --grdusr TEXT              Infoblox Grid User
  Infoblox Actions:
    --ea                       List Infoblox R7 Extensible Attributes
  Infoblox Creation Actions:
    --create                   Create Infoblox R7 Extensible Attributes
    --sync                     Sync R7 Sites and Templates with Infoblox on EA
                               creation
  --help                       Show this message and exit.
```

### Examples
#### Display Rapid7 Sites and Templates
```
./ibx-r7-ea.py --rapid7host 10.113.20.40 --rapid7user infoblox --templates
./ibx-r7-ea.py --rapid7host 10.113.20.40 --rapid7user infoblox --sites
```
#### Display NIOS Rapid7 Extensible Attributes
```
./ibx-r7-ea.py --grdmgr 192.168.1.2 --grdusr admin --ea
```
#### Create NIOS Extensible Attributes
```
./ibx-r7-ea.py --rapid7host 10.113.20.40 --rapid7user infoblox --create --grdmgr 192.168.1.2 --grdusr admin
```
#### Create NIOS Extensible Attributes and Sync Sites and Templates with Rapid7
```
./ibx-r7-ea.py --rapid7host 10.113.20.40 --rapid7user infoblox --create --grdmgr 192.168.1.2 --grdusr admin --sync
```

![Demo](infoblox-nios-rapid7.gif)
