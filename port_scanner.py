import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

open_ports = []

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080]

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def get_risk_level(port):
    high_risk = [21, 23, 445, 3389]
    medium_risk = [22, 25, 110, 139, 143, 3306]
    low_risk = [53, 80, 443]

    if port in high_risk:
        return "HIGH"
    elif port in medium_risk:
        return "MEDIUM"
    elif port in low_risk:
        return "LOW"
    else:
        return "UNKNOWN"

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = get_service_name(port)
            risk = get_risk_level(port)
            output = f"[OPEN] Port {port} | Service: {service} | Risk: {risk}"
            print(output)
            open_ports.append(output)

        sock.close()
    except:
        pass

def main():
    print("=" * 60)
    print("      ADVANCED PORT SCANNER")
    print("   Threading + Service Detection + Risk Tagging")
    print("=" * 60)

    target = input("Enter Target IP or Domain: ")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid target. Please enter a valid IP or domain.")
        return

    print("\nSelect Scan Mode:")
    print("1. Quick Scan (Common Ports)")
    print("2. Custom Scan Range")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        ports_to_scan = COMMON_PORTS
        scan_type = "Quick Scan"
    elif choice == "2":
        start_port = int(input("Enter Start Port: "))
        end_port = int(input("Enter End Port: "))
        ports_to_scan = range(start_port, end_port + 1)
        scan_type = "Custom Scan"
    else:
        print("Invalid choice.")
        return

    start_time = datetime.now()

    print(f"\nScanning Target: {target} ({target_ip})")
    print(f"Scan Type: {scan_type}")
    print("-" * 60)

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in ports_to_scan:
            executor.submit(scan_port, target_ip, port)

    end_time = datetime.now()

    print("-" * 60)
    print(f"Total Ports Scanned: {len(list(ports_to_scan)) if scan_type == 'Custom Scan' else len(COMMON_PORTS)}")
    print(f"Open Ports Found: {len(open_ports)}")
    print(f"Scan Completed At: {end_time}")

    with open("scan_results.txt", "w") as file:
        file.write("ADVANCED PORT SCANNER RESULTS\n")
        file.write("=" * 60 + "\n")
        file.write(f"Target: {target}\n")
        file.write(f"Target IP: {target_ip}\n")
        file.write(f"Scan Type: {scan_type}\n")
        file.write(f"Scan Time: {start_time} to {end_time}\n")
        file.write("-" * 60 + "\n")

        if open_ports:
            for port in open_ports:
                file.write(port + "\n")
        else:
            file.write("No open ports found.\n")

        file.write("-" * 60 + "\n")
        file.write(f"Total Ports Scanned: {len(list(ports_to_scan)) if scan_type == 'Custom Scan' else len(COMMON_PORTS)}\n")
        file.write(f"Open Ports Found: {len(open_ports)}\n")

if __name__ == "__main__":
    main()
