"""
ANVIL deploy - Build and install on device
"""

import os
import subprocess
import argparse
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def get_devices():
    """Get list of connected devices"""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True
        )
        
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip() and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2 and parts[1].strip() == 'device':
                    devices.append({
                        'id': parts[0].strip(),
                        'type': 'usb' if 'emulator' not in parts[0] else 'emulator'
                    })
        
        return devices
        
    except FileNotFoundError:
        return []

def install_apk(apk_path: str, device_id: str = None):
    """Install APK on device"""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["install", "-r", apk_path])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def launch_app(package: str, device_id: str = None):
    """Launch the app on device"""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["shell", "am", "start", "-n", f"{package}/.MainActivity"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr

def run(args):
    """Run the deploy command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - Deploy                   ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Check for APK
    dist_dir = Path("dist")
    apks = list(dist_dir.glob("*.apk")) if dist_dir.exists() else []
    
    if not apks:
        print_warning("No APK found in ./dist/")
        print_info("Building APK first...")
        
        # Run build
        from anvil.cli.build import run as build_run
        build_run(args)
        
        # Check again
        apks = list(dist_dir.glob("*.apk")) if dist_dir.exists() else []
    
    if not apks:
        print_warning("Build failed. Cannot deploy.")
        return
    
    apk_path = str(apks[0])
    print_info(f"APK: {apk_path}")
    
    # Get devices
    devices = get_devices()
    
    if not devices:
        print_warning("No devices connected!")
        print_info("Connect device via USB and enable USB debugging")
        print_info("Or start an emulator with: emulator -avd <name>")
        return
    
    # Select device
    device = None
    if len(devices) == 1:
        device = devices[0]
        print_info(f"Using device: {device['id']}")
    else:
        print(f"{Colors.BOLD}Select device:{Colors.END}")
        for i, d in enumerate(devices, 1):
            print(f"  [{i}] {d['id']} ({d['type']})")
        
        choice = input("\nSelect device [1]: ").strip() or "1"
        try:
            idx = int(choice) - 1
            device = devices[idx]
        except:
            device = devices[0]
    
    # Install
    print_info("Installing APK...")
    success, output = install_apk(apk_path, device['id'])
    
    if success:
        print_success("APK installed!")
        
        # Launch
        try:
            # Load config for package name
            import json
            with open("anvil.config.json") as f:
                config = json.load(f)
            package = config.get('package', 'com.example.app')
            
            print_info("Launching app...")
            launch_success, _ = launch_app(package, device['id'])
            
            if launch_success:
                print_success("App launched!")
            else:
                print_info("App installed but not launched (may need manual start)")
                
        except Exception as e:
            print_info(f"Launch skipped: {e}")
    else:
        print_warning(f"Install failed: {output}")

def add_parser(subparsers):
    """Add deploy command parser"""
    parser = subparsers.add_parser(
        "deploy",
        help="Build and install on device",
        description="Build APK and install on connected Android device"
    )
    parser.add_argument("--device", help="Device ID")
    parser.add_argument("--skip-build", action="store_true", help="Skip build step")
    
    return parser