"""
ANVIL Demo Command - Create a demo app to test ANVIL installation
Shows a welcome page proving ANVIL is working correctly
"""

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path

try:
    from anvil.cli.banner import BANNER, BANNER_SMALL
    from anvil import __version__
except ImportError:
    BANNER = ""
    BANNER_SMALL = ""
    __version__ = "0.3.0"

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'
    MAGENTA = '\033[95m'

DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>ANVIL Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .logo {
            font-size: 48px;
            margin-bottom: 20px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .tagline {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 30px 40px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .status-item {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin: 10px 0;
            font-size: 1.1rem;
        }
        
        .checkmark {
            color: #4ade80;
            font-size: 1.3rem;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            max-width: 500px;
            width: 100%;
        }
        
        .feature {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 15px;
            font-size: 0.9rem;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }
        
        .footer {
            margin-top: 30px;
            opacity: 0.7;
            font-size: 0.85rem;
        }
        
        .github-link {
            color: white;
            text-decoration: none;
            border-bottom: 1px dashed white;
        }
    </style>
</head>
<body>
    <div class="logo">⚒️</div>
    <h1>ANVIL</h1>
    <p class="tagline">Web to APK Converter</p>
    
    <div class="status-card">
        <div class="status-item">
            <span class="checkmark">✅</span>
            <span>ANVIL is working!</span>
        </div>
        <div class="status-item">
            <span class="checkmark">✅</span>
            <span>APK generated successfully</span>
        </div>
        <div class="status-item">
            <span class="checkmark">✅</span>
            <span>Ready for production</span>
        </div>
    </div>
    
    <div class="features">
        <div class="feature">
            <div class="feature-icon">🌐</div>
            <div>WebView Mode</div>
        </div>
        <div class="feature">
            <div class="feature-icon">📱</div>
            <div>Native APK</div>
        </div>
        <div class="feature">
            <div class="feature-icon">⚡</div>
            <div>Fast Build</div>
        </div>
        <div class="feature">
            <div class="feature-icon">🔒</div>
            <div>Secure</div>
        </div>
    </div>
    
    <div class="footer">
        <p>Built with ❤️ by ANVIL</p>
        <p><a class="github-link" href="https://github.com/whesley264-oss/anvil" target="_blank">github.com/whesley264-oss/anvil</a></p>
    </div>
</body>
</html>
"""

try:
    from anvil.cli.banner import BANNER, BANNER_SMALL
    from anvil import __version__
except ImportError:
    BANNER = ""
    BANNER_SMALL = ""
    __version__ = "0.3.0"

def print_step(step: str, message: str):
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def run(args):
    """Run the demo command"""
    
    # Print banner
    print(BANNER)
    print(BANNER_SMALL.format(version=__version__))
    print()
    
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print(f"  Creating a demo app to prove ANVIL is working!")
    print(f"  This will build a simple APK with a welcome page.")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
    print()
    
    # Get app name from args or use default
    app_name = args.name if hasattr(args, 'name') and args.name else "ANVIL-Demo"
    package = args.package if hasattr(args, 'package') and args.package else "com.anvil.demo"
    
    # Create temp project
    print_step("SETUP", "Creating demo project...")
    
    temp_dir = Path(tempfile.mkdtemp(prefix="anvil_demo_"))
    
    # Save demo HTML
    index_path = temp_dir / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(DEMO_HTML)
    print_success("Demo page created!")
    
    # Create config
    config = {
        "name": app_name,
        "author": "ANVIL",
        "author_email": "demo@anvil.dev",
        "website": "https://github.com/whesley264-oss/anvil",
        "package": package,
        "version": "1.0.0",
        "description": "ANVIL demo app - proving your installation works!",
        "source": "index.html",
        "renderMode": "webview",
        "webview": {"mode": "local"},
        "permissions": ["internet"],
        "features": ["offline-cache"],
        "theme": "system"
    }
    
    config_path = temp_dir / "anvil.config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print_success("Config created!")
    print_info(f"App: {app_name}")
    print_info(f"Package: {package}")
    
    # Generate Android project
    print_step("GENERATE", "Generating Android project...")
    
    try:
        from anvil.utils.generator import generate_android_project, build_apk
        
        generate_android_project(temp_dir, config)
        print_success("Android project generated!")
        
        # Build APK
        print_step("BUILD", "Building APK... (this may take a minute)")
        
        apk_path = build_apk(temp_dir, config)
        
        if apk_path:
            print_success(f"APK built: {apk_path}")
            
            # Copy to current directory
            output_name = f"{app_name.replace(' ', '-')}.apk"
            dest_apk = Path.cwd() / output_name
            shutil.copy2(apk_path, dest_apk)
            
            # Get size
            size_mb = os.path.getsize(dest_apk) / (1024 * 1024)
            
            print()
            print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            print(f"{Colors.BOLD}  🎉 SUCCESS! ANVIL is working perfectly!{Colors.END}")
            print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
            print()
            print(f"  📦 APK: {dest_apk}")
            print(f"  📊 Size: {size_mb:.1f} MB")
            print()
            print(f"  {Colors.CYAN}What you can do now:{Colors.END}")
            print(f"  • Install the APK on your Android device")
            print(f"  • Run 'anvil init' to create your own project")
            print(f"  • Run 'anvil quick-build --url <URL>' for quick builds")
            print(f"  • Check 'anvil --help' for all commands")
            print()
            print(f"{Colors.YELLOW}  💡 Tip: Share this APK to prove ANVIL works!{Colors.END}")
            print()
            
            # Ask if user wants to install
            if hasattr(args, 'install') and args.install:
                try:
                    import subprocess
                    print_step("INSTALL", "Installing on device...")
                    result = subprocess.run(
                        ["adb", "install", "-r", str(dest_apk)],
                        capture_output=True, text=True, timeout=60
                    )
                    if result.returncode == 0:
                        print_success("Installed on device!")
                    else:
                        print_info("ADB not connected - APK is ready to install manually")
                except FileNotFoundError:
                    print_info("ADB not found - install APK manually on your device")
        else:
            print_error("Build failed. Check your Android SDK installation.")
            print_info("Run 'anvil doctor' to check requirements.")
            
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup (optional - keep APK)
        if not (args.keep_project if hasattr(args, 'keep_project') else False):
            print_info("Cleaning up temporary files...")
            shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print_info(f"Project saved at: {temp_dir}")

def add_parser(subparsers):
    """Add demo command parser"""
    parser = subparsers.add_parser(
        'demo',
        help='Create a demo APK to test ANVIL installation',
        description='Builds a welcome APK proving ANVIL is working correctly'
    )
    parser.add_argument('--name', default='ANVIL-Demo', help='App name')
    parser.add_argument('--package', default='com.anvil.demo', help='Package ID')
    parser.add_argument('--install', action='store_true', help='Auto-install on device')
    parser.add_argument('--keep-project', action='store_true', help='Keep temp project after build')
    return parser