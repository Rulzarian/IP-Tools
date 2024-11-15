import requests
import socket
import os
import whois
from colorama import Fore, init

# Initialize Colorama (for Windows compatibility)
init(autoreset=True)

# Your API keys for ipwhois (replace with your actual key)
IPWHOIS_API_KEY = "your_ipwhois_api_key"

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an error if the response is not successful
        data = response.json()
        return data["ip"]
    except requests.RequestException as e:
        return f"Error fetching public IP: {e}"

# Function to get the private IP address (local network IP)
def get_private_ip():
    try:
        # Get the local machine's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Google's public DNS IP to establish connection
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Error fetching private IP: {e}"

# Function to get geolocation info from ipinfo.io
def get_ip_info_ipinfo(ip):
    try:
        url = f"http://ipinfo.io/{ip}/json"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the response is not successful
        return response.json()
    except requests.RequestException as e:
        return f"Error fetching data from ipinfo.io: {e}"

# Function to get geolocation info from ip-api.com
def get_ip_info_ip_api(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the response is not successful
        return response.json()
    except requests.RequestException as e:
        return f"Error fetching data from ip-api.com: {e}"

# Function to get geolocation info from ipwhois.io
def get_ip_info_ipwhois(ip):
    try:
        url = f"https://ipwhois.app/json/{ip}?key={IPWHOIS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the response is not successful
        return response.json()
    except requests.RequestException as e:
        return f"Error fetching data from ipwhois: {e}"

# Function to check if an IP is blacklisted using AbuseIPDB
def check_ip_blacklist(ip):
    try:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
        headers = {"Key": "your_abuseipdb_api_key"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['data']['abuseConfidenceScore'] > 50:
            return f"{ip} is blacklisted with a score of {data['data']['abuseConfidenceScore']}."
        else:
            return f"{ip} is not blacklisted."
    except requests.RequestException as e:
        return f"Error checking blacklist: {e}"

# Function to ping the IP and check Wi-Fi speed (latency)
def ping_ip(ip):
    try:
        # Pinging the IP using the OS ping command
        response = os.popen(f"ping {ip} -n 4").read()
        if "Request Timed Out" in response:
            return f"Ping to {ip} timed out."
        else:
            # Extracting the latency from the ping response
            lines = response.splitlines()
            for line in lines:
                if "Average" in line:
                    avg_latency = line.split('=')[1].strip().split('ms')[0]
                    return f"Average latency to {ip}: {avg_latency}ms"
            return f"Could not determine latency for {ip}."
    except Exception as e:
        return f"Error pinging IP: {e}"

# Function to get Whois information (ownership and registration details)
def get_ip_whois(ip):
    try:
        # Using the whois library to get ownership details
        domain_info = whois.whois(ip)
        if domain_info:
            return f"Whois information for {ip}: {domain_info}"
        else:
            return f"No Whois data found for {ip}."
    except Exception as e:
        return f"Error fetching Whois info: {e}"

# Function to display IP information
def display_ip_info(public_ip, private_ip):
    print(f"\nInformation for Public IP: {public_ip}\n")

    # Display Public IP details from ipinfo.io
    ip_info_ipinfo = get_ip_info_ipinfo(public_ip)
    if isinstance(ip_info_ipinfo, dict):
        print(Fore.BLUE + "Public IP Info from ipinfo.io:")
        print(Fore.BLUE + f"IP: {ip_info_ipinfo.get('ip', 'N/A')}")
        print(Fore.BLUE + f"Hostname: {ip_info_ipinfo.get('hostname', 'N/A')}")
        print(Fore.BLUE + f"City: {ip_info_ipinfo.get('city', 'N/A')}")
        print(Fore.BLUE + f"Region: {ip_info_ipinfo.get('region', 'N/A')}")
        print(Fore.BLUE + f"Country: {ip_info_ipinfo.get('country', 'N/A')}")
        print(Fore.BLUE + f"Location: {ip_info_ipinfo.get('loc', 'N/A')}")
    else:
        print(Fore.BLUE + ip_info_ipinfo)

    # Display Public IP details from ip-api.com
    ip_info_ip_api = get_ip_info_ip_api(public_ip)
    if isinstance(ip_info_ip_api, dict):
        print(Fore.RED + "Public IP Info from ip-api.com:")
        print(Fore.RED + f"IP: {ip_info_ip_api.get('query', 'N/A')}")
        print(Fore.RED + f"Country: {ip_info_ip_api.get('country', 'N/A')}")
        print(Fore.RED + f"Region: {ip_info_ip_api.get('regionName', 'N/A')}")
        print(Fore.RED + f"City: {ip_info_ip_api.get('city', 'N/A')}")
        print(Fore.RED + f"ZIP: {ip_info_ip_api.get('zip', 'N/A')}")
        print(Fore.RED + f"Latitude: {ip_info_ip_api.get('lat', 'N/A')}")
        print(Fore.RED + f"Longitude: {ip_info_ip_api.get('lon', 'N/A')}")
    else:
        print(Fore.RED + ip_info_ip_api)

    # Display Public IP details from ipwhois
    ip_info_ipwhois = get_ip_info_ipwhois(public_ip)
    if isinstance(ip_info_ipwhois, dict):
        print(Fore.YELLOW + "Public IP Info from ipwhois:")
        print(Fore.YELLOW + f"IP: {ip_info_ipwhois.get('ip', 'N/A')}")
        print(Fore.YELLOW + f"Country: {ip_info_ipwhois.get('country', 'N/A')}")
        print(Fore.YELLOW + f"Region: {ip_info_ipwhois.get('region', 'N/A')}")
        print(Fore.YELLOW + f"City: {ip_info_ipwhois.get('city', 'N/A')}")
        print(Fore.YELLOW + f"ASN: {ip_info_ipwhois.get('asn', 'N/A')}")
    else:
        print(Fore.YELLOW + ip_info_ipwhois)

    # Display Private IP in purple
    print(Fore.MAGENTA + f"\nPrivate IP: {private_ip}")

# Function to display ASCII art with an orange-ish color
def show_ascii_art():
    print(Fore.YELLOW + """
██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
██║██╔═══╝        ██║   ██║   ██║██║   ██║██║     ╚════██║
██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                                                                 
-Made By Rulzarian
    """)

# Main menu
def show_menu():
    print("""
1) Search Your Current Wi-Fi IP
2) Research Another IP Address
3) Check If IP Is Blacklisted
4) Ping IP To Check Wi-Fi Speed
5) Retrieve Whois Information For IP
6) Exit
""")

# Main function
def main():
    show_ascii_art()  # Show ASCII art in orange-like color
    while True:
        show_menu()
        choice = input("Choose an option (1/2/3/4/5/6): ").strip()

        if choice == '1':
            public_ip = get_public_ip()  # Get public IP
            private_ip = get_private_ip()  # Get private IP
            display_ip_info(public_ip, private_ip)  # Display public and private IP info
        elif choice == '2':
            ip_to_search = input("Enter the IP address you want to research: ").strip()
            display_ip_info(ip_to_search, ip_to_search)  # Display info for the entered IP
        elif choice == '3':
            ip_to_check = input("Enter the IP address to check if it's blacklisted: ").strip()
            print(check_ip_blacklist(ip_to_check))
        elif choice == '4':
            ip_to_ping = input("Enter the IP address to ping: ").strip()
            print(ping_ip(ip_to_ping))
        elif choice == '5':
            ip_for_whois = input("Enter the IP address or domain for Whois lookup: ").strip()
            print(get_ip_whois(ip_for_whois))
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
