# Description

Azure AD Application Credential Monitor

This module monitors Azure AD application credential expiration dates and exposes
them as Prometheus metrics. It helps prevent unexpected credential expirations by
providing visibility into remaining days before credentials expire.

# Features
- Lists Azure AD applications and their credentials using Microsoft Graph API
- Calculates remaining days until credential expiration
- Exposes metrics via Prometheus HTTP server
- Supports configuration via command line arguments or JSON config file
- Optional verbose output mode

# Setup

```
pip install -r requirements.txt
```

# Usage

## With script parameters

```
Usage:
    python exporter_aad_app.py -t <tenant_id> -c <client_id> -s <client_secret> [-v] [-p <port>] [-l <listen_addr>] [-t <timeout>]

Options:
    -h, --help          Show usage information
    -t, --tenant        Azure AD tenant ID
    -c, --client        Client ID for authentication
    -s, --secret        Client secret for authentication
    -p, --port          Port to run Prometheus HTTP server (default: 5001)
    -l, --listen        Address to listen on (default: 0.0.0.0)
    -t, --timeout       HTTP request timeout in seconds (default: 10)
    -v, --verbose       Enable verbose output
```

# Output example

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 461.0
python_gc_objects_collected_total{generation="1"} 19.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 38.0
python_gc_collections_total{generation="1"} 3.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="13",patchlevel="0",version="3.13.0"} 1.0
# HELP azure_app_credential_days_remaining Number of days remaining before Azure application credential expires
# TYPE azure_app_credential_days_remaining gauge
azure_app_credential_days_remaining{app_id="9f2312f7-4e77-47db-a53e-665f2cc4f3bc",app_name="Gateway-System",credential_id="130aa1d3-49df-4be3-8595-3bf65dc72ece"} 42.31322540811602
azure_app_credential_days_remaining{app_id="39702cd9-eb4f-4cc0-8138-d7ba2d006116",app_name="Web-Sync",credential_id="80a40502-d3e8-40f3-9872-0095b75479f5"} 782.3220381889447
azure_app_credential_days_remaining{app_id="82dfa503-a1c5-46a7-87a7-7a0871fed0f8",app_name="Backup-Prod",credential_id="34547559-e320-494d-bcc4-7515c4b61c99"} 287.1588045961993
azure_app_credential_days_remaining{app_id="2e6b63c2-a409-4e1d-abba-1a483d1ec878",app_name="Dashboard-API",credential_id="aecde791-19af-441f-8b32-403d6f02628b"} -37.173127599717
azure_app_credential_days_remaining{app_id="706ee4b2-84cf-4d5c-82a2-3335a5b9fffb",app_name="Monitor-Web-Central",credential_id="e52037fd-9078-4ab0-a9e2-65af22829180"} 65.02065752834775
azure_app_credential_days_remaining{app_id="b111cdb5-ea49-469e-9b08-cf0e2c7e6ed6",app_name="Dashboard-Data-Enterprise",credential_id="befeda18-2dc5-474b-bb4c-a196c699da27"} -275.11365602887275
azure_app_credential_days_remaining{app_id="5379fa19-b241-4cf9-93cd-420be72d7934",app_name="Data-Hub",credential_id="c02c41f1-d351-49d0-83e1-9d884481c27c"} 55.9209267782255
azure_app_credential_days_remaining{app_id="ad688161-de2e-4e1d-a7d4-8061cac3c9e0",app_name="Tool-Prod",credential_id="6430941b-51fd-40a5-a966-f8a4b314f2f8"} -116.83692924380989
azure_app_credential_days_remaining{app_id="0a00d27e-0b2c-4b7c-aa7a-ff2f98b5a0b1",app_name="Manager-Dev",credential_id="ef541ed5-a94f-4021-b760-66da4e675add"} 297.83924654815314
azure_app_credential_days_remaining{app_id="2f96067f-8595-4e4b-a0af-f2b3d363c0fc",app_name="Service-App",credential_id="bef99c66-bfaf-454c-9784-1d4c1b88b17c"} 108.84052783480239
azure_app_credential_days_remaining{app_id="72faf62b-26f6-4717-84f8-b7d9d813637a",app_name="Data-Enterprise",credential_id="cc41c658-2d05-485a-a793-8acbdd91509e"} 37.89300838502584
azure_app_credential_days_remaining{app_id="750104c9-86b4-4c8b-8d55-9f47b4b45639",app_name="Gateway-API-Assistant",credential_id="c0e7d2fa-d149-4892-b980-c819743b2617"} 249.4763479262262
azure_app_credential_days_remaining{app_id="4377aec6-8850-4505-b330-89303c4b3fab",app_name="Backup-Service-Cloud",credential_id="bf11d5bb-33b9-4916-a9f9-cb526f5256fd"} -125.63031161242071
```

# Grafana Dashboard

```
WIP
```