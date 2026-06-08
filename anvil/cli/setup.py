"""
ANVIL setup - Setup ANVIL on different platforms
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Import mobile detection
try:
    from anvil.utils.mobile import is_mobile, is_termux, get_platform_info, get_sdk_path, get_java_path
except ImportError:
    from utils.mobile import is_mobile, is_termux, get_platform_info, get_sdk_path, get_java_path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def run_termux_setup():
    """Setup ANVIL in Termux environment"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║       ANVIL - Termux Setup Wizard         ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    if not is_termux():
        print_warning("This command is designed for Termux on Android.")
        response = input("Continue anyway? [y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            return
    
    # Step 1: Check/update packages
    print_step("1", "Updating Termux packages...")
    
    print_info("Running: pkg update && pkg upgrade")
    result = subprocess.run(["pkg", "update"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Failed to update packages")
        return
    
    print_success("Packages updated!")
    
    # Step 2: Install required packages
    print_step("2", "Installing required packages...")
    
    packages = [
        "python",
        "git",
        "openjdk-17",
        "clang",
        "make",
        "cmake",
    ]
    
    for pkg in packages:
        print_info(f"Installing: {pkg}")
        result = subprocess.run(["pkg", "install", "-y", pkg], capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Installed: {pkg}")
        else:
            print_warning(f"Failed to install: {pkg}")
    
    # Step 3: Setup Android SDK
    print_step("3", "Setting up Android SDK...")
    
    sdk_path = get_sdk_path()
    
    if sdk_path and Path(sdk_path).exists():
        print_success(f"Android SDK found: {sdk_path}")
    else:
        print_info("Android SDK not found. Installing...")
        
        print_info("Note: Installing Android SDK in Termux requires significant storage.")
        print_info("Alternative: You can download command-line tools manually.")
        
        response = input("Install Android SDK now? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            # Try to install android-sdk package
            result = subprocess.run(["pkg", "install", "-y", "android-sdk"], capture_output=True, text=True)
            
            if result.returncode == 0:
                print_success("Android SDK installed!")
                sdk_path = "/data/data/com.termux/files/usr/lib/android-sdk"
            else:
                print_warning("Android SDK package failed. Consider manual installation.")
                print_info("Download from: https://developer.android.com/studio#command-line-tools")
    
    # Step 4: Setup environment variables
    print_step("4", "Setting up environment variables...")
    
    # Create termux startup script
    termux_bashrc = Path.home() / ".bashrc"
    termux_profile = Path.home() / ".profile"
    
    env_lines = [
        "",
        "# ANVIL Environment Variables",
        f"export ANDROID_HOME={sdk_path or '$PREFIX/lib/android-sdk'}",
        "export JAVA_HOME=$PREFIX/lib/jvm/java-17-openjdk",
        "export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools",
        "",
    ]
    
    # Add to .bashrc
    with open(termux_bashrc, 'a') as f:
        for line in env_lines:
            f.write(line + "\n")
    
    print_success("Environment variables configured!")
    
    # Step 5: Install ANVIL
    print_step("5", "Installing ANVIL...")
    
    anvil_path = Path(__file__).parent.parent.parent
    install_cmd = f"cd {anvil_path} && pip install -e ."
    
    print_info(f"Running: {install_cmd}")
    result = subprocess.run(["pip", "install", "-e", str(anvil_path)], capture_output=True, text=True)
    
    if result.returncode == 0:
        print_success("ANVIL installed!")
    else:
        print_error("Failed to install ANVIL")
        print(f"Error: {result.stderr}")
        return
    
    # Step 6: Create convenience scripts
    print_step("6", "Creating convenience scripts...")
    
    # Create anvil aliases
    alias_content = """
# ANVIL aliases
alias anvil-build='anvil build'
alias anvil-doctor='anvil doctor'
alias anvil-init='anvil init'
"""
    
    with open(termux_bashrc, 'a') as f:
        f.write(alias_content)
    
    print_success("Scripts created!")
    
    # Final message
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║         Termux Setup Complete!            ║")
    print("╚══════════════════════════════════════════╝{Colors.END}")
    
    print("\nNext steps:")
    print(f"  {Colors.CYAN}source ~/.bashrc{Colors.END} - Reload environment")
    print(f"  {Colors.CYAN}anvil init{Colors.END} - Start creating apps")
    print(f"  {Colors.CYAN}anvil doctor{Colors.END} - Check setup")

def install_sdk():
    """Install Android SDK helper"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║        ANVIL - SDK Installer              ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    sdk_path = get_sdk_path()
    
    if sdk_path and Path(sdk_path).exists():
        print_info(f"Android SDK already installed at: {sdk_path}")
        return
    
    print_info("This will download and install Android SDK command-line tools.")
    print_info("Requires: ~2GB storage, internet connection\n")
    
    response = input("Continue? [y/N]: ").strip().lower()
    
    if response not in ['y', 'yes']:
        return
    
    # Download command-line tools
    sdk_dir = Path.home() / "android-sdk"
    sdk_dir.mkdir(exist_ok=True)
    
    print_info("Downloading Android command-line tools...")
    
    # Download URL (commandlinetools for Linux)
    cmdline_tools_url = "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
    
    try:
        import urllib.request
        
        print_info(f"Downloading from: {cmdline_tools_url}")
        zip_path = sdk_dir / "cmdline-tools.zip"
        
        urllib.request.urlretrieve(cmdline_tools_url, zip_path)
        
        print_success("Download complete!")
        
        # Extract
        print_info("Extracting...")
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sdk_dir)
        
        # Organize structure
        cmdline_tools = sdk_dir / "cmdline-tools"
        latest = cmdline_tools / "latest"
        latest.mkdir(exist_ok=True)
        
        # Move contents
        for item in (cmdline_tools / "cmdline-tools").glob("*"):
            if item.name != "latest":
                pass
        
        # Cleanup
        zip_path.unlink()
        
        print_success(f"Android SDK installed to: {sdk_dir}")
        
        # Update environment
        print_info("\nAdd these to your ~/.bashrc:")
        print(f"  export ANDROID_HOME={sdk_dir}")
        print(f"  export PATH=$PATH:{sdk_dir}/cmdline-tools/latest/bin")
        
    except Exception as e:
        print_error(f"Failed to install SDK: {e}")

def check_mobile_doctor():
    """Run doctor with mobile optimizations"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║      ANVIL - Mobile System Check          ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    info = get_platform_info()
    
    print(f"{Colors.BOLD}Platform Information:{Colors.END}")
    print(f"  Platform: {info['platform']}")
    print(f"  Machine: {info['machine']}")
    print(f"  Mobile: {info['is_mobile']}")
    
    if info['is_termux']:
        print(f"  Termux: Yes")
        print(f"  PREFIX: {info['termux_prefix']}")
    
    if info['total_ram_mb']:
        print(f"  RAM: {info['total_ram_mb']} MB")
    
    print()
    
    # Run standard checks
    from anvil.cli.doctor import run as doctor_run
    from argparse import Namespace
    doctor_run(Namespace(fix=False, mobile=True))

def print_step(step: str, message: str):
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def run(args):
    """Run the setup command"""
    
    if args.termux:
        run_termux_setup()
    elif args.install_sdk:
        install_sdk()
    elif args.mobile or args.doctor_mobile:
        check_mobile_doctor()
    else:
        # Interactive menu
        print(f"{Colors.BOLD}")
        print("╔══════════════════════════════════════════╗")
        print("║          ANVIL - Setup                    ║")
        print("╚══════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"{Colors.BOLD}Setup options:{Colors.END}")
        print("  [1] Setup for Termux (Android)")
        print("  [2] Install Android SDK")
        print("  [3] Mobile doctor (check system)")
        print("  [4] Full system setup")
        
        choice = input("\nSelect [1-4]: ").strip() or "1"
        
        if choice == "1":
            run_termux_setup()
        elif choice == "2":
            install_sdk()
        elif choice == "3":
            check_mobile_doctor()
        elif choice == "4":
            run_termux_setup()
            install_sdk()

def add_parser(subparsers):
    """Add setup command parser"""
    parser = subparsers.add_parser(
        "setup",
        help="Setup ANVIL on different platforms",
        description="Setup wizard for Termux, Android SDK installation, etc."
    )
    parser.add_argument("--termux", action="store_true", help="Setup for Termux")
    parser.add_argument("--install-sdk", action="store_true", help="Install Android SDK")
    parser.add_argument("--mobile", action="store_true", help="Mobile doctor mode")
    parser.add_argument("--doctor-mobile", action="store_true", help="Check mobile system")
    
    return parser