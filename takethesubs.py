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

class Logger:
    """Enhanced logging system"""
    
    def __init__(self, log_file: str = None, verbose: bool = False):
        self.verbose = verbose
        self.setup_logging(log_file)
    
    def setup_logging(self, log_file: str):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        level = logging.DEBUG if self.verbose else logging.INFO
        
        handlers = [logging.StreamHandler(sys.stdout)]
        if log_file:
            handlers.append(logging.FileHandler(log_file))
        
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str):
        """Log info message with color"""
        print(f"{Colors.GREEN}[+]{Colors.END} {message}")
        if self.verbose:
            self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message with color"""
        print(f"{Colors.YELLOW}[!]{Colors.END} {message}")
        if self.verbose:
            self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message with color"""
        print(f"{Colors.RED}[-]{Colors.END} {message}")
        if self.verbose:
            self.logger.error(message)
    
    def success(self, message: str):
        """Log success message with color"""
        print(f"{Colors.CYAN}[✓]{Colors.END} {message}")
        if self.verbose:
            self.logger.info(f"SUCCESS: {message}")

class SubdomainTool:
    """Base class for subdomain enumeration tools"""
    
    def __init__(self, name: str, command: str, output_parser=None):
        self.name = name
        self.command = command
        self.output_parser = output_parser or self.default_parser
    
    def is_installed(self) -> bool:
        """Check if tool is installed"""
        try:
            subprocess.run([self.command.split()[0], '--help'], 
                         capture_output=True, check=False, timeout=5)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def run(self, target: str, output_file: str, **kwargs) -> Set[str]:
        """Run the tool and return discovered subdomains"""
        if not self.is_installed():
            return set()
        
        cmd = self.command.format(target=target, output=output_file, **kwargs)
        
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=300,
                check=False
            )
            
            if result.returncode == 0:
                return self.output_parser(output_file, result.stdout)
            else:
                return set()
                
        except subprocess.TimeoutExpired:
            return set()
    
    def default_parser(self, output_file: str, stdout: str = "") -> Set[str]:
        """Default output parser - reads line by line"""
        subdomains = set()
        
        # Try to read from output file first
        try:
            with open(output_file, 'r') as f:
                for line in f:
                    subdomain = line.strip()
                    if subdomain and self.is_valid_domain(subdomain):
                        subdomains.add(subdomain)
        except FileNotFoundError:
            pass
        
        # If no file output, parse stdout
        if not subdomains and stdout:
            for line in stdout.split('\n'):
                subdomain = line.strip()
                if subdomain and self.is_valid_domain(subdomain):
                    subdomains.add(subdomain)
        
        return subdomains
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate domain format"""
        if not domain or len(domain) > 253:
            return False
        
        # Basic domain validation
        parts = domain.split('.')
        if len(parts) < 2:
            return False
        
        for part in parts:
            if not part or len(part) > 63:
                return False
            if not part.replace('-', '').replace('_', '').isalnum():
                return False
        
        return True

class TakeTheSubs:
    """Main TakeTheSubs class"""
    
    def __init__(self, config_file: str = None):
        self.version = "2.0.0"
        self.author = "super3lr3y"
        self.config = self.load_config(config_file)
        self.logger = Logger(verbose=self.config.get('verbose', False))
        self.tools = self.initialize_tools()
        self.results = {
            'target': '',
            'start_time': '',
            'end_time': '',
            'total_subdomains': 0,
            'live_subdomains': 0,
            'tools_used': [],
            'subdomains': set(),
            'live_hosts': set()
        }
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        default_config = {
            'output_dir': './results',
            'threads': 50,
            'timeout': 300,
            'verify_ssl': False,
            'user_agent': 'TakeTheSubs/2.0',
            'tools': {
                'subfinder': True,
                'amass': True,
                'assetfinder': True,
                'findomain': True,
                'chaos': False,
                'github_search': False
            },
            'apis': {
                'shodan': '',
                'virustotal': '',
                'github_token': ''
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
    
    def initialize_tools(self) -> Dict[str, SubdomainTool]:
        """Initialize subdomain enumeration tools"""
        tools = {}
        
        # Subfinder
        if self.config['tools']['subfinder']:
            tools['subfinder'] = SubdomainTool(
                'Subfinder',
                'subfinder -d {target} -o {output} -silent'
            )
        
        # Amass
        if self.config['tools']['amass']:
            tools['amass'] = SubdomainTool(
                'Amass',
                'amass enum -passive -d {target} -o {output}'
            )
        
        # Assetfinder
        if self.config['tools']['assetfinder']:
            tools['assetfinder'] = SubdomainTool(
                'Assetfinder',
                'assetfinder --subs-only {target}'
            )
        
        # Findomain
        if self.config['tools']['findomain']:
            tools['findomain'] = SubdomainTool(
                'Findomain',
                'findomain -t {target} -o'
            )
        
        return tools
    
    def print_banner(self):
        """Print tool banner"""
        banner = f"""
{Colors.CYAN}
████████╗ █████╗ ██╗  ██╗███████╗████████╗██╗  ██╗███████╗███████╗██╗   ██╗██████╗ ███████╗
╚══██╔══╝██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
   ██║   ███████║█████╔╝ █████╗     ██║   ███████║█████╗  ███████╗██║   ██║██████╔╝███████╗
   ██║   ██╔══██║██╔═██╗ ██╔══╝     ██║   ██╔══██║██╔══╝  ╚════██║██║   ██║██╔══██╗╚════██║
   ██║   ██║  ██║██║  ██╗███████╗   ██║   ██║  ██║███████╗███████║╚██████╔╝██████╔╝███████║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝

                    🎯 Advanced Subdomain Discovery Tool 🎯
                         Created by: {self.author}
                            Version: {self.version}
                    🚀 Take All The Subdomains! 🚀
{Colors.END}
"""
        print(banner)
    
    def run_tool(self, tool_name: str, tool: SubdomainTool, target: str, output_dir: str) -> Set[str]:
        """Run a single enumeration tool"""
        try:
            self.logger.info(f"Running {tool_name} on {target}")
            output_file = os.path.join(output_dir, f"{tool_name}_{target}.txt")
            
            subdomains = tool.run(target, output_file)
            self.logger.success(f"{tool_name} found {len(subdomains)} subdomains")
            
            return subdomains
            
        except Exception as e:
            self.logger.error(f"{tool_name} failed: {str(e)}")
            return set()
    
    def verify_subdomains(self, subdomains: Set[str]) -> Set[str]:
        """Verify which subdomains are live"""
        self.logger.info(f"Verifying {len(subdomains)} subdomains...")
        live_hosts = set()
        
        def check_host(subdomain):
            try:
                # Try HTTP first, then HTTPS
                for protocol in ['http', 'https']:
                    url = f"{protocol}://{subdomain}"
                    response = requests.get(
                        url,
                        timeout=5,
                        verify=False,
                        allow_redirects=True,
                        headers={'User-Agent': self.config['user_agent']}
                    )
                    if response.status_code < 400:
                        return subdomain
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=self.config['threads']) as executor:
            futures = {executor.submit(check_host, sub): sub for sub in subdomains}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    live_hosts.add(result)
        
        self.logger.success(f"Found {len(live_hosts)} live subdomains")
        return live_hosts
    
    def save_results(self, target: str, output_dir: str):
        """Save results in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as text
        txt_file = os.path.join(output_dir, f"{target}_subdomains_{timestamp}.txt")
        with open(txt_file, 'w') as f:
            for subdomain in sorted(self.results['subdomains']):
                f.write(f"{subdomain}\n")
        
        # Save live hosts
        live_file = os.path.join(output_dir, f"{target}_live_{timestamp}.txt")
        with open(live_file, 'w') as f:
            for subdomain in sorted(self.results['live_hosts']):
                f.write(f"{subdomain}\n")
        
        # Save as JSON
        json_file = os.path.join(output_dir, f"{target}_results_{timestamp}.json")
        json_data = {
            'target': self.results['target'],
            'start_time': self.results['start_time'],
            'end_time': self.results['end_time'],
            'total_subdomains': len(self.results['subdomains']),
            'live_subdomains': len(self.results['live_hosts']),
            'tools_used': self.results['tools_used'],
            'subdomains': list(self.results['subdomains']),
            'live_hosts': list(self.results['live_hosts'])
        }
        
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        self.logger.success(f"Results saved to {output_dir}")
        return txt_file, live_file, json_file
    
    def enumerate_target(self, target: str, output_dir: str = None) -> Dict:
        """Main enumeration function for a single target"""
        if not output_dir:
            output_dir = os.path.join(self.config['output_dir'], target)
        
        os.makedirs(output_dir, exist_ok=True)
        
        self.results['target'] = target
        self.results['start_time'] = datetime.now().isoformat()
        
        self.logger.info(f"TakeTheSubs v{self.version} - Starting subdomain enumeration...")
        self.logger.info(f"Target: {target}")
        self.logger.info(f"Output: {output_dir}")
        self.logger.info(f"Threads: {self.config['threads']}")
        
        all_subdomains = set()
        tools_used = []
        
        # Run tools sequentially for better output
        for name, tool in self.tools.items():
            if tool.is_installed():
                subdomains = self.run_tool(name, tool, target, output_dir)
                all_subdomains.update(subdomains)
                tools_used.append(name)
            else:
                self.logger.warning(f"{name} is not installed, skipping...")
        
        # Remove duplicates and filter
        unique_subdomains = {sub for sub in all_subdomains if target in sub}
        
        self.results['subdomains'] = unique_subdomains
        self.results['tools_used'] = tools_used
        
        # Verify live hosts if requested
        if unique_subdomains and self.config.get('verify', False):
            self.results['live_hosts'] = self.verify_subdomains(unique_subdomains)
        
        self.results['end_time'] = datetime.now().isoformat()
        
        # Print summary
        self.logger.success(f"Subdomain enumeration completed!")
        self.logger.info(f"Total subdomains found: {len(unique_subdomains)}")
        if self.results['live_hosts']:
            self.logger.info(f"Live subdomains: {len(self.results['live_hosts'])}")
        
        # Save results
        files = self.save_results(target, output_dir)
        
        print(f"{Colors.GREEN}🎯 Take All The Subdomains! 🚀{Colors.END}")
        
        return {
            'target': target,
            'total_subdomains': len(unique_subdomains),
            'live_subdomains': len(self.results['live_hosts']),
            'output_files': files
        }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="TakeTheSubs - Advanced Subdomain Discovery Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 takethesubs.py -t example.com
  python3 takethesubs.py -l targets.txt
  python3 takethesubs.py -t example.com -o /tmp/results
  python3 takethesubs.py -t example.com --verify --threads 100
        """
    )
    
    parser.add_argument('-t', '--target', help='Target domain')
    parser.add_argument('-l', '--list', help='File containing list of targets')
    parser.add_argument('-o', '--output', help='Output directory', default='results')
    parser.add_argument('-c', '--config', help='Configuration file')
    parser.add_argument('--verify', action='store_true', help='Verify live subdomains')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='TakeTheSubs 2.0.0')
    
    args = parser.parse_args()
    
    if not args.target and not args.list:
        parser.print_help()
        sys.exit(1)
    
    # Initialize TakeTheSubs
    takethesubs = TakeTheSubs(args.config)
    takethesubs.config['verbose'] = args.verbose
    takethesubs.config['threads'] = args.threads
    takethesubs.config['verify'] = args.verify
    
    # Print banner
    takethesubs.print_banner()
    
    try:
        if args.target:
            # Single target
            result = takethesubs.enumerate_target(args.target, args.output)
            
        elif args.list:
            # Multiple targets from file
            try:
                with open(args.list, 'r') as f:
                    targets = [line.strip() for line in f if line.strip()]
                
                takethesubs.logger.info(f"Processing {len(targets)} targets from {args.list}")
                
                for target in targets:
                    if target:
                        try:
                            result = takethesubs.enumerate_target(target, args.output)
                        except Exception as e:
                            takethesubs.logger.error(f"Failed to process {target}: {e}")
                            
            except FileNotFoundError:
                takethesubs.logger.error(f"File not found: {args.list}")
                sys.exit(1)
                
    except KeyboardInterrupt:
        takethesubs.logger.warning("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        takethesubs.logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
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
