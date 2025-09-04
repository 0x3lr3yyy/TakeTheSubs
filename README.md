# TakeTheSubs

**Advanced Subdomain Discovery Tool**

*Simple • Fast • Effective*

Very effective for bug hunting

# What is TakeTheSubs ?

TakeTheSubs is an advanced automation tool for subdomain discovery and enumeration whether for single target or multiple targets. TakeTheSubs uses multiple reconnaissance tools for doing the subdomain gathering job in a perfect way, it can take a domains/targets list and perform the whole operation on them and after finishing the job it saves the result in a comprehensible & ordered way.

After TakeTheSubs finishes gathering subdomains it filters them from repeated subdomains then filters only the live subdomains. It also uses multiple methods to gather subdomains like: gathering subdomains through API integrations (Shodan, VirusTotal, GitHub), passive enumeration, wordlist-based enumeration and other effective techniques.

This tool is made & developed to work on modern Linux systems and has been tested on:

- Kali Linux
- Ubuntu  
- Debian

And it should work on other security distributions like:

- ParrotOS
- BackBox
- Arch Linux

# Tool Mechanism:

## Subdomains Discovery & Gathering:

- **Subfinder** - Fast passive subdomain enumeration
- **Amass v4** - Passive Mode & Intel Mode  
- **Assetfinder** - Gathering subdomains through multiple sources
- **Findomain** - Fast cross-platform subdomain enumerator
- **HTTPx** - Live host verification & HTTP/HTTPS probing
- **DNSx** - DNS enumeration and validation
- **API Integration** - Shodan API, VirusTotal API, GitHub Token Search

## Filtering & Verification:

- Unique result filtering
- Live host verification using HTTPx
- Multiple output formats (JSON, CSV, HTML, TXT)
- Advanced filtering and deduplication

# Features:
# Installation:

## Automatic Installation (Recommended):

```bash
git clone https://github.com/0x3lr3yyy/TakeTheSubs.git
cd TakeTheSubs
chmod +x install.sh
./install.sh
```

## Manual Installation:

```bash
# Clone the repository
git clone https://github.com/0x3lr3yyy/TakeTheSubs.git
cd TakeTheSubs

# Install Python dependencies
pip3 install requests colorama pyyaml

# Install Go-based tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install github.com/tomnomnom/assetfinder@latest
go install -v github.com/owasp-amass/amass/v4/...@master

# Make TakeTheSubs executable
chmod +x takethesubs.py
```

# Usage:

## Basic Usage:

```bash
# Single target
python3 takethesubs.py -t example.com

# Multiple targets from file
python3 takethesubs.py -l domains.txt

# With live host verification
python3 takethesubs.py -t example.com --verify

# Custom output format
python3 takethesubs.py -t example.com -o json
```

## Advanced Usage:

```bash
# Use specific tools only
python3 takethesubs.py -t example.com --tools subfinder,httpx

# Set custom threads
python3 takethesubs.py -t example.com --threads 50

# Use API keys for better results
python3 takethesubs.py -t example.com --shodan-api YOUR_API_KEY

# Save results to custom file
python3 takethesubs.py -t example.com --output results.txt

# Verbose mode with detailed logs
python3 takethesubs.py -t example.com --verbose
```

## Command Line Options:

```
-t, --target          Target domain to scan
-l, --list            File containing list of domains
-o, --output-format   Output format (txt, json, csv, html)
--verify              Verify live hosts using HTTPx
--tools               Comma-separated list of tools to use
--threads             Number of threads (default: 20)
--timeout             Timeout for requests (default: 10)
--shodan-api          Shodan API key
--virustotal-api      VirusTotal API key
--github-token        GitHub token for API access
--output              Custom output file name
--verbose             Enable verbose logging
--help                Show help message
```

# Examples:

## Basic Subdomain Discovery:
```bash
python3 takethesubs.py -t hackerone.com
```

## Advanced Scan with API Integration:
```bash
python3 takethesubs.py -t example.com --verify --shodan-api YOUR_KEY --output-format json
```

## Bulk Domain Scanning:
```bash
python3 takethesubs.py -l domains.txt --threads 30 --verify
```
✅ **Multi-tool Integration** - 8+ reconnaissance tools  
✅ **High Performance** - Multi-threaded processing  
✅ **Live Host Verification** - Automatic subdomain validation  
✅ **Multiple Output Formats** - JSON, CSV, HTML, TXT  
✅ **API Integration** - Shodan, VirusTotal, GitHub  
✅ **Configuration Management** - YAML-based configuration  
✅ **Enhanced Logging** - Colored output with detailed logs  
✅ **Error Resilience** - Robust error handling and recovery  

---

**Created with ❤️ by super3lr3y**

**🎯 Take All The Subdomains! 🚀**


