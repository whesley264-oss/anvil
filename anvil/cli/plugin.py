"""
ANVIL plugin - Manage plugins
"""

import os
import json
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

BUILTIN_PLUGINS = {
    "camera": {
        "name": "Camera Plugin",
        "description": "Access device camera for photos and videos",
        "version": "1.0.0",
    },
    "firebase": {
        "name": "Firebase Plugin", 
        "description": "Push notifications, analytics, and auth",
        "version": "1.0.0",
    },
    "biometric": {
        "name": "Biometric Plugin",
        "description": "Fingerprint and face authentication",
        "version": "1.0.0",
    },
    "location": {
        "name": "Location Plugin",
        "description": "GPS and location services",
        "version": "1.0.0",
    },
    "share": {
        "name": "Share Plugin",
        "description": "Share content to other apps",
        "version": "1.0.0",
    },
}

def list_plugins():
    """List available plugins"""
    print(f"\n{Colors.BOLD}Available Plugins:{Colors.END}\n")
    
    for name, info in BUILTIN_PLUGINS.items():
        print(f"  {Colors.CYAN}{name}{Colors.END}")
        print(f"    {info['description']}")
        print(f"    Version: {info['version']}")
        print()
    
    # Check installed plugins
    plugins_dir = Path("plugins")
    if plugins_dir.exists():
        installed = list(plugins_dir.iterdir())
        if installed:
            print(f"{Colors.BOLD}Installed:{Colors.END}")
            for p in installed:
                print(f"  {Colors.GREEN}{p.name}{Colors.END}")

def add_plugin(plugin_name: str):
    """Add a plugin to the project"""
    
    if plugin_name in BUILTIN_PLUGINS:
        info = BUILTIN_PLUGINS[plugin_name]
        print_info(f"Adding {info['name']}...")
        
        # Create plugins directory
        plugins_dir = Path("plugins")
        plugins_dir.mkdir(exist_ok=True)
        
        # Create plugin config
        plugin_dir = plugins_dir / plugin_name
        plugin_dir.mkdir(exist_ok=True)
        
        plugin_config = {
            "name": info["name"],
            "version": info["version"],
            "description": info["description"],
            "enabled": True,
        }
        
        with open(plugin_dir / "plugin.json", 'w') as f:
            json.dump(plugin_config, f, indent=2)
        
        print_success(f"Plugin '{plugin_name}' added!")
        print_info("Run 'anvil build' to apply changes")
        
    else:
        print_warning(f"Plugin '{plugin_name}' not found.")
        print_info(f"Available: {', '.join(BUILTIN_PLUGINS.keys())}")

def remove_plugin(plugin_name: str):
    """Remove a plugin from the project"""
    plugin_dir = Path("plugins") / plugin_name
    
    if plugin_dir.exists():
        import shutil
        shutil.rmtree(plugin_dir)
        print_success(f"Plugin '{plugin_name}' removed!")
    else:
        print_warning(f"Plugin '{plugin_name}' not found.")

def install_from_url(url: str):
    """Install plugin from GitHub URL"""
    print_info(f"Installing from: {url}")
    
    import subprocess
    
    try:
        # Clone plugin repo
        plugin_name = url.split('/')[-1].replace('.git', '')
        dest = Path("plugins") / plugin_name
        dest.mkdir(parents=True, exist_ok=True)
        
        result = subprocess.run(
            ["git", "clone", url, str(dest)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Plugin installed: {plugin_name}")
        else:
            print_warning(f"Failed to clone: {result.stderr}")
            
    except Exception as e:
        print_warning(f"Install failed: {e}")

def run(args):
    """Run the plugin command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - Plugin Manager           ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    if args.list:
        list_plugins()
    elif args.add:
        add_plugin(args.add)
    elif args.remove:
        remove_plugin(args.remove)
    elif args.install:
        install_from_url(args.install)
    else:
        # Interactive menu
        print(f"{Colors.BOLD}Plugin options:{Colors.END}")
        print("  [1] List available plugins")
        print("  [2] Add a plugin")
        print("  [3] Remove a plugin")
        print("  [4] Install from URL")
        
        choice = input("\nSelect [1-4]: ").strip() or "1"
        
        if choice == "1":
            list_plugins()
        elif choice == "2":
            plugin = input("Plugin name: ").strip()
            if plugin:
                add_plugin(plugin)
        elif choice == "3":
            plugin = input("Plugin name to remove: ").strip()
            if plugin:
                remove_plugin(plugin)
        elif choice == "4":
            url = input("GitHub URL: ").strip()
            if url:
                install_from_url(url)

def add_parser(subparsers):
    """Add plugin command parser"""
    parser = subparsers.add_parser(
        "plugin",
        help="Manage plugins",
        description="List, add, or remove ANVIL plugins"
    )
    parser.add_argument("--list", action="store_true", help="List available plugins")
    parser.add_argument("--add", metavar="NAME", help="Add a plugin")
    parser.add_argument("--remove", metavar="NAME", help="Remove a plugin")
    parser.add_argument("--install", metavar="URL", help="Install from URL")
    
    return parser