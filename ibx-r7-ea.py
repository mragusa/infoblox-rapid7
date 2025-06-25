#!/usr/bin/env python3
# TODO
# Fix duplicate r7 connection code
# Add logging for wapi.log output

import requests
import getpass
import sys

# import re
from rich.console import Console
from rich.table import Table
import click
from click_option_group import optgroup

from requests.auth import HTTPBasicAuth

from ibx_sdk.logger.ibx_logger import init_logger
from ibx_sdk.nios.exceptions import WapiRequestException
from ibx_sdk.nios.gift import Gift

log = init_logger(
    logfile_name="wapi.log",
    logfile_mode="a",
    console_log=True,
    level="info",
    max_size=100000,
    num_logs=1,
)


@click.command()
@optgroup.group("Rapid7 Server Options")
@optgroup.option("--rapid7host", help="Rapid7 Server")
@optgroup.option("--rapid7user", help="Rapid7 User")
@optgroup.group("Rapid7 Actions")
@optgroup.option("--sites", is_flag=True, help="List Rapid7 Sites")
@optgroup.option("--templates", is_flag=True, help="List Rapid7 Scan Templates")
@optgroup.group("Infoblox Grid Options")
@optgroup.option("--grdmgr", help="Infoblox Grid Master")
@optgroup.option("--grdusr", help="Infoblox Grid User")
@optgroup.group("Infoblox Actions")
@optgroup.option("--ea", is_flag=True, help="List Infoblox R7 Extensible Attributes")
@optgroup.group("Infoblox Creation Actions")
@optgroup.option(
    "--create", is_flag=True, help="Create Infoblox R7 Extensible Attributes"
)
@optgroup.option(
    "--sync",
    is_flag=True,
    help="Sync R7 Sites and Templates with Infoblox on EA creation",
)
def main(rapid7host, rapid7user, grdmgr, grdusr, sites, templates, ea, create, sync):
    if ea:
        get_ibx_ea(ibx_conn(grdmgr, grdusr))

    if sites:
        r7_sites = get_sites(rapid7host, rapid7user)
        if r7_sites:
            print(f"Retrieved {len(r7_sites)} sites")
            display_r7_sites(r7_sites)
        else:
            print("Rapid7 Sites not found")

    if templates:
        scan_templates = get_scan_templates(rapid7host, rapid7user)
        if scan_templates:
            print(f"Retrieved {len(scan_templates)} templates")
            display_r7_templates(scan_templates)
        else:
            print("Rapid7 Scan Templates not found")

    if create:
        create_ibx_ea(ibx_conn(grdmgr, grdusr), sync, rapid7host, rapid7user)


# Function to get the list of get_sites
def get_sites(rapid7host, rapid7user):
    password = getpass.getpass("Enter Rapid7 Password: ")
    endpoint = f"https://{rapid7host}:3780/api/3/sites"
    try:
        # Send GET request with Basic Authentication
        response = requests.get(
            endpoint, auth=HTTPBasicAuth(rapid7user, password), verify=False
        )

        # Check if the request was successful
        if response.status_code == 200:
            sites = response.json()["resources"]
            return sites
        else:
            print(f"Failed to fetch sites. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_scan_templates(rapid7host, rapid7user):
    password = getpass.getpass("Enter Rapid7 Password: ")
    endpoint = f"https://{rapid7host}:3780/api/3/scan_templates"
    try:
        # Send GET request with Basic Authentication
        response = requests.get(
            endpoint, auth=HTTPBasicAuth(rapid7user, password), verify=False
        )

        # Check if the request was successful
        if response.status_code == 200:
            sites = response.json()["resources"]
            return sites
        else:
            print(f"Failed to fetch sites. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def ibx_conn(grdmgr, username):
    wapi = Gift()
    wapi.grid_mgr = grdmgr
    password = getpass.getpass("Enter Infoblox Password: ")
    try:
        wapi.connect(username=username, password=password)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    return wapi


def get_ibx_ea(wapi):
    table = Table(title="Rapid7 Extensible Attributes")
    table.add_column("Name", justify="center", style="green")
    table.add_column("Comment", justify="center", style="white", no_wrap=True)
    table.add_column("Default Value", justify="center", style="green")
    # table.add_column("Allowed Object Types", justify="center", style="white")
    table.add_column("Flags", justify="center", style="green")
    try:
        ea = wapi.get(
            "extensibleattributedef",
            params={
                "_return_fields": [
                    "name",
                    "comment",
                    "default_value",
                    "allowed_object_types",
                    "flags",
                ]
            },
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    if ea.status_code == 200:
        grid_ea = ea.json()
        for e in grid_ea:
            if e["name"].startswith("R7"):
                table.add_row(
                    str(e["name"]),
                    str(e["comment"]),
                    str(e["default_value"]),
                    str(e["flags"]),
                )
    else:
        print(ea.status_code, ea.text)
    console = Console()
    console.print(table)


def create_ibx_ea(wapi, sync, rapid7host, rapid7user):
    rapid7_ea = [
        {
            "name": "R7_AddByHostname",
            "comment": "Defines if a host should be synced with Rapid7. The hostname should be resolvable by Rapid7",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "false",
        },
        {
            "name": "R7_LastScan",
            "comment": "Contains a date when an asset was last scanned by a request from Infoblox. This is updated automatically by Rapid7",
            "type": "DATE",
            "flags": "AI",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
        },
        {
            "name": "R7_NetToSite",
            "comment": "Defines if a network should be added to a site. If R7_NetToSite is false but R7_Sync is true, R7_SiteID will be updated",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "true",
            "allowed_object_types": ["Network", "IPv6Network"],
        },
        {
            "name": "R7_RangeToSite",
            "comment": "Defines if a DHCP range should be added to a Rapid7 Site.",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "true",
            "allowed_object_types": [
                "DhcpRange",
                "IPv6DhcpLease",
                "FixedAddress",
                "DhcpLease",
                "IPv6DhcpRange",
                "IPv6FixedAddress",
            ],
        },
        {
            "name": "R7_ScanOnAdd",
            "comment": "Defines if an asset should be scanned immediately after creation",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "true",
        },
        {
            "name": "R7_ScanOnEvent",
            "comment": "Defines if an asset should be scanned if RPZ or DNS Tunneling events are triggered",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "false",
        },
        {
            "name": "R7_ScanTemplate",
            "comment": "Defines which Rapid7 Nexpose/InsightVM template should be used for scanning an asset",
            "flags": "AIL",
            "type": "ENUM",
            "list_values": [{"value": "Discovery Scan"}],
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "Discovery Scan",
        },
        {
            "name": "R7_Site",
            "comment": "Defines a Rapid7 Site Name",
            "type": "ENUM",
            "flags": "AIL",
            "list_values": [{"value": "Test-Site"}],
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "Test-Site",
        },
        {
            "name": "R7_SiteID",
            "comment": "Contains an internal site ID. Updated automatically. If the value was inherited from a top level, templates will bypass a few steps retrieving this ID.",
            "type": "INTEGER",
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
        },
        {
            "name": "R7_Sync",
            "comment": "Defines if an object should be synced with Rapid7 Nexpose",
            "type": "ENUM",
            "list_values": [{"value": "true"}, {"value": "false"}],
            "flags": "AIL",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
            "default_value": "true",
        },
        {
            "name": "R7_SyncedAt",
            "comment": "Contains date/time when the object was synchronized, updated by the assets management template",
            "type": "DATE",
            "flags": "AI",
            "descendants_action": {
                "option_with_ea": "INHERIT",
                "option_delete_ea": "REMOVE",
                "option_without_ea": "INHERIT",
            },
        },
    ]

    if sync:
        rapid7_ea[6]["list_values"].pop(0)
        rapid7_ea[7]["list_values"].pop(0)
        r7_templates = get_scan_templates(rapid7host, rapid7user)
        if r7_templates:
            for t in r7_templates:
                rapid7_ea[6]["list_values"].append({"value": t["name"]})
            rapid7_ea[6]["default_value"] = rapid7_ea[6]["list_values"][0]["value"]
        else:
            print("Rapid7 Templates not found")

        r7_sites = get_sites(rapid7host, rapid7user)
        if r7_sites:
            for s in r7_sites:
                rapid7_ea[7]["list_values"].append({"value": s["name"]})
            rapid7_ea[7]["default_value"] = rapid7_ea[7]["list_values"][0]["value"]
        else:
            print("Rapid7 Sites not configured")

    for r in rapid7_ea:
        try:
            r7ea = wapi.post("extensibleattributedef", json=r)
            if r7ea.status_code != 201:
                print(r7ea.status_code, r7ea.text)
            else:
                print(r7ea.json())
        except WapiRequestException as err:
            print(err)


def display_r7_sites(r7_sites):
    table = Table(title="Rapid7 Sites")
    table.add_column("Site Name", justify="center")
    table.add_column("Site ID", justify="center")
    for s in r7_sites:
        table.add_row(s["name"], str(s["id"]))
    console = Console()
    console.print(table)


def display_r7_templates(scan_templates):
    table = Table(title="Rapid7 Templates")
    table.add_column("Template Name", justify="center")
    table.add_column("Description", justify="center")
    for t in scan_templates:
        table.add_row(t["name"], t["description"])
    console = Console()
    console.print(table)


# Main script
if __name__ == "__main__":
    main()
