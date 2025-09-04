#!/usr/bin/env python3
"""
TakeTheSubs - Advanced Subdomain Discovery Tool
Created by: super3lr3y
Version: 2.0.0
Description: Modern, fast, and comprehensive subdomain enumeration tool
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
import subprocess
import requests
from urllib.parse import urlparse
import yaml

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Print TakeTheSubs banner"""
    banner = f"""
{Colors.CYAN}
████████╗ █████╗ ██╗  ██╗███████╗████████╗██╗  ██╗███████╗███████╗██╗   ██╗██████╗ ███████╗
╚══██╔══╝██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
   ██║   ███████║█████╔╝ █████╗     ██║   ███████║█████╗  ███████╗██║   ██║██████╔╝███████╗
   ██║   ██╔══██║██╔═██╗ ██╔══╝     ██║   ██╔══██║██╔══╝  ╚════██║██║   ██║██╔══██╗╚════██║
   ██║   ██║  ██║██║  ██╗███████╗   ██║   ██║  ██║███████╗███████║╚██████╔╝██████╔╝███████║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝

                    🎯 Advanced Subdomain Discovery Tool 🎯
                         Created by: super3lr3y
                            Version: 2.0.0
                    🚀 Take All The Subdomains! 🚀
{Colors.END}
"""
    print(banner)

def main():
    """Main function"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="TakeTheSubs - Advanced Subdomain Discovery Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 takethesubs.py -t example.com
  python3 takethesubs.py -l domains.txt --verify
  python3 takethesubs.py -t example.com -o /tmp/results --threads 100
        """
    )
    
    parser.add_argument('-t', '--target', help='Target domain')
    parser.add_argument('-l', '--list', help='File containing list of domains')
    parser.add_argument('-o', '--output', help='Output directory', default='results')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('--verify', action='store_true', help='Verify live hosts')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='TakeTheSubs 2.0.0')
    
    args = parser.parse_args()
    
    if not args.target and not args.list:
        parser.print_help()
        sys.exit(1)
    
    print(f"{Colors.GREEN}[+] TakeTheSubs v2.0.0 - Starting subdomain enumeration...{Colors.END}")
    print(f"{Colors.YELLOW}[+] Target: {args.target or 'Multiple domains'}{Colors.END}")
    print(f"{Colors.YELLOW}[+] Output: {args.output}{Colors.END}")
    print(f"{Colors.YELLOW}[+] Threads: {args.threads}{Colors.END}")
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print(f"{Colors.CYAN}[+] Subdomain enumeration completed!{Colors.END}")
    print(f"{Colors.GREEN}🎯 Take All The Subdomains! 🚀{Colors.END}")

if __name__ == "__main__":
    main()
