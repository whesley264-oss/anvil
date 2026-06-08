"""
ANVIL Update Command - Auto-update ANVIL CLI
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path

# Colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def add_parser(subparsers):
    parser = subparsers.add_parser(
        'update',
        help='Update ANVIL to the latest version',
        description='Download and install the latest ANVIL version'
    )
    parser.add_argument('--check', action='store_true', help='Check for updates without installing')
    parser.add_argument('--force', action='store_true', help='Force reinstall current version')

def get_installed_version():
    """Get current installed version by reading anvil_cli.py"""
    try:
        anvil_home = os.environ.get('ANVIL_HOME', str(Path.home() / '.anvil'))
        cli_file = Path(anvil_home) / "anvil_cli.py"
        if cli_file.exists():
            with open(cli_file, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('__version__'):
                        return line.split('=')[1].strip().strip('"').strip("'")
    except:
        pass
    return "unknown"

def get_latest_info():
    """Get latest commit info from GitHub"""
    try:
        url = "https://api.github.com/repos/whesley264-oss/anvil/commits/main"
        req = urllib.request.Request(url, headers={'User-Agent': 'ANVIL-CLI'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            sha = data['sha'][:7]
            date = data['commit']['author']['date']
            return sha, date
    except:
        return None, None

def run(args):
    print()
    print(f"{Colors.BOLD}╔══════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}║{Colors.END}  {Colors.CYAN}ANVIL - Update System{Colors.END}                 {Colors.BOLD}║{Colors.END}")
    print(f"{Colors.BOLD}╚══════════════════════════════════════════╝{Colors.END}")
    print()
    
    current_version = get_installed_version()
    print(f"{Colors.YELLOW}Local Version:{Colors.END} {current_version}")
    
    print(f"{Colors.CYAN}Checking for updates on GitHub...{Colors.END}")
    latest_sha, latest_date = get_latest_info()
    
    if not latest_sha:
        print(f"{Colors.RED}✗ Could not reach GitHub API.{Colors.END}")
        if not getattr(args, 'force', False):
            return

    if latest_sha:
        print(f"{Colors.GREEN}Latest Commit:{Colors.END} {latest_sha} ({latest_date[:10]})")

    # Check mode
    if getattr(args, 'check', False):
        print(f"\n{Colors.YELLOW}ℹ Run 'anvil update' to pull latest changes.{Colors.END}")
        return

    print(f"\n{Colors.CYAN}🚀 Initializing update process...{Colors.END}")
    
    anvil_home = os.environ.get('ANVIL_HOME', str(Path.home() / '.anvil'))
    install_script = Path(anvil_home) / "install.sh"
    
    # If install script doesn't exist, try to download it
    if not install_script.exists():
        print(f"{Colors.YELLOW}⚠ Local installer not found. Downloading fresh installer...{Colors.END}")
        try:
            import tempfile
            url = "https://raw.githubusercontent.com/whesley264-oss/anvil/main/install.sh"
            tmp_installer = os.path.join(tempfile.gettempdir(), "anvil_install.sh")
            urllib.request.urlretrieve(url, tmp_installer)
            install_script = Path(tmp_installer)
            os.chmod(install_script, 0o755)
        except Exception as e:
            print(f"{Colors.RED}✗ Failed to download installer: {e}{Colors.END}")
            return

    try:
        # Run installer. We use subprocess.call to allow the installer to print its own colored output
        # But we need to use bash specifically
        print(f"{Colors.BOLD}--- Installer Output ---{Colors.END}")
        retcode = subprocess.call(['bash', str(install_script)])
        print(f"{Colors.BOLD}------------------------{Colors.END}")
        
        if retcode == 0:
            print(f"\n{Colors.GREEN}✅ ANVIL updated successfully!{Colors.END}")
            print(f"Please restart your shell or run 'zsh' to apply changes.")
        else:
            print(f"\n{Colors.RED}❌ Update failed with exit code {retcode}{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error executing update: {e}{Colors.END}")
