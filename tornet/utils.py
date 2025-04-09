import subprocess
import shutil
import sys


GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[93m" 


def print_info(message):
    """Prints an informational message."""
    print(f"{WHITE}[{GREEN}+{WHITE}]{GREEN} {message}{RESET}")

def print_warning(message):
    """Prints a warning message."""
    print(f"{WHITE}[{YELLOW}!{WHITE}]{YELLOW} {message}{RESET}")

def print_error(message):
    """Prints an error message."""
    print(f"{WHITE}[{RED}!{WHITE}]{RED} {message}{RESET}")

def check_command(command):
    """Checks if a command exists in the system's PATH."""
    return shutil.which(command) is not None

def run_command(cmd_list, capture_output=False, check=False):
    """Runs a command using subprocess."""
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=capture_output,
            text=True,
            check=check 
        )
        return result
    except FileNotFoundError:
        print_error(f"Command not found: {cmd_list[0]}")
        return None
    except subprocess.CalledProcessError as e:
        
        if not check:
             print_error(f"Command '{' '.join(cmd_list)}' failed with exit code {e.returncode}")
        
        
        return None
    except Exception as e:
        print_error(f"An unexpected error occurred while running '{' '.join(cmd_list)}': {e}")
        return None

def is_systemd_running():
    """Check if systemd is the init system."""
   
    if not check_command("systemctl"):
        return False
    try:
        
        result = run_command(["systemctl", "is-system-running"], capture_output=True)
     
        return result and result.returncode == 0 and result.stdout.strip() in ["running", "degraded"]
    except Exception:
        return False 

def check_dependencies():
    """Checks for the essential 'tor' command."""
    print_info("Checking for Tor executable...")
    if not check_command("tor"):
        print_error("Tor executable not found in PATH.")
        print_warning("Please install Tor for your system:")
        print_warning("  Linux (Debian/Ubuntu): sudo apt install tor")
        print_warning("  Linux (Fedora): sudo dnf install tor")
        print_warning("  Termux: pkg install tor")
        sys.exit(1) 
    print_info("Tor executable found.")
    return True