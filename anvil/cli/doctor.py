"""
ANVIL doctor - Check system requirements
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_ok(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_warn(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_fail(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def check_java():
    """Check Java installation"""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True
        )
        
        # Parse version from stderr
        version_line = result.stderr.split('\n')[0]
        version = version_line.split('"')[1].split('.')[0] if '"' in version_line else "?"
        
        if int(version.replace("1.", "").split(".")[0]) >= 11:
            try:
                display_version = version_line.split('"')[1] if '"' in version_line else version_line.split("'")[1]
            except:
                display_version = version
            print_ok(f"Java JDK {display_version}")
            return True
        else:
            print_warn(f"Java {version} found (requires 11+)")
            return True  # Warning, not failure
            
    except FileNotFoundError:
        print_fail("Java JDK not found")
        return False

def check_gradle():
    """Check Gradle installation"""
    try:
        result = subprocess.run(
            ["gradle", "--version"],
            capture_output=True,
            text=True
        )
        
        version_line = result.stdout.split('\n')[0]
        print_ok(f"Gradle installed")
        return True
        
    except FileNotFoundError:
        print_warn("Gradle not in PATH (will use gradlew)")
        return True  # Warning only

def check_android_sdk():
    """Check Android SDK"""
    android_home = os.environ.get('ANDROID_HOME')
    android_sdk_root = os.environ.get('ANDROID_SDK_ROOT')
    
    sdk_path = android_home or android_sdk_root
    
    if sdk_path and Path(sdk_path).exists():
        print_ok(f"Android SDK: {sdk_path}")
        return True
    else:
        print_warn("ANDROID_HOME not set")
        return False

def check_internet():
    """Check internet connection"""
    import urllib.request
    try:
        urllib.request.urlopen('https://google.com', timeout=5)
        print_ok("Internet connection")
        return True
    except:
        print_warn("No internet connection")
        return False

def check_keystore():
    """Check keystore presence"""
    if Path("release.keystore").exists():
        print_ok("release.keystore found")
        return True
    else:
        print_warn("release.keystore not found")
        print_info("Run 'anvil sign --generate' to create one")
        return False

def check_config():
    """Check anvil.config.json"""
    if Path("anvil.config.json").exists():
        print_ok("anvil.config.json found")
        return True
    else:
        print_warn("anvil.config.json not found")
        print_info("Run 'anvil init' to create project")
        return False

def check_platform_tools():
    """Check if adb is available"""
    try:
        result = subprocess.run(
            ["adb", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_ok("Android Platform Tools (adb)")
            return True
    except:
        pass
    
    print_warn("adb not found (required for deploy)")
    return False

def fix_java():
    """Fix Java installation"""
    print_info("Attempting to fix Java...")
    
    # Check if we're on Termux
    if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
        print_info("Detected Termux. Install Java with:")
        print("  pkg install openjdk-17")
        return False
    
    # Check if we're on Linux
    if os.path.exists("/usr/bin/apt"):
        print_info("Installing OpenJDK 17...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
            subprocess.run(["sudo", "apt", "install", "-y", "openjdk-17-jdk"], check=True, capture_output=True)
            print_ok("Java installed. Restart terminal and run 'anvil doctor' again.")
            return True
        except:
            print_fail("Failed to install Java")
            return False
    
    print_info("Please install Java manually from https://adoptium.net/")
    return False

def fix_android_sdk():
    """Fix Android SDK"""
    print_info("Attempting to fix Android SDK...")
    
    if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
        print_info("On Termux, install SDK with:")
        print("  pkg install android-sdk")
        return False
    
    print_info("Android SDK needs to be downloaded from:")
    print("  https://developer.android.com/studio#command-line-tools")
    print()
    print_info("Or run: anvil setup --install-sdk")
    return False

def fix_adb():
    """Fix ADB installation"""
    print_info("Platform tools (ADB) can be installed via:")
    print("  sdkmanager --install platform-tools")
    return False

def accept_licenses():
    """Accept Android SDK licenses"""
    android_home = os.environ.get('ANDROID_HOME')
    android_sdk_root = os.environ.get('ANDROID_SDK_ROOT')
    sdk_path = android_home or android_sdk_root or "/opt/android-sdk"
    
    if Path(sdk_path).exists():
        licenses_dir = Path(sdk_path) / "licenses"
        licenses_dir.mkdir(parents=True, exist_ok=True)
        
        # Write accepted licenses
        licenses = {
            "android-sdk-license": "24333f8a63b6825ea9c5514f83c2829b004d1fee",
            "android-sdk-preview-license": "d56f5187479451eabf01fb78af6dfcb131a6481e"
        }
        
        for name, content in licenses.items():
            license_file = licenses_dir / name
            if not license_file.exists():
                license_file.write_text(content)
        
        print_ok("Android SDK licenses accepted")
        return True
    
    print_warn("Android SDK not found. Install SDK first.")
    return False

def fix_issues(args):
    """Attempt to fix detected issues"""
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║          Auto-Fix Mode                    ║")
    print("╚══════════════════════════════════════════╝{Colors.END}\n")
    
    fixed_count = 0
    
    # Check for Java
    try:
        subprocess.run(["java", "-version"], capture_output=True, check=True)
        print_ok("Java already installed")
    except:
        print_info("\nFixing Java...")
        if fix_java():
            fixed_count += 1
    
    # Check for Android SDK
    sdk_path = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if not sdk_path or not Path(sdk_path).exists():
        print_info("\nFixing Android SDK...")
        fix_android_sdk()
    
    # Accept licenses
    print_info("\nAccepting Android SDK licenses...")
    accept_licenses()
    
    print()
    if fixed_count > 0:
        print_ok(f"Fixed {fixed_count} issue(s)")
        print_info("Run 'anvil doctor' again to verify")
    else:
        print_info("Some issues require manual intervention")

def run(args):
    """Run the doctor command"""
    
    if args.fix:
        fix_issues(args)
        return
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - System Check             ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    checks = [
        ("Java JDK", check_java),
        ("Gradle", check_gradle),
        ("Android SDK", check_android_sdk),
        ("Internet", check_internet),
        ("Keystore", check_keystore),
        ("Config", check_config),
        ("Platform Tools", check_platform_tools),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"{Colors.BOLD}Checking {name}...{Colors.END}")
        result = check_func()
        results.append((name, result))
        print()
    
    # Summary
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"{Colors.BOLD}Summary:{Colors.END} {passed}/{total} checks passed")
    
    if passed == total:
        print_ok("System ready for building!")
    else:
        print_warn("Some issues detected. Use 'anvil doctor --fix' for auto-fix")
        print_info("Or run 'anvil setup' for guided setup")

def add_parser(subparsers):
    """Add doctor command parser"""
    parser = subparsers.add_parser(
        "doctor",
        help="Check system requirements",
        description="Verify Java, Gradle, Android SDK, and other requirements"
    )
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
    
    return parser