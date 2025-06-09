import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyfiglet import figlet_format
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

# Port scan function
def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        return port, True
    except:
        return port, False
    finally:
        s.close()

# Banner
print(figlet_format("ReconWizard", font="doom"))

# User input
ip = input("Enter IP address: ")
print("Port options:\n(1) Define ports\n(2) Top 1000\n(3) Top 10000\n(Default scans all 65535 ports)")
choice = input("Your choice: ")

# Thread count
try:
    max_threads = int(input("Enter number of threads (recommended: 100–1000): "))
    if max_threads > 1000:
        print("Capping threads to 1000.")
        max_threads = 1000
except ValueError:
    print("Invalid input. Using 100 threads.")
    max_threads = 100

# Port list
if choice == "1":
    ports = input("Enter ports (comma-separated): ")
    port_list = [int(p.strip()) for p in ports.split(",")]
elif choice == "2":
    port_list = list(range(1, 1001))
elif choice == "3":
    port_list = list(range(1, 10001))
else:
    print("Defaulting to all ports (1–65535).")
    port_list = list(range(1, 65536))

# Run scanner with tqdm progress bar
open_ports = []
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    future_to_port = {executor.submit(scan_port, ip, port): port for port in port_list}
    for future in tqdm(as_completed(future_to_port), total=len(port_list), desc="Scanning", unit="port"):
        port, is_open = future.result()
        if is_open:
            print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
