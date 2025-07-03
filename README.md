[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
        --timeout       HTTP request timeout in seconds (default: 10)
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
azure_app_credential_days_remaining{app_id="9f2312f7-4e77-47db-a53e-665f2cc4f3bc",app_name="Gateway-System",credential_id="130aa1d3-49df-4be3-8595-3bf65dc72ece",credential_name="ClientSecret"} 42.31322540811602
azure_app_credential_days_remaining{app_id="39702cd9-eb4f-4cc0-8138-d7ba2d006116",app_name="Web-Sync",credential_id="80a40502-d3e8-40f3-9872-0095b75479f5",credential_name="Certificate"} 782.3220381889447
azure_app_credential_days_remaining{app_id="82dfa503-a1c5-46a7-87a7-7a0871fed0f8",app_name="Backup-Prod",credential_id="34547559-e320-494d-bcc4-7515c4b61c99",credential_name="ServicePrincipal"} 287.1588045961993
azure_app_credential_days_remaining{app_id="2e6b63c2-a409-4e1d-abba-1a483d1ec878",app_name="Dashboard-API",credential_id="aecde791-19af-441f-8b32-403d6f02628b",credential_name="APIKey"} -37.173127599717
azure_app_credential_days_remaining{app_id="706ee4b2-84cf-4d5c-82a2-3335a5b9fffb",app_name="Monitor-Web-Central",credential_id="e52037fd-9078-4ab0-a9e2-65af22829180",credential_name="OAuth2Token"} 65.02065752834775
azure_app_credential_days_remaining{app_id="b111cdb5-ea49-469e-9b08-cf0e2c7e6ed6",app_name="Dashboard-Data-Enterprise",credential_id="befeda18-2dc5-474b-bb4c-a196c699da27",credential_name="SharedKey"} -275.11365602887275
azure_app_credential_days_remaining{app_id="5379fa19-b241-4cf9-93cd-420be72d7934",app_name="Data-Hub",credential_id="c02c41f1-d351-49d0-83e1-9d884481c27c",credential_name="SASToken"} 55.9209267782255
```

# Prometheus Scraping

```yaml
  - job_name: 'aad_app_exporter'
    scrape_interval: 600s
    scrape_timeout: 60s
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets: ['127.0.0.1:5001']
```    

# Grafana Dashboard

You should import the grafana_dahsboard.json file inside the deployement folders