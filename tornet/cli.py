import argparse
import time
import signal
import sys
import os
import importlib.metadata
version = importlib.metadata.version('tornet')
from tornet.banner import print_banner
from tornet.core import get_current_ip, request_new_ip, is_tor_connectable
from tornet.utils import (
    print_info, print_warning, print_error,
    check_dependencies, check_command, run_command,
    GREEN, WHITE, RESET, RED
)

TOOL_NAME = "tornet" 

def change_ip_repeatedly(interval, count):
    """Handles the loop for changing IP addresses."""
    if not is_tor_connectable():
        print_error("Cannot proceed without a connectable Tor service.")
        return 

    if count == 0:
        print_info(f"Changing IP every {interval} seconds indefinitely. Press Ctrl+C to stop.")
        iteration = 0
        while True:
            iteration += 1
            print_info(f"--- Iteration {iteration} ---")
            new_ip = request_new_ip()
            if new_ip:
                print_info(f"New IP successfully obtained: {WHITE}{new_ip}{GREEN}")
            else:
                print_warning("Failed to obtain a new IP in this iteration.")
               
            print_info(f"Waiting {interval} seconds...")
            time.sleep(interval)
    else:
        print_info(f"Changing IP {count} times with {interval} seconds interval.")
        for i in range(count):
            print_info(f"--- Iteration {i + 1} of {count} ---")
            new_ip = request_new_ip()
            if new_ip:
                print_info(f"New IP successfully obtained: {WHITE}{new_ip}{GREEN}")
            else:
                print_warning("Failed to obtain a new IP in this iteration.")
                
            if i < count - 1:
                print_info(f"Waiting {interval} seconds...")
                time.sleep(interval)
        print_info("Finished requested IP changes.")

def stop_services():
    """Attempts to stop Tor and kills tornet processes."""
    print_info("Attempting to stop Tor service and related processes...")
    stopped_tor = False

    if check_command("systemctl"):
        print_info("Attempting to stop Tor via systemctl...")
        result = run_command(["systemctl", "stop", "tor"])
        if result and result.returncode == 0:
            print_info("Tor service stopped via systemctl.")
            stopped_tor = True
        else:
            print_warning("Failed to stop Tor via systemctl (maybe not running or permissions issue).")

    if not stopped_tor and check_command("service"):
        print_info("Attempting to stop Tor via service command...")
        result = run_command(["service", "tor", "stop"])
        if result and result.returncode == 0:
            print_info("Tor service stopped via service command.")
            stopped_tor = True
        else:
            print_warning("Failed to stop Tor via service command.")

    if check_command("pkill"):
        print_info("Attempting to kill remaining 'tor' processes...")
        run_command(["pkill", "-9", "-x", "tor"]) 
        run_command(["pkill", "-9", "-f", "tor"]) 
        
        check_proc = run_command(["pgrep", "-x", "tor"])
        if not check_proc or check_proc.returncode != 0:
            print_info("Tor processes killed or were not running.")
        else:
            print_warning("Could not kill all Tor processes.")

    if check_command("pkill"):
        print_info(f"Attempting to kill '{TOOL_NAME}' processes...")
        run_command(["pkill", "-f", TOOL_NAME])
        print_info(f"Sent kill signal to '{TOOL_NAME}' processes.")

    print_info(f"Stop sequence complete.")

_original_sigint_handler = signal.getsignal(signal.SIGINT)
_original_sigquit_handler = signal.getsignal(signal.SIGQUIT)
_original_sigterm_handler = signal.getsignal(signal.SIGTERM)

def signal_handler(sig, frame):
    print(f"\n{WHITE}[{RED}!{WHITE}]{RED} Signal {sig} received. Shutting down...{RESET}")
    print_info(f"{TOOL_NAME} process exiting.")
    signal.signal(signal.SIGINT, _original_sigint_handler)
    signal.signal(signal.SIGQUIT, _original_sigquit_handler)
    signal.signal(signal.SIGTERM, _original_sigterm_handler)
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)  
    signal.signal(signal.SIGQUIT, signal_handler) 
    signal.signal(signal.SIGTERM, signal_handler) 

    parser = argparse.ArgumentParser(
        description=f"{TOOL_NAME} - Automate IP address changes using Tor.",
        formatter_class=argparse.RawTextHelpFormatter 
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Time in seconds between IP change attempts (default: 60)'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Number of times to change the IP. Use 0 to run indefinitely (default: 10)'
    )
    parser.add_argument(
        '--ip',
        action='store_true',
        help='Display the current IP address (via Tor if possible) and exit'
    )
    parser.add_argument(
        '--stop',
        action='store_true',
        help='Attempt to stop Tor service and kill related processes'
    )
    
    try:
        import importlib.metadata
        version = importlib.metadata.version('tornet')
    except ImportError:
        from tornet import __version__ as version  # Add __version__ to __init__.py if needed
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {version}'
    )

    args = parser.parse_args()

    if not check_dependencies():
        sys.exit(1)

    # --- Action Handling ---
    if args.stop:
        stop_services()
        sys.exit(0)

    print_banner() 

    if args.ip:
        print_info("Querying current IP address...")
        current_ip = get_current_ip(use_tor=True)
        if current_ip:
            print_info(f"Current IP: {current_ip}")
        else:
            print_error("Could not determine current IP address.")
            sys.exit(1)
        sys.exit(0) 

    print_info("Starting TorNet IP changer...")
    if not is_tor_connectable():
        print_error("Tor service is not connectable. Cannot change IP.")
        print_warning("Please ensure Tor is installed, running, and configured correctly.")
        sys.exit(1)

    print_info("Performing initial IP check...")
    initial_ip = get_current_ip(use_tor=True)
    if not initial_ip:
        print_warning("Could not get initial IP via Tor. Proceeding with change attempts...")
 
    change_ip_repeatedly(args.interval, args.count)

    print_info(f"{TOOL_NAME} finished.")
    sys.exit(0)

if __name__ == "__main__":
    main()
