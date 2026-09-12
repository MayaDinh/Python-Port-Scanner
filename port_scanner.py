'''
Python Port Scanner:
A lightweight Python script that scans specified IP addresses for open/closed ports.
'''

import socket
import sys
from datetime import datetime

# commonly scanned ports
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    161: "SNMP",
    443: "HTTPS",
    445: "SMB",
    1099: "Java RMI",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Proxy",
}

# scans a single port on the target
def scan_port(target, port, timeout=1):
    try:
        # create a socket object (ipv4 & tcp)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # attempt to connect
        result = sock.connect_ex((target, port))

        # get service name if available
        service = COMMON_PORTS.get(port, "Unknown")

        if result == 0:
            status = "OPEN"
        else:
            status = "CLOSED"

        sock.close()
        return port, status, service

    except socket.gaierror:
        return port, "ERROR", "Hostname resolution failed"
    except socket.error:
        return port, "ERROR", "Connection error"

# scan a single port and display result
def scan_single_port(target, port):
    print(f"\n[*] Scanning {target} on port {port}...")
    print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H: %M: %S')}")

    port_num, status, service = scan_port(target, port)

    if status == "OPEN":
        print(f"[+] Port {port_num}/{service}: {status}")
    elif status == "CLOSED":
        print(f"[-] Port {port_num}/{service}: {sttaus}")
    else:
        print(f"[!] Port {port_num}: {status} - {service}")

# scan multiple ports on a target
def scan_multiple_ports(target, ports):
    print(f"\n[*] Scanning {target} on {len(ports)} ports...")
    print(f"[*] Scan started at {datetime.now().strftime('%Y-%m-%d %H: %M: %S')}")
    print("-" * 50)

    open_ports = []
    closed_ports = []

    for port in ports:
        port_num, status, service = scan_port(target, port)

        if status == "OPEN":
            print(f"[+] Port {port_num}/{service}: {status}")
            open_ports.append((port_num, service))
        elif status == "CLOSED":
            print(f"[-] Port {port_num}/{service}: {status}")
            closed_ports.append(port_num)
        else:
            print(f"[!] Port {port_num}: {status} - {service}")

    # display summary
    print("-" * 50)
    print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H: %M: %S')}")
    print(f"[*] Total ports scanned: {len(ports)}")
    print(f"[*] Open ports: {len(open_ports)}")
    print(f"[*] Closed ports: {len(closed_ports)}")

    if open_ports:
        print("\n[+] Open ports found:")
        for port, service in open_ports:
            print(f"{port}/{service}")

# scan common well-known ports
def scan_common_ports(target):
    ports = list(COMMON_PORTS.keys())
    print(f"\n[*] Scanning common ports on {target}...")
    scan_multiple_ports(target, ports)

# validate IP address format
def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# main function with menu interface
def main():
    print("=" * 50)
    print("PYTHON PORT SCANNER")
    print("Simple Network Port Scanner Tool")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Scan single port")
        print("2. Scan multiple ports")
        print("3. Scan common ports")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == "1":
            target = input("Enter target IP address: ")
            if not validate_ip(target):
                print("[!] Invalid IP address")
                continue
                
            try:
                port = int(input("Enter port number (1-65535): "))
                if not 1 <= port <= 65535:
                    print("[!] Port must be between 1 and 65535")
                    continue
            except ValueError:
                print("[!] Port must be a number")
                continue
                
            scan_single_port(target, port)
            
        elif choice == "2":
            target = input("Enter target IP address: ")
            if not validate_ip(target):
                print("[!] Invalid IP address")
                continue
                
            port_input = input("Enter ports (comma-separated, e.g., 21,22,80): ")
            try:
                ports = [int(p.strip()) for p in port_input.split(",")]
                if not all(1 <= p <= 65535 for p in ports):
                    print("[!] All ports must be between 1 and 65535")
                    continue
            except ValueError:
                print("[!] Invalid port format")
                continue
                
            scan_multiple_ports(target, ports)
            
        elif choice == "3":
            target = input("Enter target IP address: ")
            if not validate_ip(target):
                print("[!] Invalid IP address")
                continue
                
            scan_common_ports(target)
            
        elif choice == "4":
            print("\n[*] Exiting Port Scanner. Scan responsibly!")
            sys.exit(0)
            
        else:
            print("[!] Invalid option. Please select 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        print("[*] Exiting...")
        sys.exit(0)

