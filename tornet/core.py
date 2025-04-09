import requests
import time
import os
import signal as os_signal 

from .utils import (
    print_info, print_warning, print_error,
    check_command, run_command, is_systemd_running, GREEN, WHITE, RESET
)

TOR_SOCKS_PORT = 9050
TOR_SOCKS_HOST = '127.0.0.1'
IP_CHECK_URL = 'https://api.ipify.org' 
CONNECT_TIMEOUT = 10 

def _get_tor_session():
    """Creates a requests session configured for Tor."""
    session = requests.session()
    session.proxies = {
        'http': f'socks5h://{TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}', 
        'https': f'socks5h://{TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}'
    }
    return session

def is_tor_connectable():
    """Checks if we can connect to the Tor SOCKS port."""
    session = _get_tor_session()
    try:
        response = session.get(IP_CHECK_URL, timeout=CONNECT_TIMEOUT)
        response.raise_for_status()
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print_warning(f"Cannot connect to Tor SOCKS proxy at {TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}.")
        print_warning("Ensure Tor service is running and accessible.")
        return False
    except requests.exceptions.RequestException as e:
        print_warning(f"Error connecting through Tor: {e}")
        return False

def is_tor_available():
    """Checks if tor executable exists and if Tor seems connectable."""
    if not check_command("tor"):
        print_error("Tor executable not found. Please install Tor.")
        return False
    return is_tor_connectable()
def get_current_ip(use_tor=True):
    """
    Gets the current public IP address.
    If use_tor is True, attempts to use the Tor network.
    If Tor fails or use_tor is False, tries a direct connection.
    Returns the IP address string or None if unable to fetch.
    """
    ip = None
    if use_tor:
        session = _get_tor_session()
        try:
            print_info("Fetching IP address via Tor...")
            response = session.get(IP_CHECK_URL, timeout=CONNECT_TIMEOUT)
            response.raise_for_status()
            ip = response.text.strip()
            print_info(f"Current IP (via Tor): {WHITE}{ip}{GREEN}")
            return ip
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print_warning(f"Could not connect via Tor proxy ({TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}).")
        except requests.exceptions.RequestException as e:
            print_warning(f"Failed to get IP via Tor: {e}")
            

    
    if ip is None:
        print_info("Fetching IP address directly...")
        try:
            response = requests.get(IP_CHECK_URL, timeout=CONNECT_TIMEOUT)
            response.raise_for_status()
            ip = response.text.strip()
            print_info(f"Current IP (Direct): {WHITE}{ip}{GREEN}")
            return ip
        except requests.exceptions.RequestException as e:
            print_error(f"Failed to get IP directly: {e}")
            print_error("Check your internet connection.")
            return None
    return ip 


def request_new_ip():
    """
    Attempts to request a new IP address from Tor by reloading it.
    Returns the new IP address obtained via Tor, or None on failure.
    """
    print_info("Requesting new IP address from Tor...")
    reloaded = False


    if is_systemd_running():
        print_info("Attempting reload via systemctl...")
        result = run_command(["systemctl", "reload", "tor"])
        if result and result.returncode == 0:
            print_info("Tor reload signal sent via systemctl.")
            reloaded = True
        else:
            print_warning("systemctl reload tor failed or command not found. Trying pkill -HUP.")


    if not reloaded and check_command("pkill"):
        print_info("Attempting reload via pkill -HUP...")
        check_proc = run_command(["pgrep", "-x", "tor"], capture_output=True)
        if check_proc and check_proc.returncode == 0:
             result = run_command(["pkill", "-HUP", "tor"])
             if result and result.returncode == 0:
                 print_info("SIGHUP signal sent to Tor process(es).")
                 reloaded = True
             else:
                 print_warning("pkill -HUP tor command failed. Tor might not be running or insufficient permissions.")
        else:
            print_warning("Tor process not found running via pgrep. Cannot send HUP signal.")

    
    if not reloaded and check_command("service"):
         print_info("Attempting reload via service command...")
         result = run_command(["service", "tor", "reload"])
         if result and result.returncode == 0:
              print_info("Tor reload signal sent via service command.")
              reloaded = True
         else:
              print_warning("service tor reload failed or command not found.")

    if not reloaded:
        print_error("Failed to send reload signal to Tor using available methods.")
        print_warning("Ensure Tor is running and you have permissions.")
        return None

 
    print_info("Waiting for Tor to establish a new circuit (10 seconds)...")
    time.sleep(10)

    new_ip = get_current_ip(use_tor=True)
    if new_ip:
        print_info(f"Successfully changed IP to {WHITE}{new_ip}{GREEN}")
        return new_ip
    else:
        print_error("Failed to get a new IP address via Tor after reload.")
        return None