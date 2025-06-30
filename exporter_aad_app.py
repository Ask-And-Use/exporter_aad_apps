"""
Azure AD Application Credential Monitor

This module monitors Azure AD application credential expiration dates and exposes
them as Prometheus metrics. It helps prevent unexpected credential expirations by
providing visibility into remaining days before credentials expire.

Features:
- Lists Azure AD applications and their credentials using Microsoft Graph API
- Calculates remaining days until credential expiration
- Exposes metrics via Prometheus HTTP server
- Supports configuration via command line arguments or JSON config file
- Optional verbose output mode

Usage:
    python exporter_aad_app.py -t <tenant_id> -c <client_id> -s <client_secret>

Options:
    -h, --help          Show usage information
    -t, --tenant        Azure AD tenant ID
    -c, --client        Client ID for authentication
    -s, --secret        Client secret for authentication
    -p, --port          Port to run Prometheus HTTP server (default: 5001)
    -l, --listen        Address to listen on (default: 0.0.0.0)
    -t, --timeout       HTTP request timeout in seconds (default: 10)
    -v, --verbose       Enable verbose output

Metrics:
    azure_app_credential_days_remaining - Number of days before credential expires

Dependencies:
    - requests
    - msal
    - enforce_typing
    - prometheus_client
"""

from datetime import datetime, timezone
from getopt import getopt
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
from sys import exit as sys_exit
from typing import Dict, NoReturn

import requests
from enforce_typing import enforce_types
from msal import ConfidentialClientApplication
from prometheus_client import Gauge, generate_latest

app_credential_days_remaining = Gauge(
    "azure_app_credential_days_remaining",
    "Number of days remaining before Azure application credential expires",
    ["app_name", "app_id", "credential_id"],
)


@enforce_types
def usage():
    """
    Display usage information for the script and exit.

    This function prints out the command-line options and their descriptions,
    then exits with status code 2 (indicating improper usage).
    """

    print("Azure AD Application Credential Monitor")
    print("\nUsage:")
    print(
        "    python exporter_aad_app.py -t <tenant_id> -c <client_id> -s <client_secret>"
    )
    print("\nOptions:")
    print("    -h, --help          Show this usage information")
    print("    -t, --tenant        Azure AD tenant ID")
    print("    -c, --client        Client ID for authentication")
    print("    -s, --secret        Client secret for authentication")
    print("    -p, --port          Port to run Prometheus HTTP server (default: 5001)")
    print("    -l, --listen        Address to listen on (default: 0.0.0.0)")
    print("    -t, --timeout       HTTP request timeout in seconds (default: 10)")
    print("    -v, --verbose       Enable verbose output")
    sys_exit(2)


class SimpleHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP requests and monitors Azure Active Directory (AAD) applications.

    This class is designed to process HTTP requests and provide HTTP GET operations that
    output monitoring metrics in a format compatible with Prometheus. The metrics are generated
    based on Azure AD applications and credentials information retrieved via the Microsoft Graph
    API. These include expiration statuses of credentials associated with Azure AD applications.
    """

    def do_GET(self) -> NoReturn:
        """
        Handles HTTP GET requests and provides metrics response in plain text format.

        This method performs monitoring tasks related to Azure Active Directory (AAD) applications by invoking
        the `monitor_aad_applications` method. Once the monitoring process is completed, it sends an HTTP 200
        response and outputs the metrics data generated in Prometheus' text-based exposition format for monitoring.

        :returns: None
        """

        self.monitor_aad_applications()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        # self.end_headers()
        self.wfile.write(generate_latest())

    @enforce_types
    def monitor_aad_applications(self) -> NoReturn:
        """
        List Azure AD Applications and Enterprise Apps and monitor credential expiration.

        This function retrieves Azure AD applications and their credentials using the
        Microsoft Graph API and sets up metrics for credential expiration. Optionally,
        it can provide verbose output detailing the remaining days for credential
        expiration for apps.

        :return: None
        :rtype: None
        """

        try:
            app = ConfidentialClientApplication(
                client_id=config["client_id"],
                client_credential=config["client_secret"],
                authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
            )

            token_response = app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"]
            )

            applications = (
                requests.get(
                    "https://graph.microsoft.com/v1.0/applications",
                    headers={
                        "Authorization": f"Bearer {token_response['access_token']}",
                        "Content-Type": "application/json",
                    },
                    timeout=config["timeout"],
                )
                .json()
                .get("value", [])
            )

            for app in applications:
                if app.get("deletedDateTime", False) is None:
                    for cred in app.get("passwordCredentials", []):
                        current_time = datetime.now(timezone.utc)
                        end_date = datetime.fromisoformat(
                            cred.get("endDateTime", "").replace("Z", "+00:00")
                        )

                        remaining_days = (
                            end_date - current_time
                        ).total_seconds() / 86400

                        app_credential_days_remaining.labels(
                            app_name=app.get("displayName", "unknown"),
                            app_id=app.get("appId", "unknown"),
                            credential_id=cred.get("keyId", "unknown"),
                        ).set(remaining_days)

                        if config["verbose"]:
                            print(
                                f"{app.get(
                                    'displayName', 'unknown'
                                )} [{app.get('appId', 'unknown')}] => {remaining_days:.0f} days"
                            )
                        break

        except Exception as e:
            print(str(e))
            usage()


if __name__ == "__main__":

    try:
        opts, args = getopt(
            argv[1:],
            "hvt:c:s:f:p:l:t:",
            [
                "help",
                "tenant=",
                "client=",
                "secret=",
                "port=",
                "listen=",
                "timeout=",
                "verbose",
            ],
        )
    except Exception as e:
        print(str(e))
        print(usage)

    try:
        listen: str = "0.0.0.0"
        port: int = 5001

        config: Dict = {
            "tenant_id": None,
            "client_id": None,
            "client_secret": None,
            "verbose": False,
            "timeout": 10,
        }

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(usage)
                sys_exit()
            elif opt in ("-t", "--tenant"):
                config["tenant_id"] = str(arg)
            elif opt in ("-c", "--client"):
                config["client_id"] = str(arg)
            elif opt in ("-s", "--secret"):
                config["client_secret"] = str(arg)
            elif opt in ("-p", "--port"):
                port = int(arg)
            elif opt in ("-l", "--listen"):
                listen = str(arg)
            elif opt in ("-t", "--timeout"):
                config["timeout"] = int(arg)
            elif opt in ("-v", "--verbose"):
                config["verbose"] = True

        if None in config.values():
            raise Exception("Missing required configuration parameters.")

        server = HTTPServer((listen, port), SimpleHandler)
        print(f"Prometheus metrics server running on http://{listen}:{port}/metrics")
        server.serve_forever()

    except Exception as e:
        print(str(e))
        print(usage)
