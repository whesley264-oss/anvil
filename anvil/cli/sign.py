"""
ANVIL sign - Generate keystore and sign APK
"""

import os
import sys
import argparse
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step: str, message: str):
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def ask_password() -> str:
    """Ask for password without echo"""
    import getpass
    return getpass.getpass(f"{Colors.BOLD}Password{Colors.END}: ")

def run(args):
    """Run the sign command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - Sign APK                 ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Check for keystore generation
    if args.generate or args.name is None:
        generate_keystore()
    else:
        sign_apk(args)

def generate_keystore():
    """Generate a new keystore"""
    
    print_step("KEYSTORE", "Generate new keystore")
    
    # Get parameters
    keystore_path = input(f"{Colors.BOLD}Keystore path{Colors.END} [release.keystore]: ").strip()
    if not keystore_path:
        keystore_path = "release.keystore"
    
    # Validate path
    if Path(keystore_path).exists():
        response = input(f"{Colors.YELLOW}Keystore exists. Overwrite? [y/N]: {Colors.END}")
        if response.lower() not in ['y', 'yes']:
            print_info("Keystore generation cancelled.")
            return
    
    key_alias = input(f"{Colors.BOLD}Key alias{Colors.END} [release]: ").strip() or "release"
    store_password = ask_password()
    key_password = ask_password()
    
    # Generate keystore using keytool
    import subprocess
    
    cmd = [
        "keytool",
        "-genkeypair",
        "-v",
        "-keystore", keystore_path,
        "-alias", key_alias,
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", "10000",
        "-storepass", store_password,
        "-keypass", key_password,
        "-dname", f"CN=ANVIL, OU=Development, O=ANVIL, L=City, ST=State, C=US"
    ]
    
    print_info("Generating keystore...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"Keystore created: {keystore_path}")
            print_info(f"Alias: {key_alias}")
            print_info(f"Store password: {'*' * len(store_password)}")
            print_info(f"Key password: {'*' * len(key_password)}")
            
            print(f"\n{Colors.BOLD}Update anvil.config.json with:{Colors.END}")
            print(f"""
  "keystore": {{
    "path": "{keystore_path}",
    "alias": "{key_alias}",
    "storePassword": "{store_password}",
    "keyPassword": "{key_password}"
  }}
""")
        else:
            print_error("Failed to generate keystore!")
            print_info("Make sure Java JDK is installed and keytool is in PATH")
            print(f"Error: {result.stderr}")
            
    except FileNotFoundError:
        print_error("keytool not found!")
        print_info("Install Java JDK or add it to PATH")

def sign_apk(args):
    """Sign an existing APK"""
    
    print_step("SIGN", "Sign APK")
    
    # Find APK
    apk_path = args.apk or "dist/app-release.apk"
    keystore = args.keystore or "release.keystore"
    alias = args.name or "release"
    
    if not Path(apk_path).exists():
        print_error(f"APK not found: {apk_path}")
        print_info("Run 'anvil build --release' first")
        return
    
    if not Path(keystore).exists():
        print_error(f"Keystore not found: {keystore}")
        print_info("Run 'anvil sign --generate' first")
        return
    
    print_info(f"Signing: {apk_path}")
    print_info(f"Keystore: {keystore}")
    print_info(f"Alias: {alias}")
    
    # Sign using apksigner
    import subprocess
    
    cmd = [
        "apksigner", "sign",
        "--ks", keystore,
        "--ks-key-alias", alias,
        "--out", apk_path.replace(".apk", "-signed.apk"),
        apk_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success(f"APK signed: {apk_path.replace('.apk', '-signed.apk')}")
        else:
            print_error("Signing failed!")
            print(f"Error: {result.stderr}")
            
    except FileNotFoundError:
        print_error("apksigner not found!")
        print_info("Install Android SDK Build Tools")

def add_parser(subparsers):
    """Add sign command parser"""
    parser = subparsers.add_parser(
        "sign",
        help="Generate keystore or sign APK",
        description="Generate keystore and sign APK for release"
    )
    parser.add_argument("--generate", action="store_true", help="Generate new keystore")
    parser.add_argument("--keystore", help="Path to keystore file")
    parser.add_argument("--alias", dest="name", help="Key alias name")
    parser.add_argument("--apk", help="APK file to sign")
    
    return parser