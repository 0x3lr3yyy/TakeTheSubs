#!/bin/bash

# TakeTheSubs Installation Script
# Created by: super3lr3y
# Version: 2.0.0

echo "🎯 TakeTheSubs v2.0.0 Installation Script"
echo "Created by: super3lr3y"
echo "=========================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
sudo apt update -y

# Install Python3 and pip
echo "🐍 Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

# Install Go (for Go-based tools)
echo "🔧 Installing Go..."
sudo apt install -y golang-go

# Install required Python packages
echo "📚 Installing Python dependencies..."
pip3 install -r requirements.txt 2>/dev/null || echo "⚠️  requirements.txt not found, skipping..."

# Install subdomain enumeration tools
echo "🛠️  Installing subdomain enumeration tools..."

# Install Subfinder
echo "Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install HTTPx
echo "Installing HTTPx..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install DNSx
echo "Installing DNSx..."
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Install Assetfinder
echo "Installing Assetfinder..."
go install github.com/tomnomnom/assetfinder@latest

# Install Amass
echo "Installing Amass..."
go install -v github.com/owasp-amass/amass/v4/...@master

# Make TakeTheSubs executable
echo "🔐 Making TakeTheSubs executable..."
chmod +x takethesubs.py

# Add Go bin to PATH if not already added
if ! echo $PATH | grep -q "$HOME/go/bin"; then
    echo "📝 Adding Go bin to PATH..."
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
    export PATH=$PATH:$HOME/go/bin
fi

echo ""
echo "✅ TakeTheSubs installation completed successfully!"
echo ""
echo "🚀 Usage:"
echo "  python3 takethesubs.py -t example.com"
echo "  python3 takethesubs.py -l domains.txt --verify"
echo ""
echo "🎯 Take All The Subdomains! 🚀"
