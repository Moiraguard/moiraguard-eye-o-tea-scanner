#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ███╗   ███╗ ██████╗ ██╗██████╗  █████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗   ║
║   ████╗ ████║██╔═══██╗██║██╔══██╗██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗  ║
║   ██╔████╔██║██║   ██║██║██████╔╝███████║██║  ███╗██║   ██║███████║██████╔╝██║  ██║  ║
║   ██║╚██╔╝██║██║   ██║██║██╔══██╗██╔══██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║  ║
║   ██║ ╚═╝ ██║╚██████╔╝██║██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝  ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝   ║
║                                                                       ║
║                           👁️  Eye - O - Tea (IoT)                    ║
║              Global IoT/IIoT Infrastructure Reconnaissance            ║
║                 Monitoring IoT Reconnaissance & Guard                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

Author: Mohammed Amine Moulay (@MLY)
DEFCON GROUP CASANLANCA 2026 | IoT Security Research
Version: 1.0-MOIRAGUARD
License: Research & Educational Use Only

[WARNING] This tool is for security research and education only.
[WARNING] Unauthorized access to systems is illegal.
[WARNING] Use responsibly and ethically.
"""

import shodan
import sys
import time
from datetime import datetime
from collections import defaultdict
import os
import json
import csv
from pathlib import Path
import base64
import socket
import ssl
import concurrent.futures
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# HTML to PNG conversion (optional - will check if available)
try:
    from html2image import Html2Image
    HTML2IMAGE_AVAILABLE = True
except ImportError:
    HTML2IMAGE_AVAILABLE = False

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                         COLOR SCHEMES                             ║
# ╚═══════════════════════════════════════════════════════════════════╝

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[38;5;135m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    END = '\033[0m'
    CLEAR = '\033[2J\033[H'

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      UTILITY FUNCTIONS                            ║
# ╚═══════════════════════════════════════════════════════════════════╝

def typewriter_print(text, delay=0.03):
    """Print text with typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_separator(char='═', length=70, color=Colors.CYAN):
    """Print a separator line"""
    print(f"{color}{char * length}{Colors.END}")

def loading_animation(text="Initializing", duration=2):
    """Show loading animation"""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]} {text}...{Colors.END}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def print_status(status_type, message):
    """Print formatted status message"""
    icons = {
        'success': f'{Colors.GREEN}[✓]{Colors.END}',
        'error': f'{Colors.RED}[✗]{Colors.END}',
        'warning': f'{Colors.YELLOW}[!]{Colors.END}',
        'info': f'{Colors.CYAN}[i]{Colors.END}',
        'scan': f'{Colors.MAGENTA}[►]{Colors.END}',
        'found': f'{Colors.GREEN}[◆]{Colors.END}',
        'critical': f'{Colors.RED}{Colors.BLINK}[!!!]{Colors.END}'
    }
    icon = icons.get(status_type, f'{Colors.WHITE}[•]{Colors.END}')
    print(f"{icon} {message}")

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      API KEY MANAGEMENT                           ║
# ╚═══════════════════════════════════════════════════════════════════╝

def load_api_key():
    """Load API key from file"""
    key_file = 'shodan_api.key'

    loading_animation("Loading API credentials", 1.5)

    if not os.path.exists(key_file):
        print_status('error', f"API key file not found: {Colors.YELLOW}{key_file}{Colors.END}")
        print_status('info', f"Create file '{Colors.CYAN}{key_file}{Colors.END}' with your API key")
        print_status('info', f"Get key from: {Colors.UNDERLINE}https://account.shodan.io/{Colors.END}")
        sys.exit(1)

    try:
        with open(key_file, 'r') as f:
            api_key = f.read().strip()

        if not api_key:
            print_status('error', "API key file is empty")
            sys.exit(1)

        print_status('success', f"API key loaded from {Colors.CYAN}{key_file}{Colors.END}")
        print_status('info', f"Key length: {Colors.GREEN}{len(api_key)} characters{Colors.END}")
        return api_key

    except Exception as e:
        print_status('error', f"Error reading API key: {Colors.RED}{e}{Colors.END}")
        sys.exit(1)

def check_requirements(api_key):
    """Check all requirements before starting scan to avoid wasting credits"""
    print_separator('═', 70, Colors.CYAN)
    print(f"{Colors.BOLD}{Colors.CYAN}PRE-SCAN REQUIREMENTS CHECK{Colors.END}")
    print_separator('─', 70, Colors.CYAN)

    try:
        # Test API connection
        loading_animation("Testing Shodan API connection", 1.5)
        api = shodan.Shodan(api_key)

        # Get account information
        loading_animation("Retrieving account information", 1)
        info = api.info()

        # Display API status
        print(f"\n{Colors.GREEN}✓{Colors.END} {Colors.BOLD}API Connection:{Colors.END} {Colors.GREEN}Active{Colors.END}")

        # Display account info
        plan = info.get('plan', 'Unknown')
        query_credits = info.get('query_credits', 0)
        scan_credits = info.get('scan_credits', 0)

        print(f"{Colors.GREEN}✓{Colors.END} {Colors.BOLD}Account Plan:{Colors.END} {Colors.CYAN}{plan}{Colors.END}")

        # Display credits with color coding
        if query_credits < 10:
            credit_color = Colors.RED
            warning_icon = "⚠️ "
        elif query_credits < 50:
            credit_color = Colors.YELLOW
            warning_icon = "⚡"
        else:
            credit_color = Colors.GREEN
            warning_icon = "✓"

        print(f"{warning_icon} {Colors.BOLD}Query Credits:{Colors.END} {credit_color}{query_credits}{Colors.END}")
        print(f"{Colors.GREEN}✓{Colors.END} {Colors.BOLD}Scan Credits:{Colors.END} {Colors.CYAN}{scan_credits}{Colors.END}")

        # Show scan cost info
        print(f"\n{Colors.BOLD}{Colors.CYAN}Scan Information:{Colors.END}")
        print(f"  • This scan will use: {Colors.YELLOW}6 query credits{Colors.END}")
        print(f"  • Credits after scan: {Colors.CYAN}{max(0, query_credits - 6)}{Colors.END}")

        # Warning if low credits
        if query_credits < 6:
            print(f"\n{Colors.RED}⚠️  INSUFFICIENT CREDITS{Colors.END}")
            print(f"{Colors.RED}You need at least 6 query credits to run this scan.{Colors.END}")
            print(f"{Colors.YELLOW}Get more credits at: https://account.shodan.io/{Colors.END}")
            return False
        elif query_credits < 10:
            print(f"\n{Colors.YELLOW}⚠️  WARNING: Low credits detected!{Colors.END}")
            print(f"{Colors.YELLOW}You have {query_credits} credits remaining.{Colors.END}")
            print(f"{Colors.DIM}Consider topping up at: https://account.shodan.io/{Colors.END}")

        print_separator('─', 70, Colors.CYAN)

        # Ask for confirmation
        while True:
            try:
                confirm = input(f"\n{Colors.BOLD}Proceed with scan? [Y/n]: {Colors.END}").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    print_status('success', "Requirements verified - proceeding with scan")
                    return True
                elif confirm in ['n', 'no']:
                    print_status('info', "Scan cancelled by user")
                    return False
                else:
                    print_status('error', "Please enter Y or N")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Cancelled by user{Colors.END}")
                return False

    except shodan.APIError as e:
        print(f"\n{Colors.RED}✗ API Connection Failed{Colors.END}")
        print_status('error', f"Shodan API Error: {Colors.RED}{e}{Colors.END}")
        print_status('info', "Please check your API key and internet connection")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}✗ Requirements Check Failed{Colors.END}")
        print_status('error', f"Unexpected error: {Colors.RED}{e}{Colors.END}")
        return False

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                   COUNTRY SELECTION                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

def load_countries():
    """Load country list from JSON file"""
    config_file = 'countries.json'

    if not os.path.exists(config_file):
        print_status('warning', f"Config file not found: {Colors.YELLOW}{config_file}{Colors.END}")
        print_status('info', "Using default country list")
        return {
            "Morocco": "MA",
            "United States": "US",
            "China": "CN",
            "Russia": "RU",
            "Germany": "DE",
            "United Kingdom": "GB",
            "France": "FR",
            "India": "IN",
            "Brazil": "BR",
            "Japan": "JP"
        }

    try:
        with open(config_file, 'r') as f:
            data = json.load(f)
            print_status('success', f"Loaded {Colors.GREEN}{len(data.get('countries', {}))}{Colors.END} countries from config")
            return data.get('countries', {})
    except Exception as e:
        print_status('error', f"Error loading config: {Colors.RED}{e}{Colors.END}")
        sys.exit(1)

def display_country_menu(countries):
    """Display country selection menu"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}            {Colors.WHITE}SELECT TARGET COUNTRY{Colors.END}              {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")

    print(f"{Colors.GREEN}[0]{Colors.END} {Colors.BOLD}GLOBAL{Colors.END} {Colors.DIM}(All countries - no filter){Colors.END}\n")

    country_list = list(countries.items())
    for idx, (country_name, country_code) in enumerate(country_list, 1):
        print(f"{Colors.CYAN}[{idx}]{Colors.END} {country_name:20s} {Colors.DIM}({country_code}){Colors.END}")

    print(f"\n{Colors.YELLOW}[C]{Colors.END} {Colors.DIM}Custom country code{Colors.END}")
    print_separator('─', 60, Colors.DIM)

    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Select option: {Colors.END}").strip()

            if choice.upper() == 'C':
                custom_code = input(f"{Colors.CYAN}Enter 2-letter country code (e.g., MA, US): {Colors.END}").strip().upper()
                if len(custom_code) == 2:
                    return custom_code, f"Custom ({custom_code})"
                else:
                    print_status('error', "Invalid country code format")
                    continue

            choice_num = int(choice)

            if choice_num == 0:
                return None, "Global"
            elif 1 <= choice_num <= len(country_list):
                country_name, country_code = country_list[choice_num - 1]
                return country_code, country_name
            else:
                print_status('error', f"Please enter a number between 0 and {len(country_list)}")
        except ValueError:
            print_status('error', "Invalid input. Please enter a number or 'C'")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Selection cancelled{Colors.END}")
            sys.exit(0)

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      MOIRAGUARD BANNER                            ║
# ╚═══════════════════════════════════════════════════════════════════╝

def print_banner():
    """MOIRAGUARD Eye O Tea banner"""
    
    print(Colors.CLEAR)
    
    # Main banner with Eye O Tea
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ███╗   ███╗ ██████╗ ██╗██████╗  █████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗   ║
║   ████╗ ████║██╔═══██╗██║██╔══██╗██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗  ║
║   ██╔████╔██║██║   ██║██║██████╔╝███████║██║  ███╗██║   ██║███████║██████╔╝██║  ██║  ║
║   ██║╚██╔╝██║██║   ██║██║██╔══██╗██╔══██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║  ║
║   ██║ ╚═╝ ██║╚██████╔╝██║██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝  ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.GREEN}{Colors.BOLD}
                     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
                   ▄▀░░░░░░░░░░░░░░░▀▄
                  █░░░▄▀▀▀▀▀▀▀▀▀▄░░░░█
                 █░░░█░░░░░░░░░░█░░░░█
                 █░░░█░░░░ 👁️  ░░█░░░░█    {Colors.CYAN}Eye{Colors.END}  {Colors.WHITE}O{Colors.END}  {Colors.GREEN}Tea{Colors.END}
                 █░░░█░░░░░░░░░░█░░░░█         {Colors.DIM}(IoT){Colors.END}
                  █░░░▀▄▄▄▄▄▄▄▄▄▀░░░░█
                   ▀▄░░░░░░░░░░░░░░▄▀
                     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
{Colors.END}

{Colors.CYAN}┌───────────────────────────────────────────────────────────────────────┐{Colors.END}
{Colors.CYAN}│{Colors.END}  {Colors.WHITE}Global IoT/IIoT Infrastructure Reconnaissance Framework{Colors.END}          {Colors.CYAN}│{Colors.END}
{Colors.CYAN}│{Colors.END}  {Colors.GREEN}Monitoring IoT Reconnaissance & Guard{Colors.END}                           {Colors.CYAN}│{Colors.END}
{Colors.CYAN}└───────────────────────────────────────────────────────────────────────┘{Colors.END}

{Colors.DIM}
┌───────────────────────────────────────────────────────────────────────┐
│  Author: {Colors.WHITE}Mohammed Amine Moulay (@MLY){Colors.DIM}                              │
│  Event:  {Colors.CYAN}DEFCON GROUP CASANLANCA 2026{Colors.DIM}                                        │
│  Focus:  {Colors.GREEN}IoT Security Research & Industrial Protocol Analysis{Colors.DIM}      │
│  Build:  {Colors.YELLOW}v1.0-MOIRAGUARD{Colors.DIM} ({datetime.now().strftime('%Y.%m.%d')}){Colors.DIM}                                 │
└───────────────────────────────────────────────────────────────────────┘
{Colors.END}
"""
    print(banner)
    
    # Warning
    print(f"\n{Colors.RED}{Colors.BOLD}⚠️  LEGAL WARNING ⚠️{Colors.END}")
    print(f"{Colors.YELLOW}This tool is for SECURITY RESEARCH and EDUCATION only.{Colors.END}")
    print(f"{Colors.DIM}• Unauthorized access to systems is ILLEGAL{Colors.END}")
    print(f"{Colors.DIM}• This tool performs PASSIVE reconnaissance only{Colors.END}")
    print(f"{Colors.DIM}• Use RESPONSIBLY and ETHICALLY{Colors.END}\n")
    
    time.sleep(1)
    
    print(f"{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}]{Colors.END} {Colors.GREEN}System initialized{Colors.END}")
    print(f"{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}]{Colors.END} {Colors.GREEN}Reconnaissance mode: {Colors.YELLOW}PASSIVE{Colors.END}")
    print(f"{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}]{Colors.END} {Colors.GREEN}Target scope: {Colors.YELLOW}GLOBAL IoT/IIoT{Colors.END}")
    
    print_separator()
    loading_animation("Preparing MOIRAGUARD scan modules", 2)
    print()

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    SCAN DATA STORAGE                              ║
# ╚═══════════════════════════════════════════════════════════════════╝

class ScanData:
    """Store detailed scan results"""
    def __init__(self, country_code=None, country_name=None):
        self.timestamp = datetime.now()
        self.country_code = country_code
        self.country_name = country_name if country_name else "Global"
        self.categories = {}
        self.detailed_results = []

    def add_category(self, category_name, total_count):
        """Add category statistics"""
        self.categories[category_name] = {
            'count': total_count,
            'devices': []
        }

    def add_device(self, category_name, device_info):
        """Add detailed device information"""
        if category_name in self.categories:
            self.categories[category_name]['devices'].append(device_info)

    def to_dict(self):
        """Convert to dictionary for export"""
        return {
            'scan_timestamp': self.timestamp.isoformat(),
            'scan_date': self.timestamp.strftime('%Y-%m-%d'),
            'scan_time': self.timestamp.strftime('%H:%M:%S'),
            'target_country': self.country_name,
            'country_code': self.country_code,
            'total_devices': sum(cat['count'] for cat in self.categories.values()),
            'categories': self.categories
        }

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      SCAN FUNCTIONS                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

def scan_header(scan_num, total, title, risk_level, risk_color):
    """Print scan header"""
    print_separator('─', 70, Colors.DIM)
    print(f"\n{Colors.BOLD}{Colors.WHITE}[SCAN {scan_num}/{total}]{Colors.END} {Colors.CYAN}►{Colors.END} {Colors.BOLD}{risk_color}{title}{Colors.END}")
    print(f"{Colors.YELLOW}Risk Level: {risk_color}{risk_level}{Colors.END}\n")

def scan_smart_home_devices(api, country_code=None, scan_data=None, verbose=False):
    """Scan for smart home appliances"""
    scan_header(1, 6, "SMART HOME APPLIANCES & CONSUMER IoT", "HIGH ⚠️⚠️", Colors.ORANGE)

    query = '"smart home" port:80,8080,443'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Querying Shodan database", 1.5)

    try:
        results = api.search(query)
        total = results['total']

        print_status('found', f"Discovered {Colors.BOLD}{Colors.GREEN}{total:,}{Colors.END} exposed smart home devices globally")
        print_status('warning', f"Risk: {Colors.RED}Unsecured management interfaces{Colors.END}")

        # Store in scan_data if provided
        if scan_data:
            scan_data.add_category("Smart Home Devices", total)

        # Count countries - INCREASED SAMPLE SIZE
        countries = defaultdict(int)
        for result in results['matches'][:100]:
            country = result.get('location', {}).get('country_name', 'Unknown')
            countries[country] += 1

            # Store detailed info if verbose mode
            if scan_data and verbose:
                device_info = {
                    'ip': result['ip_str'],
                    'port': result.get('port', 'N/A'),
                    'product': result.get('product', 'Smart Home Device'),
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': result.get('org', 'Unknown'),
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("Smart Home Devices", device_info)

        # Show geographic distribution (keep existing display logic)
        morocco_count = countries.get('Morocco', 0)
        print(f"\n{Colors.BOLD}{Colors.CYAN}Geographic Distribution:{Colors.END}")

        if morocco_count > 0:
            print(f"  {Colors.YELLOW}►{Colors.END} {'Morocco (Local)':20s} {Colors.YELLOW}{'█' * min(morocco_count * 2, 40)}{Colors.END} {morocco_count}")
            other_countries = {k: v for k, v in countries.items() if k != 'Morocco'}
            for country, count in sorted(other_countries.items(), key=lambda x: x[1], reverse=True)[:4]:
                bar = '█' * min(count * 2, 40)
                print(f"  {Colors.GREEN}►{Colors.END} {country:20s} {Colors.YELLOW}{bar}{Colors.END} {count}")
        else:
            for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]:
                bar = '█' * min(count * 2, 40)
                print(f"  {Colors.GREEN}►{Colors.END} {country:20s} {Colors.YELLOW}{bar}{Colors.END} {count}")

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Sample Devices:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            product = result.get('product', 'Smart Home Device')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.YELLOW}[{i}]{Colors.END} {Colors.WHITE}{ip:15s}{Colors.END} │ {product:25s} │ {Colors.CYAN}{country}{Colors.END}")

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

def scan_iot_cameras(api, country_code=None, scan_data=None, verbose=False):
    """Scan for IoT cameras"""
    scan_header(2, 6, "IoT CAMERAS & SURVEILLANCE SYSTEMS (RTSP)", "CRITICAL ⚠️⚠️⚠️", Colors.RED)

    query = 'port:554 "RTSP/1.0"'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Scanning for RTSP streams", 1.5)

    try:
        results = api.search(query)
        total = results['total']

        print_status('critical', f"Found {Colors.BOLD}{Colors.RED}{total:,}{Colors.END} exposed camera streams")
        print_status('warning', f"Risk: {Colors.RED}Unprotected video surveillance{Colors.END}")

        if scan_data:
            scan_data.add_category("IoT Cameras", total)

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Live Stream Exposures:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            org = result.get('org', 'Unknown')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.RED}[{i}]{Colors.END} {Colors.WHITE}rtsp://{ip}:554{Colors.END}")
            print(f"      ├─ Organization: {Colors.CYAN}{org}{Colors.END}")
            print(f"      └─ Location: {Colors.YELLOW}{country}{Colors.END}")

            if scan_data and verbose:
                device_info = {
                    'ip': ip,
                    'port': 554,
                    'product': result.get('product', 'RTSP Camera'),
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': org,
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("IoT Cameras", device_info)

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

def scan_scada_ics(api, country_code=None, scan_data=None, verbose=False):
    """Scan for SCADA/ICS"""
    scan_header(3, 6, "SCADA / INDUSTRIAL CONTROL SYSTEMS", "CRITICAL ⚠️⚠️⚠️", Colors.RED)

    query = 'port:502 "Modbus"'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Discovering critical infrastructure", 2)
    
    try:
        results = api.search(query)
        total = results['total']

        print_status('critical', f"Discovered {Colors.BOLD}{Colors.RED}{total:,}{Colors.END} SCADA/ICS systems exposed")
        print_status('warning', f"Impact: {Colors.RED}Critical infrastructure{Colors.END}")

        if scan_data:
            scan_data.add_category("SCADA/ICS", total)

        print(f"\n{Colors.BOLD}{Colors.RED}Potential Sectors Affected:{Colors.END}")
        sectors = [
            ("Manufacturing & Production", "⚙️"),
            ("Water Treatment Facilities", "💧"),
            ("Power Generation/Distribution", "⚡"),
            ("Building Automation Systems", "🏭"),
        ]
        for sector, icon in sectors:
            print(f"  {Colors.YELLOW}{icon}{Colors.END}  {sector}")

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Critical Infrastructure Exposures:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            org = result.get('org', 'Unknown')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.RED}[CRITICAL-{i}]{Colors.END} {Colors.WHITE}{ip}:502{Colors.END}")
            print(f"      ├─ Organization: {Colors.CYAN}{org}{Colors.END}")
            print(f"      ├─ Country: {Colors.YELLOW}{country}{Colors.END}")
            print(f"      └─ Protocol: {Colors.RED}Modbus (Industrial){Colors.END}")

            if scan_data and verbose:
                device_info = {
                    'ip': ip,
                    'port': 502,
                    'product': result.get('product', 'Modbus SCADA'),
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': org,
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("SCADA/ICS", device_info)

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

def scan_building_automation(api, country_code=None, scan_data=None, verbose=False):
    """Scan for Building Management Systems"""
    scan_header(4, 6, "BUILDING AUTOMATION SYSTEMS (BACnet)", "HIGH ⚠️⚠️", Colors.ORANGE)

    query = 'port:47808 "BACnet"'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Analyzing building automation protocols", 1.5)
    
    try:
        results = api.search(query)
        total = results['total']

        print_status('found', f"Located {Colors.BOLD}{Colors.ORANGE}{total:,}{Colors.END} building automation systems")
        print_status('warning', f"Controls: {Colors.RED}HVAC, lighting, security{Colors.END}")

        if scan_data:
            scan_data.add_category("Building Automation", total)

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Building System Exposures:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            org = result.get('org', 'Unknown')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.ORANGE}[{i}]{Colors.END} {Colors.WHITE}{ip}:47808{Colors.END}")
            print(f"      ├─ Organization: {Colors.CYAN}{org}{Colors.END}")
            print(f"      └─ Country: {Colors.YELLOW}{country}{Colors.END}")

            if scan_data and verbose:
                device_info = {
                    'ip': ip,
                    'port': 47808,
                    'product': result.get('product', 'BACnet System'),
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': org,
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("Building Automation", device_info)

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

def scan_iot_mqtt(api, country_code=None, scan_data=None, verbose=False):
    """Scan for MQTT brokers"""
    scan_header(5, 6, "IoT MQTT MESSAGING BROKERS", "HIGH ⚠️⚠️", Colors.ORANGE)

    query = 'port:1883 "mosquitto"'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Discovering IoT messaging infrastructure", 1.5)
    
    try:
        results = api.search(query)
        total = results['total']

        print_status('found', f"Found {Colors.BOLD}{Colors.ORANGE}{total:,}{Colors.END} exposed MQTT brokers")
        print_status('warning', f"Risk: {Colors.RED}IoT device communication interception{Colors.END}")

        if scan_data:
            scan_data.add_category("MQTT Brokers", total)

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}MQTT Broker Exposures:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            version = result.get('product', 'MQTT Broker')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.ORANGE}[{i}]{Colors.END} {Colors.WHITE}{ip}:1883{Colors.END}")
            print(f"      ├─ Version: {Colors.CYAN}{version}{Colors.END}")
            print(f"      └─ Country: {Colors.YELLOW}{country}{Colors.END}")

            if scan_data and verbose:
                device_info = {
                    'ip': ip,
                    'port': 1883,
                    'product': version,
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': result.get('org', 'Unknown'),
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("MQTT Brokers", device_info)

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

def scan_industrial_iot(api, country_code=None, scan_data=None, verbose=False):
    """Scan for Industrial IoT"""
    scan_header(6, 6, "INDUSTRIAL IoT GATEWAYS & AUTOMATION", "CRITICAL ⚠️⚠️⚠️", Colors.RED)

    query = '"Industrial IoT" OR "IIoT Gateway" OR "Siemens" OR "Allen Bradley"'
    if country_code:
        query += f' country:{country_code}'
    print_status('scan', f"Query: {Colors.CYAN}{query}{Colors.END}")
    loading_animation("Scanning industrial automation systems", 2)
    
    try:
        results = api.search(query)
        total = results['total']

        print_status('critical', f"Identified {Colors.BOLD}{Colors.RED}{total:,}{Colors.END} Industrial IoT systems")
        print_status('warning', f"Risk: {Colors.RED}Production line control{Colors.END}")

        if scan_data:
            scan_data.add_category("Industrial IoT", total)

        # Vendor distribution
        vendors = defaultdict(int)
        for result in results['matches'][:20]:
            product = result.get('product', '').lower()
            if 'siemens' in product:
                vendors['Siemens'] += 1
            elif 'rockwell' in product or 'allen bradley' in product:
                vendors['Rockwell/Allen Bradley'] += 1
            elif 'schneider' in product:
                vendors['Schneider Electric'] += 1
            else:
                vendors['Other'] += 1

        print(f"\n{Colors.BOLD}{Colors.CYAN}Vendor Distribution:{Colors.END}")
        for vendor, count in sorted(vendors.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                bar = '█' * min(count * 2, 20)
                print(f"  {Colors.GREEN}►{Colors.END} {vendor:30s} {Colors.YELLOW}{bar}{Colors.END} {count}")

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}IIoT System Exposures:{Colors.END}")
        for i, result in enumerate(results['matches'][:3], 1):
            ip = result['ip_str']
            product = result.get('product', 'Industrial System')
            country = result.get('location', {}).get('country_name', 'Unknown')
            print(f"  {Colors.RED}[IIoT-{i}]{Colors.END} {Colors.WHITE}{ip}{Colors.END}")
            print(f"      ├─ System: {Colors.CYAN}{product}{Colors.END}")
            print(f"      └─ Country: {Colors.YELLOW}{country}{Colors.END}")

            if scan_data and verbose:
                device_info = {
                    'ip': ip,
                    'port': result.get('port', 'N/A'),
                    'product': product,
                    'version': result.get('version', 'Unknown'),
                    'country': country,
                    'city': result.get('location', {}).get('city', 'Unknown'),
                    'org': result.get('org', 'Unknown'),
                    'isp': result.get('isp', 'Unknown'),
                    'timestamp': result.get('timestamp', 'Unknown')
                }
                scan_data.add_device("Industrial IoT", device_info)

        return total
    except Exception as e:
        print_status('error', f"Scan failed: {e}")
        return 0

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    EXPORT & VISUALIZATION                         ║
# ╚═══════════════════════════════════════════════════════════════════╝

def create_output_directory():
    """Create output directory for exports"""
    output_dir = Path("Moiraguard-Eye-O-Tea-Exports")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def export_json(scan_data, verbose=False):
    """Export scan results to JSON"""
    try:
        output_dir = create_output_directory()
        timestamp = scan_data.timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"moiraguard_scan_{timestamp}.json"
        filepath = output_dir / filename

        data = scan_data.to_dict()
        if not verbose:
            # Remove detailed device info for non-verbose exports
            for category in data['categories'].values():
                category['devices'] = []

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print_status('success', f"JSON exported to: {Colors.CYAN}{filepath}{Colors.END}")
        return filepath
    except Exception as e:
        print_status('error', f"JSON export failed: {Colors.RED}{e}{Colors.END}")
        return None

def export_csv(scan_data, verbose=False):
    """Export scan results to CSV"""
    try:
        output_dir = create_output_directory()
        timestamp = scan_data.timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"moiraguard_scan_{timestamp}.csv"
        filepath = output_dir / filename

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write metadata
            writer.writerow(['MOIRAGUARD IoT Security Scan Report'])
            writer.writerow(['Scan Date', scan_data.timestamp.strftime('%Y-%m-%d')])
            writer.writerow(['Scan Time', scan_data.timestamp.strftime('%H:%M:%S')])
            writer.writerow(['Target', scan_data.country_name])
            writer.writerow(['Country Code', scan_data.country_code or 'Global'])
            writer.writerow([])

            # Write summary
            writer.writerow(['Category Summary'])
            writer.writerow(['Category', 'Device Count', 'Risk Level'])

            risk_levels = {
                'Smart Home Devices': 'HIGH',
                'IoT Cameras': 'CRITICAL',
                'SCADA/ICS': 'CRITICAL',
                'Building Automation': 'HIGH',
                'MQTT Brokers': 'HIGH',
                'Industrial IoT': 'CRITICAL'
            }

            for category, data in scan_data.categories.items():
                risk = risk_levels.get(category, 'MEDIUM')
                writer.writerow([category, data['count'], risk])

            writer.writerow([])
            writer.writerow(['Total Devices', sum(cat['count'] for cat in scan_data.categories.values())])

            # Write detailed devices if verbose
            if verbose:
                writer.writerow([])
                writer.writerow(['Detailed Device Information'])
                writer.writerow(['Category', 'IP Address', 'Port', 'Product', 'Version', 'Country', 'City', 'Organization', 'ISP', 'Timestamp'])

                for category, data in scan_data.categories.items():
                    for device in data['devices']:
                        writer.writerow([
                            category,
                            device.get('ip', 'N/A'),
                            device.get('port', 'N/A'),
                            device.get('product', 'N/A'),
                            device.get('version', 'N/A'),
                            device.get('country', 'N/A'),
                            device.get('city', 'N/A'),
                            device.get('org', 'N/A'),
                            device.get('isp', 'N/A'),
                            device.get('timestamp', 'N/A')
                        ])

        print_status('success', f"CSV exported to: {Colors.CYAN}{filepath}{Colors.END}")
        return filepath
    except Exception as e:
        print_status('error', f"CSV export failed: {Colors.RED}{e}{Colors.END}")
        return None

def export_png_charts(scan_data):
    """Export charts as PNG images using matplotlib with logo and improved styling"""
    try:
        output_dir = create_output_directory()
        timestamp = scan_data.timestamp.strftime('%Y%m%d_%H%M%S')

        # Prepare data
        categories = list(scan_data.categories.keys())
        counts = [scan_data.categories[cat]['count'] for cat in categories]
        total = sum(counts)

        # Enhanced color scheme for risk levels
        colors_map = {
            'Smart Home Devices': '#FF8C00',  # Orange
            'IoT Cameras': '#DC143C',         # Crimson
            'SCADA/ICS': '#B22222',           # Fire Brick
            'Building Automation': '#FF6347', # Tomato
            'MQTT Brokers': '#FFA500',        # Orange
            'Industrial IoT': '#8B0000'       # Dark Red
        }
        colors = [colors_map.get(cat, '#4682B4') for cat in categories]

        # Modern clean style with better fonts
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
            'font.size': 11,
            'axes.labelsize': 13,
            'axes.titlesize': 16,
            'xtick.labelsize': 11,
            'ytick.labelsize': 11,
            'legend.fontsize': 11,
            'figure.titlesize': 18
        })

        # Load logo if available
        logo_path = Path("MoiraGuard-Eye-O-Tea-logo.png")
        logo_img = None
        if logo_path.exists():
            try:
                logo_img = plt.imread(str(logo_path))
            except Exception:
                pass

        # 1. PIE CHART - Device Distribution (Improved)
        fig1, ax1 = plt.subplots(figsize=(14, 10), facecolor='white')

        wedges, texts, autotexts = ax1.pie(
            counts, labels=categories, colors=colors,
            autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'},
            explode=[0.03] * len(categories),
            shadow=True,
            pctdistance=0.85
        )

        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(13)

        # Enhanced title
        title_text = f'MOIRAGUARD IoT Device Distribution\n{scan_data.country_name} | Total: {total:,} Devices\n{scan_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
        ax1.set_title(title_text, fontsize=20, fontweight='bold', pad=35, color='#2c3e50')

        # Add logo if available
        if logo_img is not None:
            imagebox = OffsetImage(logo_img, zoom=0.12)
            ab = AnnotationBbox(imagebox, (1.35, 1.15), frameon=False,
                               xycoords='axes fraction')
            ax1.add_artist(ab)

        # Professional footer
        fig1.text(0.5, 0.02, '👁️ MOIRAGUARD Eye-O-Tea Scanner | DEFCON GROUP CASABLANCA 2026 | @MLY',
                 ha='center', fontsize=11, style='italic', color='#7f8c8d')

        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        pie_file = output_dir / f"moiraguard_pie_chart_{timestamp}.png"
        plt.savefig(pie_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print_status('success', f"Pie chart exported: {Colors.CYAN}{pie_file.name}{Colors.END}")

        # 2. BAR CHART - Category Comparison (Improved)
        fig2, ax2 = plt.subplots(figsize=(16, 10), facecolor='white')

        bars = ax2.bar(
            range(len(categories)), counts,
            color=colors,
            edgecolor='#2c3e50',
            linewidth=2,
            alpha=0.85,
            width=0.7
        )

        # Style axes
        ax2.set_xlabel('IoT Device Category', fontsize=15, fontweight='bold', color='#2c3e50', labelpad=10)
        ax2.set_ylabel('Number of Exposed Devices', fontsize=15, fontweight='bold', color='#2c3e50', labelpad=10)
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories, rotation=30, ha='right', fontsize=12, weight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        ax2.grid(axis='y', alpha=0.25, linestyle='--', linewidth=0.8, color='#95a5a6')
        ax2.set_axisbelow(True)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Enhanced title
        title_text = f'MOIRAGUARD IoT Exposure by Category\n{scan_data.country_name} | Total: {total:,} Devices | {scan_data.timestamp.strftime("%Y-%m-%d %H:%M")}'
        ax2.set_title(title_text, fontsize=20, fontweight='bold', pad=35, color='#2c3e50')

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2., height + (max(counts) * 0.015),
                f'{count:,}',
                ha='center', va='bottom',
                fontsize=12, fontweight='bold',
                color='#2c3e50'
            )

        # Add logo
        if logo_img is not None:
            imagebox = OffsetImage(logo_img, zoom=0.1)
            ab = AnnotationBbox(imagebox, (1.08, 1.08), frameon=False,
                               xycoords='axes fraction')
            ax2.add_artist(ab)

        # Footer
        fig2.text(0.5, 0.02, '👁️ MOIRAGUARD Eye-O-Tea Scanner | DEFCON GROUP CASABLANCA 2026 | @MLY',
                 ha='center', fontsize=11, style='italic', color='#7f8c8d')

        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        bar_file = output_dir / f"moiraguard_bar_chart_{timestamp}.png"
        plt.savefig(bar_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print_status('success', f"Bar chart exported: {Colors.CYAN}{bar_file.name}{Colors.END}")

        # 3. RISK LEVEL DOUGHNUT CHART
        risk_levels = {
            'Smart Home Devices': 'HIGH',
            'IoT Cameras': 'CRITICAL',
            'SCADA/ICS': 'CRITICAL',
            'Building Automation': 'HIGH',
            'MQTT Brokers': 'HIGH',
            'Industrial IoT': 'CRITICAL'
        }

        risk_data = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0}
        for cat, count in zip(categories, counts):
            risk = risk_levels.get(cat, 'MEDIUM')
            risk_data[risk] += count

        # Filter out zero values
        risk_labels = [k for k, v in risk_data.items() if v > 0]
        risk_values = [v for v in risk_data.values() if v > 0]
        risk_colors = {'CRITICAL': '#DC143C', 'HIGH': '#FF8C00', 'MEDIUM': '#FFD700'}
        risk_chart_colors = [risk_colors[label] for label in risk_labels]

        # 3. RISK LEVEL DOUGHNUT CHART (Improved)
        fig3, ax3 = plt.subplots(figsize=(14, 10), facecolor='white')

        wedges, texts, autotexts = ax3.pie(
            risk_values, labels=risk_labels,
            colors=risk_chart_colors,
            autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=4),
            textprops={'fontsize': 14, 'weight': 'bold'},
            explode=[0.05] * len(risk_labels),
            shadow=True
        )

        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(15)

        # Enhanced title
        title_text = f'MOIRAGUARD Risk Level Distribution\n{scan_data.country_name} | Total: {total:,} Devices\n{scan_data.timestamp.strftime("%Y-%m-%d")}'
        ax3.set_title(title_text, fontsize=20, fontweight='bold', pad=35, color='#2c3e50')

        # Add center text in doughnut
        centre_circle = plt.Circle((0, 0), 0.60, fc='white', linewidth=0)
        ax3.add_artist(centre_circle)
        ax3.text(0, 0.05, f'{total:,}', ha='center', va='center',
                fontsize=24, weight='bold', color='#2c3e50')
        ax3.text(0, -0.12, 'Devices', ha='center', va='center',
                fontsize=16, weight='bold', color='#7f8c8d')

        # Enhanced legend
        legend_labels = [f'{label}: {value:,} devices ({value/total*100:.1f}%)'
                        for label, value in zip(risk_labels, risk_values)]
        legend = ax3.legend(legend_labels, loc='upper left', bbox_to_anchor=(1.02, 1),
                           fontsize=13, frameon=True, shadow=True, fancybox=True)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_alpha(0.95)
        legend.get_frame().set_edgecolor('#95a5a6')

        # Add logo
        if logo_img is not None:
            imagebox = OffsetImage(logo_img, zoom=0.1)
            ab = AnnotationBbox(imagebox, (1.3, 1.15), frameon=False,
                               xycoords='axes fraction')
            ax3.add_artist(ab)

        # Footer
        fig3.text(0.5, 0.02, '👁️ MOIRAGUARD Eye-O-Tea Scanner | DEFCON GROUP CASABLANCA 2026 | @MLY',
                 ha='center', fontsize=11, style='italic', color='#7f8c8d')

        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        risk_file = output_dir / f"moiraguard_risk_chart_{timestamp}.png"
        plt.savefig(risk_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print_status('success', f"Risk chart exported: {Colors.CYAN}{risk_file.name}{Colors.END}")

        # 4. COMBINED SUMMARY CHART (Improved)
        fig4 = plt.figure(figsize=(22, 13), facecolor='white')

        # Add logo at top center if available
        if logo_img is not None:
            ax_logo = fig4.add_axes([0.42, 0.93, 0.16, 0.07])
            ax_logo.imshow(logo_img)
            ax_logo.axis('off')

        # Device distribution pie chart
        ax4_1 = plt.subplot(2, 2, 1)
        wedges, texts, autotexts = ax4_1.pie(
            counts, labels=categories, colors=colors,
            autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'},
            explode=[0.02] * len(categories),
            shadow=True
        )
        ax4_1.set_title('Device Distribution by Category', fontsize=15, fontweight='bold',
                       pad=15, color='#2c3e50')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)

        # Risk level doughnut chart
        ax4_2 = plt.subplot(2, 2, 2)
        wedges, texts, autotexts = ax4_2.pie(
            risk_values, labels=risk_labels,
            colors=risk_chart_colors,
            autopct='%1.1f%%', startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'},
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
            explode=[0.05] * len(risk_labels),
            shadow=True
        )
        ax4_2.set_title('Risk Level Distribution', fontsize=15, fontweight='bold',
                       pad=15, color='#2c3e50')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(13)

        # Center circle for doughnut
        centre_circle = plt.Circle((0, 0), 0.40, fc='white', linewidth=0)
        ax4_2.add_artist(centre_circle)
        ax4_2.text(0, 0, f'{total:,}', ha='center', va='center',
                  fontsize=18, weight='bold', color='#2c3e50')

        # Horizontal bar chart at bottom
        ax4_3 = plt.subplot(2, 1, 2)
        bars = ax4_3.barh(categories, counts, color=colors,
                         edgecolor='#2c3e50', linewidth=1.5, alpha=0.85)
        ax4_3.set_xlabel('Number of Exposed Devices', fontsize=14, fontweight='bold',
                        color='#2c3e50', labelpad=10)
        ax4_3.set_title('Detailed Category Breakdown', fontsize=15, fontweight='bold',
                       pad=15, color='#2c3e50')
        ax4_3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        ax4_3.grid(axis='x', alpha=0.2, linestyle='--', color='#95a5a6')
        ax4_3.set_axisbelow(True)
        ax4_3.spines['top'].set_visible(False)
        ax4_3.spines['right'].set_visible(False)

        # Add value labels
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax4_3.text(width + (max(counts) * 0.01), bar.get_y() + bar.get_height()/2,
                      f'{count:,}',
                      ha='left', va='center', fontsize=11, fontweight='bold', color='#2c3e50')

        # Main title
        main_title = f'MOIRAGUARD IoT Security Scan Summary\n{scan_data.country_name} | Total: {total:,} Devices | {scan_data.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
        fig4.suptitle(main_title, fontsize=22, fontweight='bold', y=0.985, color='#2c3e50')

        # Footer with branding
        fig4.text(0.5, 0.005,
                 f'👁️ Generated by MOIRAGUARD Eye-O-Tea Scanner | DEFCON GROUP CASABLANCA 2026 | Author: @MLY\n'
                 f'⚠️ For Security Research & Educational Purposes Only ⚠️',
                 ha='center', fontsize=11, style='italic', color='#7f8c8d')

        plt.tight_layout(rect=[0, 0.02, 1, 0.97])
        summary_file = output_dir / f"moiraguard_summary_{timestamp}.png"
        plt.savefig(summary_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        print_status('success', f"Summary chart exported: {Colors.CYAN}{summary_file.name}{Colors.END}")

        print_status('success', f"All PNG charts exported to: {Colors.CYAN}{output_dir}{Colors.END}")
        return [pie_file, bar_file, risk_file, summary_file]

    except Exception as e:
        print_status('error', f"PNG export failed: {Colors.RED}{e}{Colors.END}")
        return None

def export_html_with_charts(scan_data, verbose=False):
    """Export scan results to HTML with embedded charts"""
    try:
        output_dir = create_output_directory()
        timestamp = scan_data.timestamp.strftime('%Y%m%d_%H%M%S')
        filename = f"moiraguard_scan_{timestamp}.html"
        filepath = output_dir / filename

        # Prepare data for charts
        categories = list(scan_data.categories.keys())
        counts = [scan_data.categories[cat]['count'] for cat in categories]
        total = sum(counts)

        # Enhanced color scheme - distinct colors for each category
        colors_map = {
            'Smart Home Devices': '#00a8e8',    # Cyan Blue (IoT theme)
            'IoT Cameras': '#DC143C',           # Crimson Red (Critical)
            'SCADA/ICS': '#8B0000',             # Dark Red (Critical)
            'Building Automation': '#9C27B0',   # Purple (Control Systems)
            'MQTT Brokers': '#FF6F00',          # Deep Orange (Messaging)
            'Industrial IoT': '#1B5E20'         # Dark Green (Industrial)
        }
        chart_colors = [colors_map.get(cat, '#4682B4') for cat in categories]

        # Load and encode logo as base64
        logo_base64 = ""
        logo_path = Path("MoiraGuard-Eye-O-Tea-logo.png")
        if logo_path.exists():
            try:
                with open(logo_path, 'rb') as logo_file:
                    logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            except Exception:
                pass

        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MOIRAGUARD Scan Report - {scan_data.timestamp.strftime('%Y-%m-%d')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* 👁️ MOIRAGUARD Eye O Tea - Cyber-Mystic Neon Theme */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Rajdhani', 'Orbitron', 'Segoe UI', sans-serif;
            background: #05070B;
            color: #E6F0F5;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }}

        /* Animated circuit pattern background */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
                radial-gradient(circle at 20% 30%, rgba(0, 255, 136, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(0, 201, 107, 0.06) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(0, 255, 170, 0.03) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
            animation: pulseGlow 8s ease-in-out infinite;
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 0.8; }}
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(11, 18, 32, 0.95);
            border-radius: 20px;
            box-shadow:
                0 25px 70px rgba(0, 0, 0, 0.6),
                0 0 40px rgba(0, 255, 136, 0.15),
                inset 0 0 60px rgba(0, 255, 136, 0.02);
            overflow: hidden;
            position: relative;
            z-index: 1;
            border: 1px solid rgba(0, 255, 136, 0.3);
            backdrop-filter: blur(10px);
        }}

        /* Neon header with eye effect gradient */
        .header {{
            background: linear-gradient(135deg, #02140F 0%, #052E23 100%);
            color: #E6F0F5;
            padding: 50px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-bottom: 2px solid #00FF88;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, rgba(0, 255, 170, 0.15) 0%, rgba(0, 59, 46, 0.1) 40%, transparent 70%);
            pointer-events: none;
            animation: eyePulse 6s ease-in-out infinite;
        }}

        @keyframes eyePulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.3; }}
            50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; }}
        }}

        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 15px;
            background: linear-gradient(180deg, #FFFFFF 0%, #BFC9D4 50%, #7A8A99 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
            position: relative;
            z-index: 1;
            font-weight: 900;
            letter-spacing: 2px;
        }}

        .header .subtitle {{
            font-size: 1.3em;
            position: relative;
            z-index: 1;
            color: #00FF88;
            text-shadow: 0 0 15px rgba(0, 255, 136, 0.8), 0 0 30px rgba(0, 201, 107, 0.4);
            font-weight: 600;
            letter-spacing: 1px;
        }}

        /* Critical warning banner */
        .warning-banner {{
            background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
            color: white;
            padding: 18px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            box-shadow: 0 0 20px rgba(220, 20, 60, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* Glassmorphic meta cards */
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            padding: 40px;
            background: linear-gradient(135deg, rgba(11, 18, 32, 0.6) 0%, rgba(5, 46, 35, 0.4) 100%);
        }}

        .meta-card {{
            background: rgba(0, 255, 136, 0.05);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            text-align: center;
            border: 1px solid rgba(0, 255, 136, 0.3);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }}

        .meta-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
            transition: left 0.5s;
        }}

        .meta-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.4);
            border-color: #00FF88;
        }}

        .meta-card:hover::before {{
            left: 100%;
        }}

        .meta-card .label {{
            color: #A7B8C5;
            font-size: 0.85em;
            margin-bottom: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .meta-card .value {{
            color: #00FF88;
            font-size: 2em;
            font-weight: bold;
            text-shadow: 0 0 15px rgba(0, 255, 136, 0.6);
            font-family: 'Orbitron', monospace;
        }}
        /* Neon chart sections */
        .charts-section {{
            padding: 50px 40px;
            background: linear-gradient(135deg, rgba(5, 7, 11, 0.9) 0%, rgba(11, 18, 32, 0.9) 100%);
        }}

        .chart-container {{
            margin-bottom: 50px;
            background: rgba(0, 255, 136, 0.03);
            padding: 35px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(0, 255, 136, 0.2);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            position: relative;
        }}

        .chart-container::before {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, #00FF88 0%, #00C96B 50%, #007A4D 100%);
            border-radius: 15px;
            opacity: 0;
            z-index: -1;
            transition: opacity 0.3s;
        }}

        .chart-container:hover {{
            box-shadow: 0 0 40px rgba(0, 255, 136, 0.3);
            transform: translateY(-3px);
        }}

        .chart-container:hover::before {{
            opacity: 0.3;
        }}

        .chart-title {{
            font-size: 1.7em;
            color: #E6F0F5;
            margin-bottom: 25px;
            text-align: center;
            font-weight: 700;
            position: relative;
            padding-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .chart-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #00FF88 0%, #00C96B 50%, #007A4D 100%);
            border-radius: 2px;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}

        /* Neon stat cards */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            padding: 40px;
            background: linear-gradient(135deg, rgba(2, 20, 15, 0.6) 0%, rgba(5, 46, 35, 0.4) 100%);
        }}

        .stat-card {{
            background: rgba(0, 255, 136, 0.05);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            border-left: 4px solid;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(0, 255, 136, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            animation: rotatePulse 10s linear infinite;
        }}

        @keyframes rotatePulse {{
            0% {{ transform: rotate(0deg) scale(1); }}
            50% {{ transform: rotate(180deg) scale(1.2); }}
            100% {{ transform: rotate(360deg) scale(1); }}
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        }}

        .stat-card.critical {{
            border-left-color: #DC143C;
            box-shadow: 0 8px 32px rgba(220, 20, 60, 0.2);
        }}
        .stat-card.high {{
            border-left-color: #FF6F00;
            box-shadow: 0 8px 32px rgba(255, 111, 0, 0.2);
        }}
        .stat-card.medium {{
            border-left-color: #FFD700;
            box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
        }}

        .stat-card h3 {{
            color: #E6F0F5;
            font-size: 1.15em;
            margin-bottom: 15px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .stat-card .count {{
            font-size: 3em;
            font-weight: bold;
            color: #00FF88;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
            font-family: 'Orbitron', monospace;
        }}

        .stat-card .risk {{
            margin-top: 12px;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            font-size: 0.9em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .risk.critical {{
            background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
            color: white;
            box-shadow: 0 0 15px rgba(220, 20, 60, 0.5);
        }}
        .risk.high {{
            background: linear-gradient(135deg, #FF6F00 0%, #CC5500 100%);
            color: white;
            box-shadow: 0 0 15px rgba(255, 111, 0, 0.5);
        }}
        .risk.medium {{
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        }}
        .devices-table {{
            width: 100%;
            margin: 30px;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #2a5298;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        /* Neon footer */
        .footer {{
            background: linear-gradient(135deg, #02140F 0%, #052E23 100%);
            color: #E6F0F5;
            padding: 35px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-top: 2px solid #00FF88;
        }}

        .footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                radial-gradient(circle at 30% 50%, rgba(0, 255, 136, 0.1) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(0, 201, 107, 0.08) 0%, transparent 60%);
            pointer-events: none;
        }}

        .footer p {{
            position: relative;
            z-index: 1;
            margin: 10px 0;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
            letter-spacing: 1px;
        }}

        canvas {{
            max-height: 450px;
        }}

        /* Neon table styling */
        .devices-table {{
            margin: 40px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(11, 18, 32, 0.8);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(0, 255, 136, 0.2);
        }}

        th {{
            background: linear-gradient(135deg, #02140F 0%, #00FF88 100%);
            color: #05070B;
            padding: 18px 15px;
            text-align: left;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-size: 0.9em;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}

        td {{
            padding: 15px;
            border-bottom: 1px solid rgba(0, 255, 136, 0.1);
            color: #A7B8C5;
            font-family: 'Courier New', monospace;
        }}

        tr:hover {{
            background: rgba(0, 255, 136, 0.08);
        }}

        tr:hover td {{
            color: #00FF88;
            text-shadow: 0 0 5px rgba(0, 255, 136, 0.3);
        }}

        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}

        ::-webkit-scrollbar-track {{
            background: #0B1220;
        }}

        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #00FF88 0%, #00C96B 100%);
            border-radius: 6px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #00FFAA 0%, #00FF88 100%);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            {f'<img src="data:image/png;base64,{logo_base64}" alt="MOIRAGUARD Logo" style="max-width: 300px; margin-bottom: 20px;">' if logo_base64 else ''}
            <h1>👁️ MOIRAGUARD Eye-O-Tea Scanner</h1>
            <div class="subtitle">IoT/IIoT Infrastructure Security Scan Report</div>
        </div>

        <div class="warning-banner">
            ⚠️ CONFIDENTIAL SECURITY REPORT - For Authorized Personnel Only ⚠️
        </div>

        <div class="meta-info">
            <div class="meta-card">
                <div class="label">Scan Date</div>
                <div class="value">{scan_data.timestamp.strftime('%Y-%m-%d')}</div>
            </div>
            <div class="meta-card">
                <div class="label">Scan Time</div>
                <div class="value">{scan_data.timestamp.strftime('%H:%M:%S')}</div>
            </div>
            <div class="meta-card">
                <div class="label">Target Region</div>
                <div class="value">{scan_data.country_name}</div>
            </div>
            <div class="meta-card">
                <div class="label">Total Devices</div>
                <div class="value">{total:,}</div>
            </div>
        </div>

        <div class="stats-grid">
"""

        # Add individual category cards
        risk_levels = {
            'Smart Home Devices': ('HIGH', 'high'),
            'IoT Cameras': ('CRITICAL', 'critical'),
            'SCADA/ICS': ('CRITICAL', 'critical'),
            'Building Automation': ('HIGH', 'high'),
            'MQTT Brokers': ('HIGH', 'high'),
            'Industrial IoT': ('CRITICAL', 'critical')
        }

        for category, data in scan_data.categories.items():
            risk_text, risk_class = risk_levels.get(category, ('MEDIUM', 'medium'))
            html_content += f"""
            <div class="stat-card {risk_class}">
                <h3>{category}</h3>
                <div class="count">{data['count']:,}</div>
                <span class="risk {risk_class}">{risk_text}</span>
            </div>
"""

        html_content += """
        </div>

        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📊 Device Distribution by Category</div>
                <canvas id="categoryChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">📈 Exposure by Category (Bar Chart)</div>
                <canvas id="barChart"></canvas>
            </div>

            <div class="chart-container">
                <div class="chart-title">🎯 Risk Level Distribution</div>
                <canvas id="riskChart"></canvas>
            </div>
        </div>
"""

        # Add detailed devices table if verbose
        if verbose:
            html_content += """
        <div class="devices-table">
            <h2 style="margin-bottom: 20px; color: #2a5298;">🔍 Detailed Device Information</h2>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>IP Address</th>
                        <th>Port</th>
                        <th>Product</th>
                        <th>Country</th>
                        <th>City</th>
                        <th>Organization</th>
                    </tr>
                </thead>
                <tbody>
"""
            for category, data in scan_data.categories.items():
                for device in data['devices'][:50]:  # Limit to first 50 per category
                    html_content += f"""
                    <tr>
                        <td>{category}</td>
                        <td><code>{device.get('ip', 'N/A')}</code></td>
                        <td>{device.get('port', 'N/A')}</td>
                        <td>{device.get('product', 'N/A')}</td>
                        <td>{device.get('country', 'N/A')}</td>
                        <td>{device.get('city', 'N/A')}</td>
                        <td>{device.get('org', 'N/A')}</td>
                    </tr>
"""
            html_content += """
                </tbody>
            </table>
        </div>
"""

        html_content += f"""
        <div class="footer">
            <p>Generated by MOIRAGUARD Eye-O-Tea Scanner | DEFCON GROUP CASANLANCA 2026</p>
            <p>Author: Mohammed Amine Moulay (@MLY)</p>
            <p style="margin-top: 10px; font-size: 0.9em;">⚠️ For Security Research & Educational Purposes Only ⚠️</p>
        </div>
    </div>

    <script>
        // Category Pie Chart
        // Category Pie Chart with Enhanced Colors
        const ctx1 = document.getElementById('categoryChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(categories)},
                datasets: [{{
                    data: {json.dumps(counts)},
                    backgroundColor: {json.dumps(chart_colors)},
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 4,
                    hoverBorderColor: '#00f2fe',
                    hoverOffset: 15
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            font: {{
                                size: 13,
                                weight: 'bold',
                                family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                            }},
                            color: '#0a192f',
                            usePointStyle: true,
                            pointStyle: 'circle',
                            boxWidth: 15,
                            boxHeight: 15
                        }}
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(10, 25, 47, 0.95)',
                        titleColor: '#00f2fe',
                        bodyColor: '#fff',
                        borderColor: '#00a8e8',
                        borderWidth: 2,
                        padding: 12,
                        titleFont: {{
                            size: 14,
                            weight: 'bold'
                        }},
                        bodyFont: {{
                            size: 13
                        }},
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                let value = context.parsed || 0;
                                let total = context.dataset.data.reduce((a, b) => a + b, 0);
                                let percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }},
                animation: {{
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500
                }}
            }}
        }});

        // Bar Chart
        // Bar Chart with Enhanced Styling
        const ctx2 = document.getElementById('barChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(categories)},
                datasets: [{{
                    label: 'Exposed Devices',
                    data: {json.dumps(counts)},
                    backgroundColor: {json.dumps(chart_colors)},
                    borderWidth: 2,
                    borderColor: {json.dumps(chart_colors)},
                    borderRadius: 8,
                    hoverBackgroundColor: {json.dumps([c + 'dd' for c in chart_colors])},
                    hoverBorderColor: '#00f2fe',
                    hoverBorderWidth: 3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(10, 25, 47, 0.95)',
                        titleColor: '#00f2fe',
                        bodyColor: '#fff',
                        borderColor: '#00a8e8',
                        borderWidth: 2,
                        padding: 12,
                        titleFont: {{
                            size: 14,
                            weight: 'bold'
                        }},
                        bodyFont: {{
                            size: 13
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(0, 168, 232, 0.1)',
                            lineWidth: 1
                        }},
                        ticks: {{
                            color: '#0a192f',
                            font: {{
                                size: 12,
                                weight: 'bold'
                            }},
                            callback: function(value) {{
                                return value.toLocaleString();
                            }}
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }},
                        ticks: {{
                            color: '#0a192f',
                            font: {{
                                size: 12,
                                weight: 'bold'
                            }}
                        }}
                    }}
                }},
                animation: {{
                    duration: 1500,
                    easing: 'easeOutQuart'
                }}
            }}
        }});

        // Risk Level Doughnut Chart
        const riskData = {{
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0
        }};

        const riskMap = {json.dumps(dict(zip(categories, [risk_levels.get(cat, ('MEDIUM', 'medium'))[0] for cat in categories])))};
        const countMap = {json.dumps(dict(zip(categories, counts)))};

        for (let cat in riskMap) {{
            riskData[riskMap[cat]] += countMap[cat];
        }}

        const ctx3 = document.getElementById('riskChart').getContext('2d');
        new Chart(ctx3, {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(riskData),
                datasets: [{{
                    data: Object.values(riskData),
                    backgroundColor: ['#DC143C', '#FF8C00', '#FFD700'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 15,
                            font: {{
                                size: 12
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                let value = context.parsed || 0;
                                let total = context.dataset.data.reduce((a, b) => a + b, 0);
                                let percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

        with open(filepath, 'w') as f:
            f.write(html_content)

        print_status('success', f"HTML report exported to: {Colors.CYAN}{filepath}{Colors.END}")
        return filepath
    except Exception as e:
        print_status('error', f"HTML export failed: {Colors.RED}{e}{Colors.END}")
        return None

def export_html_as_png(scan_data, verbose=False):
    """Export HTML report as a long PNG screenshot"""
    try:
        if not HTML2IMAGE_AVAILABLE:
            print_status('error', "html2image library not installed")
            print_status('info', f"Install with: {Colors.CYAN}pip3 install html2image{Colors.END}")
            return None

        output_dir = create_output_directory()
        timestamp = scan_data.timestamp.strftime('%Y%m%d_%H%M%S')

        # First generate the HTML file
        print_status('info', "Generating HTML report...")
        html_file = export_html_with_charts(scan_data, verbose)

        if not html_file:
            print_status('error', "Failed to generate HTML")
            return None

        # Convert HTML to PNG
        print_status('info', "Converting HTML to PNG (this may take a moment)...")
        loading_animation("Rendering HTML as image", 2)

        # Generate PNG filename
        png_filename = f"moiraguard_report_{timestamp}.png"

        # Initialize Html2Image with fixed viewport size
        # The library will capture the full scrollable content
        try:
            hti = Html2Image(output_path=str(output_dir))

            # Read HTML content for inline rendering
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Screenshot with html_str and explicit size
            hti.screenshot(
                html_str=html_content,
                save_as=png_filename,
                size=(1400, 8000)  # Wide viewport to capture full page
            )
        except TypeError:
            # Fallback: try with file path if html_str fails
            hti = Html2Image(output_path=str(output_dir))
            hti.screenshot(
                html_file=str(html_file),
                save_as=png_filename,
                size=(1400, 8000)
            )

        png_file = output_dir / png_filename

        if png_file.exists():
            # Get file size for display
            file_size = png_file.stat().st_size / (1024 * 1024)  # MB
            print_status('success', f"HTML screenshot exported: {Colors.CYAN}{png_filename}{Colors.END}")
            print_status('info', f"File size: {Colors.GREEN}{file_size:.2f} MB{Colors.END}")
            return png_file
        else:
            print_status('error', "PNG file was not created")
            return None

    except Exception as e:
        print_status('error', f"HTML to PNG export failed: {Colors.RED}{e}{Colors.END}")
        print_status('info', "Make sure Chrome/Chromium is installed on your system")
        print_status('info', f"Install Chrome/Chromium with:")
        print(f"  {Colors.CYAN}• Ubuntu/Debian:{Colors.END} sudo apt install chromium-browser")
        print(f"  {Colors.CYAN}• Fedora/RHEL:{Colors.END} sudo dnf install chromium")
        print(f"  {Colors.CYAN}• Arch:{Colors.END} sudo pacman -S chromium")
        print(f"  {Colors.CYAN}• macOS:{Colors.END} brew install chromium")
        print_status('info', f"HTML file was saved successfully at: {Colors.CYAN}{html_file}{Colors.END}")
        return None

def post_scan_menu(scan_data):
    """Display post-scan options menu"""
    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}            {Colors.WHITE}POST-SCAN OPTIONS{Colors.END}                    {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")

        print(f"{Colors.MAGENTA}[V]{Colors.END} {Colors.BOLD}Verify Exposure{Colors.END} {Colors.DIM}— Active protocol probing (confirms unauthenticated access, 0 credits){Colors.END}")
        print_separator('─', 60, Colors.DIM)
        print(f"{Colors.GREEN}[1]{Colors.END} Export to JSON {Colors.DIM}(Metrics Only){Colors.END}")
        print(f"{Colors.GREEN}[2]{Colors.END} Export to JSON {Colors.DIM}(Verbose - with IP addresses){Colors.END}")
        print(f"{Colors.GREEN}[3]{Colors.END} Export to CSV {Colors.DIM}(Metrics Only){Colors.END}")
        print(f"{Colors.GREEN}[4]{Colors.END} Export to CSV {Colors.DIM}(Verbose - with device details){Colors.END}")
        print(f"{Colors.GREEN}[5]{Colors.END} Export to HTML with Charts {Colors.DIM}(Metrics Only){Colors.END}")
        print(f"{Colors.GREEN}[6]{Colors.END} Export to HTML with Charts {Colors.DIM}(Verbose - with device table){Colors.END}")
        print(f"{Colors.GREEN}[7]{Colors.END} Export Charts as PNG {Colors.DIM}(4 chart images){Colors.END}")
        print(f"{Colors.GREEN}[8]{Colors.END} Export HTML as Long PNG {Colors.DIM}(Full page screenshot - Metrics){Colors.END}")
        print(f"{Colors.GREEN}[9]{Colors.END} Export HTML as Long PNG {Colors.DIM}(Full page screenshot - Verbose){Colors.END}")
        print(f"{Colors.GREEN}[10]{Colors.END} Export ALL formats {Colors.DIM}(Metrics Only){Colors.END}")
        print(f"{Colors.GREEN}[11]{Colors.END} Export ALL formats + Screenshots {Colors.DIM}(Verbose){Colors.END}")
        print(f"{Colors.YELLOW}[0]{Colors.END} {Colors.DIM}Exit{Colors.END}")

        print_separator('─', 60, Colors.DIM)

        try:
            choice = input(f"\n{Colors.BOLD}Select option: {Colors.END}").strip()

            if choice == '0':
                print_status('info', "Exiting MOIRAGUARD...")
                break
            elif choice.upper() == 'V':
                verify_exposure(scan_data)
            elif choice == '1':
                export_json(scan_data, verbose=False)
            elif choice == '2':
                export_json(scan_data, verbose=True)
            elif choice == '3':
                export_csv(scan_data, verbose=False)
            elif choice == '4':
                export_csv(scan_data, verbose=True)
            elif choice == '5':
                export_html_with_charts(scan_data, verbose=False)
            elif choice == '6':
                export_html_with_charts(scan_data, verbose=True)
            elif choice == '7':
                export_png_charts(scan_data)
            elif choice == '8':
                export_html_as_png(scan_data, verbose=False)
            elif choice == '9':
                export_html_as_png(scan_data, verbose=True)
            elif choice == '10':
                print_status('info', "Exporting all formats (metrics only)...")
                export_json(scan_data, verbose=False)
                export_csv(scan_data, verbose=False)
                export_html_with_charts(scan_data, verbose=False)
                print_status('success', "All formats exported successfully!")
            elif choice == '11':
                print_status('info', "Exporting all formats + screenshots (verbose mode)...")
                export_json(scan_data, verbose=True)
                export_csv(scan_data, verbose=True)
                export_html_with_charts(scan_data, verbose=True)
                export_png_charts(scan_data)
                export_html_as_png(scan_data, verbose=True)
                print_status('success', "All formats and screenshots exported successfully!")
            else:
                print_status('error', "Invalid option. Please try again.")

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Menu interrupted{Colors.END}")
            break
        except Exception as e:
            print_status('error', f"Error: {Colors.RED}{e}{Colors.END}")

# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    SUMMARY & REPORTING                            ║
# ╚═══════════════════════════════════════════════════════════════════╝

def print_summary(stats, api=None, target_country=None):
    """Print MOIRAGUARD summary with target country context"""
    total_devices = sum(stats.values())

    print("\n")
    print_separator('═', 70, Colors.CYAN)
    print(f"{Colors.BOLD}{Colors.CYAN}╔{'═' * 68}╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}{Colors.BOLD}{Colors.WHITE}{'MOIRAGUARD RECONNAISSANCE COMPLETE'.center(68)}{Colors.END}{Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚{'═' * 68}╝{Colors.END}")
    print_separator('═', 70, Colors.CYAN)

    # Target scope
    if target_country and target_country != "Global":
        print(f"\n{Colors.BOLD}{Colors.CYAN}Target Scope:{Colors.END} {Colors.YELLOW}{target_country}{Colors.END}")
    else:
        print(f"\n{Colors.BOLD}{Colors.CYAN}Target Scope:{Colors.END} {Colors.YELLOW}Global (All Countries){Colors.END}")
    
    # Total count
    print(f"\n{Colors.BOLD}{Colors.WHITE}Total Exposed Systems Discovered:{Colors.END}")
    print(f"{Colors.BOLD}{Colors.RED}{Colors.UNDERLINE}{total_devices:,}{Colors.END} {Colors.WHITE}IoT/IIoT/SCADA systems globally accessible{Colors.END}\n")
    
    # Category breakdown
    print(f"{Colors.BOLD}{Colors.CYAN}Exposure Breakdown by Category:{Colors.END}\n")
    for category, count in stats.items():
        percentage = (count / total_devices * 100) if total_devices > 0 else 0
        bar_length = int(percentage / 2)
        bar = '█' * bar_length
        
        if 'SCADA' in category or 'Industrial' in category:
            color = Colors.RED
            risk = "CRITICAL"
        elif 'Camera' in category:
            color = Colors.ORANGE
            risk = "HIGH"
        else:
            color = Colors.YELLOW
            risk = "MEDIUM-HIGH"
        
        print(f"  {color}■{Colors.END} {category:27s} {Colors.BOLD}{color}{count:9,}{Colors.END} systems  {Colors.DIM}{bar}{Colors.END} {percentage:5.1f}% [{color}{risk}{Colors.END}]")
    
    # Critical findings
    print(f"\n{Colors.BOLD}{Colors.RED}═══ CRITICAL SECURITY FINDINGS ═══{Colors.END}\n")
    
    critical_findings = [
        (f"{total_devices:,} IoT/IIoT systems", "PUBLICLY ACCESSIBLE from internet"),
        (f"{stats.get('SCADA/ICS', 0):,} SCADA systems", "CRITICAL INFRASTRUCTURE exposed"),
        (f"{stats.get('IoT Cameras', 0):,} camera streams", "PRIVACY VIOLATIONS"),
        (f"{stats.get('MQTT Brokers', 0):,} MQTT brokers", "UNENCRYPTED messaging"),
        (f"{stats.get('Building Automation', 0):,} building systems", "PHYSICAL SECURITY bypass"),
    ]
    
    for count_text, risk_text in critical_findings:
        print(f"  {Colors.RED}⚠️{Colors.END}  {Colors.BOLD}{Colors.WHITE}{count_text:30s}{Colors.END} │ {Colors.RED}{risk_text}{Colors.END}")
    
    # MOROCCO LOCAL CONTEXT (if API available)
    if api is not None:
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}═══ LOCAL CONTEXT: MOROCCO ═══{Colors.END}\n")
        
        try:
            loading_animation("Analyzing local exposure patterns", 1)
            
            morocco_stats = {}
            
            ma_iot = api.search('port:80,8080,443 country:MA')
            morocco_stats['IoT Web Interfaces'] = ma_iot['total']
            
            ma_cameras = api.search('port:554 country:MA')
            morocco_stats['Camera Streams'] = ma_cameras['total']
            
            ma_telnet = api.search('port:23 country:MA')
            morocco_stats['Telnet Services'] = ma_telnet['total']
            
            ma_scada = api.search('port:502 country:MA')
            morocco_stats['SCADA/ICS Systems'] = ma_scada['total']
            
            print_status('found', "Morocco-specific exposure identified")
            
            print(f"\n{Colors.BOLD}Moroccan Infrastructure Exposure:{Colors.END}\n")
            for category, count in morocco_stats.items():
                print(f"  {Colors.YELLOW}►{Colors.END} {category:25s} {Colors.RED}{count:6,}{Colors.END} systems")
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}Context:{Colors.END}")
            print(f"  • Morocco faces {Colors.YELLOW}same IoT security challenges{Colors.END} as global infrastructure")
            print(f"  • Patterns: {Colors.RED}Default credentials, legacy protocols, no segmentation{Colors.END}")
            print(f"  • Solutions: {Colors.GREEN}Same defensive measures apply universally{Colors.END}")
            
            print(f"\n{Colors.DIM}This data shown for local awareness and defensive preparation.{Colors.END}")
            
        except Exception as e:
            print_status('info', "Local context analysis unavailable")
    
    # Footer
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}👁️  MOIRAGUARD Eye-O-Tea Scanner{Colors.END} {Colors.DIM}|{Colors.END} {Colors.CYAN}DEFCON GROUP CASANLANCA 2026{Colors.END} {Colors.DIM}|{Colors.END} {Colors.GREEN}@MLY{Colors.END}")
    print(f"{Colors.YELLOW}[!] Research Purpose:{Colors.END} Understanding global IoT/IIoT exposure patterns")
    print(f"{Colors.YELLOW}[!] Ethical Note:{Colors.END} PASSIVE reconnaissance only")
    print(f"{Colors.RED}[!] Legal Warning:{Colors.END} Unauthorized access is ILLEGAL")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

# ╔═══════════════════════════════════════════════════════════════════╗
# ║              ACTIVE PROTOCOL VERIFICATION ENGINE                   ║
# ╚═══════════════════════════════════════════════════════════════════╝

def _probe_mqtt(ip, port=1883, timeout=5):
    """Send anonymous MQTT CONNECT, check CONNACK return code.
    rc=0 means the broker accepted the connection without credentials."""
    try:
        client_id = b'moiravfy1'
        # MQTT 3.1.1 variable header: protocol name (6B) + level (1B) + flags (1B) + keepalive (2B)
        var_header = b'\x00\x04MQTT\x04\x00\x00\x3c'
        payload    = b'\x00\x09' + client_id          # 2-byte length prefix + client ID
        remaining  = var_header + payload
        packet     = bytes([0x10, len(remaining)]) + remaining  # CONNECT fixed header

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall(packet)
        response = s.recv(4)
        s.close()

        if len(response) >= 4 and response[0] == 0x20:
            rc = response[3]
            if rc == 0:
                return True,  'CONNACK rc=0 — anonymous access accepted'
            return False, f'CONNACK rc={rc} — broker refused (auth required)'
        return False, 'No valid CONNACK received'
    except Exception as e:
        return False, str(e)


def _probe_rtsp(ip, port=554, timeout=5):
    """Send RTSP OPTIONS * and inspect response code.
    200 = stream accessible without credentials, 401/403 = protected."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall(b'OPTIONS * RTSP/1.0\r\nCSeq: 1\r\n\r\n')
        response = s.recv(512).decode('utf-8', errors='ignore')
        s.close()

        first = response.split('\r\n')[0] if response else ''
        if '200' in first:
            return True,  'RTSP 200 OK — stream accessible without credentials'
        elif '401' in first:
            return False, 'RTSP 401 — authentication required'
        elif '403' in first:
            return False, 'RTSP 403 — forbidden'
        return False, (first.strip()[:70] or 'No response')
    except Exception as e:
        return False, str(e)


def _probe_modbus(ip, port=502, timeout=5):
    """Send Modbus TCP Read Coils (FC 0x01) request.
    Any valid Modbus response confirms the PLC is reachable and unauthenticated
    (Modbus has no auth layer — if it responds, it's open)."""
    try:
        # MBAP header (7 B): TransactionID + ProtocolID + Length + UnitID
        # PDU (5 B): FC=0x01 + StartAddr=0x0000 + Count=0x0001
        request = b'\x00\x01\x00\x00\x00\x06\x01\x01\x00\x00\x00\x01'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.sendall(request)
        response = s.recv(256)
        s.close()

        if len(response) >= 8:
            fc = response[7]
            if fc == 0x01:
                return True,  'Modbus FC01 response — PLC answers reads without auth'
            elif fc == 0x81:
                exc = response[8] if len(response) > 8 else '?'
                return True,  f'Modbus exception fc=0x81 code={exc} — PLC reachable, no transport auth'
            return True, f'Modbus response fc=0x{fc:02x} — device responding'
        return False, 'No valid Modbus response'
    except Exception as e:
        return False, str(e)


def _probe_bacnet(ip, port=47808, timeout=5):
    """Send BACnet/IP Who-Is (UDP) and listen for I-Am response.
    Any response confirms the device is reachable and unauthenticated."""
    try:
        # BACnet/IP Original-Unicast-NPDU Who-Is
        # BVLC (4B): type=0x81, func=0x0a, len=0x0008
        # NPDU (2B): version=0x01, control=0x00
        # APDU (2B): type=0x10 (Unconfirmed-Req), service=0x08 (Who-Is)
        who_is = b'\x81\x0a\x00\x08\x01\x00\x10\x08'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        s.sendto(who_is, (ip, port))
        response, _ = s.recvfrom(1024)
        s.close()

        if response:
            return True, f'BACnet I-Am received ({len(response)} bytes) — device responding'
        return False, 'Empty UDP response'
    except socket.timeout:
        return False, 'No response (timeout)'
    except Exception as e:
        return False, str(e)


def _probe_telnet(ip, port=23, timeout=5):
    """Connect to Telnet and read the login banner.
    Receiving any banner confirms the service is alive and presenting itself."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        time.sleep(0.5)
        banner = s.recv(256)
        s.close()

        if banner:
            text = banner.decode('utf-8', errors='replace').strip()[:80]
            return True, f'Telnet banner: {repr(text)}'
        return False, 'Connected but no banner received'
    except Exception as e:
        return False, str(e)


def _probe_http(ip, port=80, timeout=5):
    """Send GET / and check HTTP status code.
    200 = interface accessible without credentials.
    Handles both HTTP and HTTPS (port 443/8443)."""
    try:
        raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw.settimeout(timeout)

        if port in (443, 8443):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(raw, server_hostname=ip)
            scheme = 'HTTPS'
        else:
            s = raw
            scheme = 'HTTP'

        s.connect((ip, port))
        s.sendall(f'GET / HTTP/1.0\r\nHost: {ip}\r\nUser-Agent: MOIRAGUARD/1.0\r\nConnection: close\r\n\r\n'.encode())
        response = s.recv(512).decode('utf-8', errors='ignore')
        s.close()

        first = response.split('\r\n')[0].strip() if response else ''
        if '200' in first:
            return True,  f'{scheme} 200 — web interface accessible without auth'
        elif '401' in first:
            return False, f'{scheme} 401 — auth required'
        elif '403' in first:
            return False, f'{scheme} 403 — forbidden'
        elif '301' in first or '302' in first:
            return False, f'{scheme} redirect — likely to login page'
        return False, (first[:70] or 'No response')
    except Exception as e:
        return False, str(e)


# Maps each ScanData category → (protocol label, probe function, fallback port)
_CATEGORY_PROBERS = {
    'IoT Cameras':        ('RTSP',   _probe_rtsp,    554),
    'SCADA/ICS':          ('Modbus', _probe_modbus,  502),
    'Building Automation':('BACnet', _probe_bacnet, 47808),
    'MQTT Brokers':       ('MQTT',   _probe_mqtt,   1883),
    'Smart Home Devices': ('HTTP',   _probe_http,     80),
    'Industrial IoT':     ('HTTP',   _probe_http,     80),
}


def verify_exposure(scan_data):
    """Actively probe IPs collected during Verbose scan to confirm
    each device is genuinely accessible without credentials.
    Uses direct TCP/UDP sockets — zero Shodan credits consumed."""

    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}     {Colors.WHITE}ACTIVE PROTOCOL VERIFICATION ENGINE{Colors.END}           {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")

    # Require verbose scan data
    total_ips = sum(len(cat['devices']) for cat in scan_data.categories.values())
    if total_ips == 0:
        print_status('warning', "No device IPs found in scan data.")
        print_status('info', "Re-run Query Mode with Verbose mode selected to collect IPs.")
        return

    print_status('warning', f"{Colors.YELLOW}This makes DIRECT TCP/UDP connections to discovered IPs.{Colors.END}")
    print_status('info',    "Only probe systems you are authorised to test.")
    print_status('info',    f"{Colors.CYAN}{total_ips}{Colors.END} IPs available across "
                            f"{Colors.CYAN}{len([c for c in scan_data.categories.values() if c['devices']])}{Colors.END} categories.")
    print_separator('─', 60, Colors.DIM)

    try:
        confirm = input(f"\n{Colors.BOLD}Proceed with active verification? [Y/n]: {Colors.END}").strip().lower()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
        return
    if confirm not in ('', 'y', 'yes'):
        print_status('info', "Verification cancelled.")
        return

    try:
        limit_raw = input(f"{Colors.BOLD}Max IPs to probe per category [{Colors.CYAN}10{Colors.END}{Colors.BOLD}]: {Colors.END}").strip()
        max_per_cat = int(limit_raw) if limit_raw.isdigit() and int(limit_raw) > 0 else 10
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
        return

    print_separator('─', 60, Colors.DIM)

    grand_probed    = 0
    grand_confirmed = 0
    verification_results = {}

    for category, (proto_label, probe_fn, fallback_port) in _CATEGORY_PROBERS.items():
        devices = scan_data.categories.get(category, {}).get('devices', [])
        if not devices:
            continue

        targets = devices[:max_per_cat]
        print(f"\n{Colors.BOLD}{Colors.CYAN}[{proto_label}]{Colors.END} "
              f"{Colors.WHITE}{category}{Colors.END} — probing {Colors.CYAN}{len(targets)}{Colors.END} IP(s)")
        print_separator('─', 50, Colors.DIM)

        cat_results    = []
        cat_confirmed  = 0

        # Capture loop variables for the closure
        _probe  = probe_fn
        _fport  = fallback_port

        def _task(device, probe=_probe, fport=_fport):
            ip   = device.get('ip', '')
            port = device.get('port', fport)
            if not isinstance(port, int):
                port = fport
            if not ip:
                return ip, port, False, 'No IP stored'
            ok, detail = probe(ip, port)
            return ip, port, ok, detail

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            futures = {pool.submit(_task, dev): dev for dev in targets}
            for future in concurrent.futures.as_completed(futures):
                ip, port, ok, detail = future.result()
                cat_results.append({'ip': ip, 'port': port, 'confirmed': ok, 'detail': detail})
                if ok:
                    cat_confirmed += 1
                    print(f"  {Colors.GREEN}[CONFIRMED]{Colors.END} "
                          f"{Colors.WHITE}{ip}:{port}{Colors.END}  "
                          f"{Colors.DIM}{detail}{Colors.END}")
                else:
                    print(f"  {Colors.DIM}[protected]{Colors.END} "
                          f"{Colors.WHITE}{ip}:{port}{Colors.END}  "
                          f"{Colors.DIM}{detail}{Colors.END}")

        verification_results[category] = cat_results
        grand_probed    += len(targets)
        grand_confirmed += cat_confirmed
        print(f"  {Colors.BOLD}→ {Colors.GREEN}{cat_confirmed}{Colors.END}{Colors.BOLD}/{len(targets)} "
              f"confirmed unauthenticated{Colors.END}")

    # Attach results to scan_data so exports can include them
    scan_data.verification_results = verification_results

    # Grand summary
    print_separator('═', 70, Colors.CYAN)
    print(f"{Colors.BOLD}{Colors.WHITE}VERIFICATION SUMMARY{Colors.END}")
    print_separator('─', 70, Colors.DIM)
    print(f"  Devices probed      : {Colors.CYAN}{grand_probed}{Colors.END}")
    print(f"  Confirmed open      : {Colors.RED if grand_confirmed else Colors.GREEN}{grand_confirmed}{Colors.END}")
    print(f"  Auth enforced       : {Colors.GREEN}{grand_probed - grand_confirmed}{Colors.END}")

    if grand_confirmed:
        rate = grand_confirmed / grand_probed * 100 if grand_probed else 0
        print(f"\n  {Colors.RED}⚠️  {rate:.1f}% of sampled devices have NO authentication.{Colors.END}")
        print(f"  {Colors.YELLOW}These are CONFIRMED exposures — not just Shodan estimates.{Colors.END}")
    else:
        print(f"\n  {Colors.GREEN}✓ All sampled devices appear to enforce authentication.{Colors.END}")

    print_separator('═', 70, Colors.CYAN)


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                      MODE SELECTION MENU                          ║
# ╚═══════════════════════════════════════════════════════════════════╝

def display_mode_menu():
    """Display operation mode selection menu. Returns 1-4."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}       {Colors.WHITE}SELECT OPERATION MODE{Colors.END}             {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.END}\n")

    print(f"  {Colors.GREEN}[1]{Colors.END} {Colors.BOLD}Query Mode{Colors.END}      {Colors.DIM}— Search Shodan's indexed database (current behavior){Colors.END}")
    print(f"  {Colors.GREEN}[2]{Colors.END} {Colors.BOLD}Scanner Mode{Colors.END}    {Colors.DIM}— On-demand active scan of IP/CIDR targets{Colors.END}")
    print(f"  {Colors.GREEN}[3]{Colors.END} {Colors.BOLD}Monitor Mode{Colors.END}    {Colors.DIM}— Set up persistent network alerts{Colors.END}")
    print(f"  {Colors.GREEN}[4]{Colors.END} {Colors.BOLD}Intelligence{Colors.END}    {Colors.DIM}— View Shodan protocols & active ports (free){Colors.END}")

    print_separator('─', 50, Colors.DIM)

    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Select mode [1-4]: {Colors.END}").strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            else:
                print_status('error', "Please enter a number between 1 and 4")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Cancelled by user{Colors.END}")
            sys.exit(0)


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                        SCANNER MODE                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

def scanner_mode(api):
    """On-demand active scan of IP/CIDR targets using Shodan Scanner API."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}          {Colors.WHITE}SCANNER MODE{Colors.END}                    {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.END}\n")

    # Step 1: Check scan credits
    try:
        loading_animation("Retrieving account information", 1)
        info = api.info()
        scan_credits = info.get('scan_credits', 0)
        query_credits = info.get('query_credits', 0)
        plan = info.get('plan', 'Unknown')

        print_status('info', f"Plan: {Colors.CYAN}{plan}{Colors.END}  |  "
                             f"Scan Credits: {Colors.GREEN if scan_credits > 0 else Colors.RED}{scan_credits}{Colors.END}  |  "
                             f"Query Credits: {Colors.CYAN}{query_credits}{Colors.END}")

        if scan_credits < 1:
            print_status('warning', f"{Colors.YELLOW}You have no scan credits remaining.{Colors.END}")
            print_status('info', "Scan credits can be purchased at https://account.shodan.io/")
            print_status('info', "Continuing in read-only mode — you can still submit but the API will reject it.")
    except shodan.APIError as e:
        print_status('error', f"Could not retrieve account info: {Colors.RED}{e}{Colors.END}")

    # Step 2: Get targets
    print_separator('─', 60, Colors.DIM)
    print_status('info', f"Enter IPs or CIDR ranges to scan, comma-separated.")
    print(f"  {Colors.DIM}Example: 192.168.1.1, 10.0.0.0/24{Colors.END}")

    try:
        raw_input_targets = input(f"\n{Colors.BOLD}Targets: {Colors.END}").strip()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Cancelled by user{Colors.END}")
        return

    if not raw_input_targets:
        print_status('error', "No targets entered. Returning to main menu.")
        return

    ips_list = [t.strip() for t in raw_input_targets.split(',') if t.strip()]
    print_status('success', f"Targets queued: {Colors.CYAN}{', '.join(ips_list)}{Colors.END}")

    # Step 3: Show available protocols (paginated)
    print_separator('─', 60, Colors.DIM)
    print_status('info', "Fetching available scan protocols from Shodan...")
    try:
        loading_animation("Fetching protocols", 1)
        protocols = api.protocols()
        proto_items = sorted(protocols.items())
        page_size = 20
        total = len(proto_items)
        start = 0

        while start < total:
            print(f"\n{Colors.BOLD}{Colors.CYAN}Available Protocols [{start + 1}-{min(start + page_size, total)} of {total}]:{Colors.END}")
            for name, desc in proto_items[start:start + page_size]:
                print(f"  {Colors.GREEN}{name:<25}{Colors.END} {Colors.DIM}{desc}{Colors.END}")
            start += page_size
            if start < total:
                try:
                    more = input(f"\n{Colors.DIM}[Press Enter for more, or 'q' to skip]{Colors.END} ").strip().lower()
                    if more == 'q':
                        break
                except KeyboardInterrupt:
                    break
    except shodan.APIError as e:
        print_status('warning', f"Could not fetch protocols: {Colors.YELLOW}{e}{Colors.END}")

    # Step 4: Confirm scan
    print_separator('─', 60, Colors.DIM)
    try:
        confirm = input(f"\n{Colors.BOLD}Submit scan for {Colors.CYAN}{', '.join(ips_list)}{Colors.END}{Colors.BOLD}? [Y/n]: {Colors.END}").strip().lower()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Cancelled by user{Colors.END}")
        return

    if confirm not in ['', 'y', 'yes']:
        print_status('info', "Scan cancelled by user.")
        return

    # Step 5: Submit scan
    try:
        print_status('scan', "Submitting scan request to Shodan...")
        result = api.scan(ips_list)
        scan_id = result.get('id', 'unknown')
        count = result.get('count', 0)
        credits_left = result.get('credits_left', '?')

        print_status('success', f"Scan submitted — ID: {Colors.CYAN}{scan_id}{Colors.END}  |  "
                                f"IPs queued: {Colors.GREEN}{count}{Colors.END}  |  "
                                f"Credits remaining: {Colors.YELLOW}{credits_left}{Colors.END}")
    except shodan.APIError as e:
        print_status('error', f"Scan submission failed: {Colors.RED}{e}{Colors.END}")
        return

    # Step 6: Poll scan status
    print_separator('─', 60, Colors.DIM)
    print_status('info', "Polling scan status (Ctrl+C to stop polling)...")
    spinner_chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    i = 0
    try:
        while True:
            try:
                status_result = api.scan_status(scan_id)
                status = status_result.get('status', 'UNKNOWN')
            except shodan.APIError as e:
                print_status('warning', f"Status check error: {Colors.YELLOW}{e}{Colors.END}")
                status = 'UNKNOWN'

            status_color = {
                'SUBMITTING': Colors.YELLOW,
                'QUEUE': Colors.YELLOW,
                'PROCESSING': Colors.CYAN,
                'DONE': Colors.GREEN,
            }.get(status, Colors.DIM)

            sys.stdout.write(
                f'\r{Colors.CYAN}{spinner_chars[i % len(spinner_chars)]}{Colors.END} '
                f'Scan Status: {status_color}{status}{Colors.END}        '
            )
            sys.stdout.flush()
            i += 1

            if status == 'DONE':
                print()
                print_status('success', "Scan completed successfully.")
                break

            time.sleep(5)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Stopped polling. Scan may still be running in the background.{Colors.END}")
        print_status('info', f"Use scan ID {Colors.CYAN}{scan_id}{Colors.END} to check status later.")
        return

    # Step 7: Offer to query results
    print_separator('─', 60, Colors.DIM)
    try:
        query_now = input(f"\n{Colors.BOLD}Search Shodan for these IPs now? [Y/n]: {Colors.END}").strip().lower()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
        return

    if query_now in ['', 'y', 'yes']:
        for target in ips_list:
            query = f"net:{target}"
            print_separator('─', 60, Colors.DIM)
            print_status('scan', f"Querying: {Colors.CYAN}{query}{Colors.END}")
            try:
                res = api.search(query)
                total_found = res.get('total', 0)
                print_status('found', f"Total results: {Colors.GREEN}{total_found:,}{Colors.END}")
                for match in res.get('matches', [])[:5]:
                    ip = match.get('ip_str', 'N/A')
                    port = match.get('port', 'N/A')
                    org = match.get('org', 'N/A')
                    print(f"  {Colors.CYAN}{ip}:{port}{Colors.END}  {Colors.DIM}{org}{Colors.END}")
            except shodan.APIError as e:
                print_status('error', f"Query failed: {Colors.RED}{e}{Colors.END}")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                        MONITOR MODE                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

def monitor_mode(api):
    """Persistent network alert management via Shodan Monitor API."""
    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}          {Colors.WHITE}MONITOR MODE{Colors.END}                    {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.END}\n")

        print(f"  {Colors.GREEN}[1]{Colors.END} List active alerts")
        print(f"  {Colors.GREEN}[2]{Colors.END} Create new alert (name + IP/CIDR)")
        print(f"  {Colors.GREEN}[3]{Colors.END} Check alert results")
        print(f"  {Colors.GREEN}[4]{Colors.END} Delete alert")
        print(f"  {Colors.YELLOW}[0]{Colors.END} Back to main menu")
        print_separator('─', 50, Colors.DIM)

        try:
            choice = input(f"\n{Colors.BOLD}Select option: {Colors.END}").strip()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Returning to main menu{Colors.END}")
            return

        if choice == '0':
            return

        elif choice == '1':
            # List active alerts
            print_separator('─', 60, Colors.DIM)
            print_status('info', "Fetching active alerts...")
            try:
                loading_animation("Retrieving alerts", 1)
                alerts = api.alerts()
                if not alerts:
                    print_status('info', "No active alerts found.")
                else:
                    print(f"\n{Colors.BOLD}{Colors.CYAN}{'ID':<30} {'Name':<25} {'IP/Range':<20} {'Created'}{Colors.END}")
                    print_separator('─', 90, Colors.DIM)
                    for alert in alerts:
                        alert_id = alert.get('id', 'N/A')
                        name = alert.get('name', 'N/A')
                        filters = alert.get('filters', {})
                        ip_range = filters.get('ip', 'N/A') if isinstance(filters, dict) else 'N/A'
                        created = alert.get('created', 'N/A')
                        print(f"  {Colors.CYAN}{alert_id:<28}{Colors.END} {name:<25} {Colors.GREEN}{ip_range:<20}{Colors.END} {Colors.DIM}{created}{Colors.END}")
                    print_status('found', f"Total alerts: {Colors.GREEN}{len(alerts)}{Colors.END}")
            except shodan.APIError as e:
                print_status('error', f"Could not retrieve alerts: {Colors.RED}{e}{Colors.END}")

        elif choice == '2':
            # Create new alert
            print_separator('─', 60, Colors.DIM)
            try:
                alert_name = input(f"{Colors.BOLD}Alert name: {Colors.END}").strip()
                ip_range = input(f"{Colors.BOLD}IP/CIDR range (e.g. 10.0.0.0/24): {Colors.END}").strip()
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
                continue

            if not alert_name or not ip_range:
                print_status('error', "Name and IP range are required.")
                continue

            try:
                loading_animation("Creating alert", 1)
                alert = api.create_alert(alert_name, {'ip': ip_range})
                alert_id = alert.get('id', 'N/A')
                print_status('success', f"Alert created — ID: {Colors.CYAN}{alert_id}{Colors.END}  Name: {Colors.GREEN}{alert_name}{Colors.END}  Range: {Colors.YELLOW}{ip_range}{Colors.END}")
            except shodan.APIError as e:
                print_status('error', f"Failed to create alert: {Colors.RED}{e}{Colors.END}")

        elif choice == '3':
            # Check alert results
            print_separator('─', 60, Colors.DIM)
            try:
                alert_id = input(f"{Colors.BOLD}Enter alert ID: {Colors.END}").strip()
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
                continue

            if not alert_id:
                print_status('error', "Alert ID is required.")
                continue

            try:
                loading_animation("Fetching alert info", 1)
                alert_info = api.alert_info(alert_id)
                name = alert_info.get('name', 'N/A')
                filters = alert_info.get('filters', {})
                ip_range = filters.get('ip', 'N/A') if isinstance(filters, dict) else 'N/A'
                matches = alert_info.get('matches', [])
                size = alert_info.get('size', len(matches))

                print(f"\n{Colors.BOLD}Alert:{Colors.END} {Colors.CYAN}{name}{Colors.END}  |  Range: {Colors.GREEN}{ip_range}{Colors.END}  |  Matches: {Colors.YELLOW}{size}{Colors.END}")

                if matches:
                    print_separator('─', 60, Colors.DIM)
                    for match in matches[:10]:
                        ip = match.get('ip_str', 'N/A')
                        port = match.get('port', 'N/A')
                        org = match.get('org', 'N/A')
                        print(f"  {Colors.CYAN}{ip}:{port}{Colors.END}  {Colors.DIM}{org}{Colors.END}")
                    if size > 10:
                        print(f"  {Colors.DIM}... and {size - 10} more{Colors.END}")
                else:
                    print_status('info', "No matches recorded for this alert yet.")
            except shodan.APIError as e:
                print_status('error', f"Could not fetch alert info: {Colors.RED}{e}{Colors.END}")

        elif choice == '4':
            # Delete alert
            print_separator('─', 60, Colors.DIM)
            try:
                alert_id = input(f"{Colors.BOLD}Enter alert ID to delete: {Colors.END}").strip()
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
                continue

            if not alert_id:
                print_status('error', "Alert ID is required.")
                continue

            try:
                confirm = input(f"{Colors.YELLOW}[!] Delete alert {Colors.CYAN}{alert_id}{Colors.END}{Colors.YELLOW}? [y/N]: {Colors.END}").strip().lower()
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Cancelled{Colors.END}")
                continue

            if confirm in ['y', 'yes']:
                try:
                    loading_animation("Deleting alert", 1)
                    api.delete_alert(alert_id)
                    print_status('success', f"Alert {Colors.CYAN}{alert_id}{Colors.END} deleted successfully.")
                except shodan.APIError as e:
                    print_status('error', f"Failed to delete alert: {Colors.RED}{e}{Colors.END}")
            else:
                print_status('info', "Deletion cancelled.")

        else:
            print_status('error', "Invalid option. Please enter 0-4.")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                    INTELLIGENCE MODE                              ║
# ╚═══════════════════════════════════════════════════════════════════╝

def show_shodan_intelligence(api):
    """Display Shodan protocols & active ports — no credits consumed."""
    IOT_PORTS = {554, 1883, 502, 47808, 23, 80, 443}

    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║{Colors.END}    {Colors.WHITE}SHODAN INTELLIGENCE{Colors.END} {Colors.GREEN}[FREE]{Colors.END}          {Colors.BOLD}{Colors.CYAN}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════╝{Colors.END}\n")
    print_status('info', "No query credits consumed for this view.")

    # Step 1: Protocols
    print_separator('═', 70, Colors.CYAN)
    print(f"{Colors.BOLD}{Colors.CYAN}KNOWN PROTOCOLS{Colors.END}")
    print_separator('─', 70, Colors.DIM)

    try:
        loading_animation("Fetching protocols", 1)
        protocols = api.protocols()
        proto_items = sorted(protocols.items())

        col_width_name = 30
        print(f"{Colors.BOLD}{'Protocol':<{col_width_name}} Description{Colors.END}")
        print_separator('─', 70, Colors.DIM)

        for name, desc in proto_items:
            print(f"  {Colors.GREEN}{name:<{col_width_name - 2}}{Colors.END} {Colors.DIM}{desc}{Colors.END}")

        print_status('found', f"Total protocols available: {Colors.GREEN}{len(proto_items)}{Colors.END}")
    except shodan.APIError as e:
        print_status('error', f"Could not fetch protocols: {Colors.RED}{e}{Colors.END}")

    # Step 2: Ports
    print_separator('═', 70, Colors.CYAN)
    print(f"{Colors.BOLD}{Colors.CYAN}SCANNED PORTS{Colors.END}")
    print_separator('─', 70, Colors.DIM)

    try:
        loading_animation("Fetching scanned ports", 1)
        ports = sorted(api.ports())

        # Group by range
        ranges = [
            ("Well-Known   (0–1023)",    [p for p in ports if p < 1024]),
            ("Registered  (1024–49151)", [p for p in ports if 1024 <= p < 49152]),
            ("Dynamic     (49152+)",     [p for p in ports if p >= 49152]),
        ]

        for range_label, range_ports in ranges:
            if not range_ports:
                continue
            print(f"\n  {Colors.BOLD}{Colors.CYAN}{range_label}{Colors.END}")
            port_strs = []
            for p in range_ports:
                if p in IOT_PORTS:
                    port_strs.append(f"{Colors.YELLOW}{p}*{Colors.END}")
                else:
                    port_strs.append(f"{Colors.DIM}{p}{Colors.END}")
            # Print 15 per line
            line_size = 15
            for j in range(0, len(port_strs), line_size):
                print("    " + "  ".join(port_strs[j:j + line_size]))

        print_status('found', f"Total ports scanned by Shodan: {Colors.GREEN}{len(ports)}{Colors.END}")

        # Step 3: IoT cross-reference
        print_separator('─', 70, Colors.DIM)
        print(f"{Colors.BOLD}{Colors.YELLOW}IoT-Relevant Ports (marked with * above):{Colors.END}")
        iot_labels = {
            554:   "RTSP – IP Camera Streams",
            1883:  "MQTT – IoT Message Broker",
            502:   "Modbus – Industrial SCADA/ICS",
            47808: "BACnet – Building Automation",
            23:    "Telnet – Legacy/Default-Creds",
            80:    "HTTP – Web Interfaces",
            443:   "HTTPS – Secure Web Interfaces",
        }
        for port in sorted(IOT_PORTS):
            present = port in set(ports)
            status_icon = f"{Colors.GREEN}[ACTIVE]{Colors.END}" if present else f"{Colors.DIM}[NOT SCANNED]{Colors.END}"
            label = iot_labels.get(port, '')
            print(f"  {Colors.YELLOW}{port:<7}{Colors.END} {status_icon}  {Colors.DIM}{label}{Colors.END}")

    except shodan.APIError as e:
        print_status('error', f"Could not fetch ports: {Colors.RED}{e}{Colors.END}")

    print_separator('═', 70, Colors.CYAN)
    print_status('info', "Intelligence view complete. No credits were consumed.")


# ╔═══════════════════════════════════════════════════════════════════╗
# ║                         MAIN FUNCTION                             ║
# ╚═══════════════════════════════════════════════════════════════════╝

def main():
    """Main execution"""

    print_banner()

    api_key = load_api_key()

    # Mode selection
    mode = display_mode_menu()

    if mode == 2:
        api = shodan.Shodan(api_key)
        scanner_mode(api)
        return
    elif mode == 3:
        api = shodan.Shodan(api_key)
        monitor_mode(api)
        return
    elif mode == 4:
        api = shodan.Shodan(api_key)
        show_shodan_intelligence(api)
        return

    # mode == 1: existing Query Mode flow
    # Check requirements before proceeding
    if not check_requirements(api_key):
        print(f"\n{Colors.CYAN}[i] Exiting MOIRAGUARD...{Colors.END}\n")
        sys.exit(0)

    # Load countries and display selection menu
    countries = load_countries()
    country_code, country_name = display_country_menu(countries)

    if country_code:
        print_status('info', f"Target set to: {Colors.YELLOW}{country_name}{Colors.END} ({Colors.CYAN}{country_code}{Colors.END})")
    else:
        print_status('info', f"Target set to: {Colors.YELLOW}Global{Colors.END} (no country filter)")

    # Ask for verbosity level
    print(f"\n{Colors.BOLD}{Colors.CYAN}Scan Verbosity:{Colors.END}")
    print(f"  {Colors.GREEN}[1]{Colors.END} Metrics Only {Colors.DIM}(Fast - counts and totals only){Colors.END}")
    print(f"  {Colors.GREEN}[2]{Colors.END} Verbose Mode {Colors.DIM}(Detailed - includes IPs and device info){Colors.END}")

    while True:
        try:
            verbose_choice = input(f"\n{Colors.BOLD}Select mode [1/2]: {Colors.END}").strip()
            if verbose_choice in ['1', '2']:
                verbose = (verbose_choice == '2')
                break
            else:
                print_status('error', "Please enter 1 or 2")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Cancelled by user{Colors.END}")
            sys.exit(0)

    if verbose:
        print_status('info', f"Verbose mode enabled - {Colors.YELLOW}will collect detailed device information{Colors.END}")
    else:
        print_status('info', f"Metrics mode - {Colors.GREEN}collecting counts only{Colors.END}")

    try:
        # Initialize API connection (already verified in requirements check)
        api = shodan.Shodan(api_key)

        print(f"\n{Colors.BOLD}{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}]{Colors.END} {Colors.GREEN}Initiating MOIRAGUARD reconnaissance sweep...{Colors.END}\n")
        time.sleep(1)

        # Create scan data object
        scan_data = ScanData(country_code, country_name)

        # Run scans with country filter and data collection
        stats = {}

        stats['Smart Home Devices'] = scan_smart_home_devices(api, country_code, scan_data, verbose)
        time.sleep(1)

        stats['IoT Cameras'] = scan_iot_cameras(api, country_code, scan_data, verbose)
        time.sleep(1)

        stats['SCADA/ICS'] = scan_scada_ics(api, country_code, scan_data, verbose)
        time.sleep(1)

        stats['Building Automation'] = scan_building_automation(api, country_code, scan_data, verbose)
        time.sleep(1)

        stats['MQTT Brokers'] = scan_iot_mqtt(api, country_code, scan_data, verbose)
        time.sleep(1)

        stats['Industrial IoT'] = scan_industrial_iot(api, country_code, scan_data, verbose)
        time.sleep(1)

        # Print summary with target country context
        print_summary(stats, api, country_name)

        # Show post-scan menu
        post_scan_menu(scan_data)
        
    except shodan.APIError as e:
        print_status('error', f"Shodan API Error: {Colors.RED}{e}{Colors.END}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.END}")
        print(f"{Colors.CYAN}[i] Exiting MOIRAGUARD...{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print_status('error', f"Unexpected error: {Colors.RED}{e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
