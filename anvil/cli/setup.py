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
        
        print_info("Downloading Android command-line tools (~150MB)...")
        
        # Download command-line tools
        sdk_dir = Path.home() / "android-sdk"
        sdk_dir.mkdir(exist_ok=True)
        
        cmdline_tools_url = "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
        
        try:
            import urllib.request
            import zipfile
            
            zip_path = sdk_dir / "cmdline-tools.zip"
            
            # Download with progress
            def progress(count, block_size, total_size):
                if total_size > 0:
                    percent = int(count * block_size * 100 / total_size)
                    if percent % 10 == 0:
                        print(f"\r{Colors.CYAN}   Downloading: {percent}%{Colors.END}", end="", flush=True)
            
            urllib.request.urlretrieve(cmdline_tools_url, zip_path, reporthook=progress)
            print()
            print_success("Download complete!")
            
            # Extract
            print_info("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(sdk_dir)
            
            # Organize structure
            cmdline_tools = sdk_dir / "cmdline-tools"
            latest = cmdline_tools / "latest"
            latest.mkdir(parents=True, exist_ok=True)
            
            extracted_tools = cmdline_tools / "cmdline-tools"
            if extracted_tools.exists():
                import shutil
                for item in extracted_tools.glob("*"):
                    shutil.move(str(item), str(latest / item.name))
                shutil.rmtree(extracted_tools)
            
            zip_path.unlink()
            print_success("Android SDK installed!")
            sdk_path = str(sdk_dir)
            
            # Accept licenses
            sdkmanager = latest / "bin" / "sdkmanager"
            if sdkmanager.exists():
                print_info("Accepting licenses...")
                subprocess.run([str(sdkmanager), "--licenses"], input=b"y\ny\ny\ny\ny\ny\ny\n", cwd=sdk_dir)
                
                print_info("Installing basic packages (platform-tools, android-34, build-tools)...")
                subprocess.run([str(sdkmanager), "platform-tools", "platforms;android-34", "build-tools;34.0.0"], cwd=sdk_dir)
                print_success("Basic packages installed!")
                
        except Exception as e:
            print_warning(f"SDK download failed: {e}")
            print_info("You can run 'anvil setup --install-sdk' later")
    
    # Step 4: Setup environment variables
    print_step("4", "Setting up environment variables...")
    
    # Create termux startup script
    termux_bashrc = Path.home() / ".bashrc"
    termux_profile = Path.home() / ".profile"
    
    # Find Java path
    java_home_path = "$PREFIX/lib/jvm/java-17-openjdk"
    if not Path(os.path.expandvars(java_home_path)).exists():
        # Try alternative paths
        for jpath in ["$PREFIX/lib/jvm/java-17", "$PREFIX/opt/openjdk"]:
            if Path(os.path.expandvars(jpath)).exists():
                java_home_path = jpath
                break
    
    # Use the downloaded SDK path or default
    android_home_path = sdk_path or "$HOME/android-sdk"
    
    env_lines = [
        "",
        "# ANVIL Environment Variables",
        f"export ANDROID_HOME={android_home_path}",
        f"export ANDROID_SDK_ROOT={android_home_path}",
        f"export JAVA_HOME={java_home_path}",
        f"export PATH=$PATH:$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools",
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
        import zipfile
        
        print_info(f"Downloading from: {cmdline_tools_url}")
        zip_path = sdk_dir / "cmdline-tools.zip"
        
        # Download with progress
        def progress(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                if percent % 10 == 0:
                    print(f"\r{Colors.CYAN}ℹ Progress: {percent}%{Colors.END}", end="", flush=True)
        
        urllib.request.urlretrieve(cmdline_tools_url, zip_path, reporthook=progress)
        print()  # New line after progress
        
        print_success("Download complete!")
        
        # Extract
        print_info("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sdk_dir)
        
        # Organize structure: cmdline-tools/latest/bin
        cmdline_tools = sdk_dir / "cmdline-tools"
        
        # Remove any existing latest folder
        latest = cmdline_tools / "latest"
        if latest.exists():
            import shutil
            shutil.rmtree(latest)
        
        # Create latest directory
        latest.mkdir(parents=True, exist_ok=True)
        
        # Move contents from the extracted cmdline-tools folder
        extracted_tools = cmdline_tools / "cmdline-tools"
        if extracted_tools.exists():
            import shutil
            for item in extracted_tools.glob("*"):
                shutil.move(str(item), str(latest / item.name))
            shutil.rmtree(extracted_tools)
        
        # Cleanup
        zip_path.unlink()
        
        print_success(f"Android SDK installed to: {sdk_dir}")
        
        # Set environment variables for this session
        os.environ["ANDROID_HOME"] = str(sdk_dir)
        os.environ["ANDROID_SDK_ROOT"] = str(sdk_dir)
        
        # Add to shell config
        shell_rc = Path.home() / ".bashrc"
        if Path.home() / ".zshrc":
            shell_rc = Path.home() / ".zshrc"
        
        env_lines = [
            "",
            "# Android SDK for ANVIL",
            f"export ANDROID_HOME={sdk_dir}",
            f"export ANDROID_SDK_ROOT={sdk_dir}",
            f"export PATH=$PATH:{sdk_dir}/cmdline-tools/latest/bin:{sdk_dir}/platform-tools",
        ]
        
        with open(shell_rc, 'a') as f:
            for line in env_lines:
                f.write(line + "\n")
        
        print_success("Environment variables configured!")
        print_info(f"Added to {shell_rc}")
        
        # Try to accept licenses
        sdkmanager = latest / "bin" / "sdkmanager"
        if sdkmanager.exists():
            print_info("Accepting Android SDK licenses...")
            subprocess.run([str(sdkmanager), "--licenses"], input=b"y\ny\ny\ny\ny\ny\ny\n", cwd=sdk_dir)
            print_success("Licenses accepted!")
            
            # Install basic packages
            print_info("Installing basic SDK packages...")
            subprocess.run([str(sdkmanager), "platform-tools", "platforms;android-34", "build-tools;34.0.0"], cwd=sdk_dir)
            print_success("Basic packages installed!")
        
        print(f"\n{Colors.BOLD}SDK Installation Complete!{Colors.END}")
        print(f"  ANDROID_HOME={sdk_dir}")
        print(f"\nRun 'source {shell_rc}' to reload environment")
        
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