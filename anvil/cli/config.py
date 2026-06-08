"""
ANVIL config - Manage project configuration
"""

import os
import json
import argparse
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def view_config():
    """View current configuration"""
    config_path = Path("anvil.config.json")
    
    if not config_path.exists():
        print("No anvil.config.json found.")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print(f"\n{Colors.BOLD}Current Configuration:{Colors.END}\n")
    print(json.dumps(config, indent=2))

def edit_config():
    """Interactive config editor"""
    config_path = Path("anvil.config.json")
    
    if not config_path.exists():
        print("No anvil.config.json found.")
        print("Run 'anvil init' first.")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print(f"\n{Colors.BOLD}Edit Configuration{Colors.END}")
    print("Press Enter to keep current value.\n")
    
    # Edit app name
    new_name = input(f"App name [{config.get('name', '')}]: ").strip()
    if new_name:
        config['name'] = new_name
    
    # Edit version
    new_version = input(f"Version [{config.get('version', '')}]: ").strip()
    if new_version:
        config['version'] = new_version
    
    # Edit description
    new_desc = input(f"Description [{config.get('description', '')}]: ").strip()
    if new_desc:
        config['description'] = new_desc
    
    # Save
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print_success("Configuration updated!")

def export_template():
    """Export config as template"""
    config_path = Path("anvil.config.json")
    
    if not config_path.exists():
        print("No anvil.config.json found.")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Remove user-specific fields
    template = config.copy()
    template['name'] = "TemplateName"
    template['package'] = "com.template.app"
    template['version'] = "1.0.0"
    template['source'] = "./src"
    
    template_path = Path("anvil.template.json")
    with open(template_path, 'w') as f:
        json.dump(template, f, indent=2)
    
    print_success(f"Template exported to: {template_path}")

def add_permission():
    """Add a permission to config"""
    config_path = Path("anvil.config.json")
    
    if not config_path.exists():
        print("No anvil.config.json found.")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    available = ["camera", "storage", "bluetooth", "notifications", "contacts", "location", "microphone", "internet"]
    current = config.get('permissions', [])
    
    print(f"\n{Colors.BOLD}Add Permission{Colors.END}")
    print(f"Current permissions: {current or 'none'}")
    print("\nAvailable:")
    for i, perm in enumerate(available, 1):
        marker = "(added)" if perm in current else ""
        print(f"  [{i}] {perm} {marker}")
    
    choice = input("\nSelect permission [1-8]: ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(available):
            perm = available[idx]
            if perm not in current:
                current.append(perm)
                config['permissions'] = current
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print_success(f"Added permission: {perm}")
            else:
                print_info(f"Permission already added: {perm}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")

def run(args):
    """Run the config command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - Config                    ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    if args.view:
        view_config()
    elif args.edit:
        edit_config()
    elif args.template:
        export_template()
    elif args.add_permission:
        add_permission()
    else:
        # Interactive menu
        print(f"{Colors.BOLD}Config options:{Colors.END}")
        print("  [1] View current config")
        print("  [2] Edit config")
        print("  [3] Add permission")
        print("  [4] Export as template")
        
        choice = input("\nSelect [1-4]: ").strip() or "1"
        
        if choice == "1":
            view_config()
        elif choice == "2":
            edit_config()
        elif choice == "3":
            add_permission()
        elif choice == "4":
            export_template()

def add_parser(subparsers):
    """Add config command parser"""
    parser = subparsers.add_parser(
        "config",
        help="Manage project configuration",
        description="View, edit, or export anvil.config.json"
    )
    parser.add_argument("--view", action="store_true", help="View current config")
    parser.add_argument("--edit", action="store_true", help="Edit config")
    parser.add_argument("--add-permission", action="store_true", help="Add a permission")
    parser.add_argument("--template", action="store_true", help="Export as template")
    
    return parser