import socket
import threading
from concurrent.futures import ThreadPoolExecutor
# Define the scanner
def scan_port(ip,port_range):
    try:
        s=socket.socket()
        s.settimeout(1)
        s.connect((ip,port_range))
        print(f"[+Port{port_range} is open]")
        s.close()
    except:
        pass

# Pre defined values for the script, script requires either the user supplies ports to scan if not avail;aible then script will scan top1000 or top 10000 ports,
#in order to do that script will load these ports list.

# Variables Required for script to execute
ip = input("Enter ip:")
print("Port:\n(1)Define Ports to scan\n(2)Use Top 1000\n(3)Use top 10000\nDefault scan all 65000 ports.")
choice = input("Your Choice:")
port_range=650001

# Threading Control
try:
    max_threads = int(input("Enter number of threads (recommended: 100–1000): "))
    if max_threads > 1001:
        print("Capping threads to 1000 to avoid overload.")
        max_threads = 1000
except ValueError:
    print("Invalid input. Using default of 100 threads.")
    max_threads = 100

# Consequence of user Choice
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    if choice == "1":
        ports = input("Enter ports (comma-separated): ")
        port_list = [int(p.strip()) for p in ports.split(",")]
        for port_range in port_list:
            executor.submit(scan_port, ip, port_range)

    elif choice == "2":
        for port_range in range(1, 1001):
            executor.submit(scan_port, ip, port_range)

    elif choice == "3":
        for port_range in range(1, 10001):
            executor.submit(scan_port, ip, port_range)

    else:
        print("Invalid choice.")


