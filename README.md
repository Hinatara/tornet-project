# TorNet

TorNet is a tool for automating IP address changes using the Tor network. It is designed to be compatible with standard Linux distributions and Termux.

**Note**: Please use this tool responsibly and ethically. Ensure that you comply with the terms of service of any website or service you interact with.

---

## Prerequisites

- **Python**: Version 3.7+ and pip.
  - Ensure Python and pip are installed on your system.
- **Tor**: The Tor service or program must be installed and configured.

### Installing Tor

#### Linux (Debian/Ubuntu):
```bash
sudo apt update && sudo apt install tor
```

#### Linux (Fedora):
```bash
sudo dnf install tor
```

#### Termux:
```bash
pkg update && pkg install tor
```

---

## Installation Guide

You can install TorNet from GitHub or from a local source directory. Once uploaded to PyPI (if applicable), you can also install it directly from there.

### Install from GitHub
```bash
pip install git+https://github.com/Hinatara/tornet-project.git
```

### Install from Local Source
1. Clone the project directory:
    ```bash
    git clone https://github.com/Hinatara/tornet-project.git
    cd tornet-project
    ```
2. Install the package:
    ```bash
    pip install .
    ```

### Install from PyPI (Future)
When the project is uploaded to PyPI, you can use:
```bash
pip install tornet
```

---

## Usage

### View Command Help
```bash
tornet -h
```

**Output**:
```
usage: tornet [-h] [--interval INTERVAL] [--count COUNT] [--ip] [--stop] [--version]

tornet - Automate IP address changes using Tor.

options:
  -h, --help           show this help message and exit
  --interval INTERVAL  Time in seconds between IP change attempts (default: 60)
  --count COUNT        Number of times to change the IP. Use 0 to run indefinitely (default: 10)
  --ip                 Display the current IP address (via Tor if possible) and exit
  --stop               Attempt to stop Tor service and kill related processes
  --version            show program's version number and exit
```

### Check Version
```bash
tornet --version
```

**Output**:
```
tornet 2.1.0
```

---

## Examples

- Change IP 5 times, with 30 seconds between each change:
    ```bash
    tornet --interval 30 --count 5
    ```

- Display the current IP via Tor:
    ```bash
    tornet --ip
    ```

- Stop the Tor service and related processes:
    ```bash
    tornet --stop
    ```

---

## Notes

- Ensure the Tor service is running before using IP change features. In Termux, you can run `tor` in a separate terminal session.
- If you encounter errors, check your Tor setup and dependencies like `requests[socks]`:
    ```bash
    pip install "requests[socks]"
    ```