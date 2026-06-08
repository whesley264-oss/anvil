"""
ANVIL init - Create new project from web app
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Optional

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(step: str, message: str):
    """Print a step message"""
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def ask_question(question: str, default: Optional[str] = None) -> str:
    """Ask a question and return the answer"""
    if default:
        response = input(f"{Colors.BOLD}{question}{Colors.END} [{default}]: ").strip()
        return response if response else default
    else:
        return input(f"{Colors.BOLD}{question}{Colors.END}: ").strip()

def ask_choice(question: str, options: list, default: int = 1) -> int:
    """Ask a choice question and return the index"""
    print(f"\n{Colors.BOLD}{question}{Colors.END}")
    for i, option in enumerate(options, 1):
        marker = "(default)" if i == default else ""
        print(f"  [{i}] {option} {marker}")
    
    while True:
        try:
            response = input(f"\nSelect [1-{len(options)}]: ").strip()
            if not response:
                return default
            idx = int(response)
            if 1 <= idx <= len(options):
                return idx
            print(f"{Colors.RED}Please enter a number between 1 and {len(options)}{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number{Colors.END}")

def ask_multiselect(question: str, options: list) -> list:
    """Ask multi-select question and return selected indices"""
    print(f"\n{Colors.BOLD}{question}{Colors.END}")
    print("(Press SPACE to toggle, ENTER when done)\n")
    
    selected = [True] * len(options)
    
    while True:
        for i, option in enumerate(options):
            marker = "[x]" if selected[i] else "[ ]"
            print(f"  {marker} {option}")
        
        print(f"\n{Colors.CYAN}Press SPACE to toggle, ENTER to confirm{Colors.END}")
        
        key = input()
        if key == '':
            break
        
        # If space was pressed (key might be ' ')
        if key == ' ':
            continue
    
    return [i for i, s in enumerate(selected) if s]

def validate_package_id(package_id: str) -> bool:
    """Validate Android package ID format"""
    parts = package_id.split('.')
    if len(parts) < 2:
        return False
    for part in parts:
        if not part or not part[0].isalpha():
            return False
        if not all(c.isalnum() or c == '_' for c in part):
            return False
    return True

def get_source_path() -> str:
    """Get source path with validation"""
    while True:
        path = input(f"\n{Colors.BOLD}Source path{Colors.END}: ").strip()
        if not path:
            print(f"{Colors.RED}Path cannot be empty{Colors.END}")
            continue
        
        # Handle different source types
        if path.startswith('http://') or path.startswith('https://'):
            return path
        
        # Check if path exists (for local paths)
        resolved = Path(path).expanduser()
        if not resolved.exists():
            print(f"{Colors.RED}Path does not exist: {path}{Colors.END}")
            continue
        
        return str(resolved)

def get_source_type() -> int:
    """Ask how to import the source"""
    print(f"\n{Colors.BOLD}How to import source?{Colors.END}")
    options = [
        "Local folder",
        "GitHub URL",
        "ZIP file",
        "Template starter",
        "Remote URL"
    ]
    return ask_choice("How to import?", options, default=1)

def get_template() -> str:
    """Get template choice"""
    print(f"\n{Colors.BOLD}Select template:{Colors.END}")
    templates = {
        "1": ("blank", "Blank - Empty project"),
        "2": ("vue", "Vue.js starter"),
        "3": ("react", "React starter"),
        "4": ("next", "Next.js starter"),
        "5": ("svelte", "Svelte starter"),
    }
    
    for key, (_, desc) in templates.items():
        print(f"  [{key}] {desc}")
    
    while True:
        choice = input(f"\nSelect [1-{len(templates)}]: ").strip() or "1"
        if choice in templates:
            return templates[choice][0]
    return "blank"

def get_render_mode() -> tuple:
    """Ask render mode and language"""
    print(f"\n{Colors.BOLD}Render mode:{Colors.END}")
    print("  [1] WebView (stable)")
    print("      APK wraps web app in Android WebView")
    print("      • Simpler, faster build")
    print("      • Requires internet or local assets")
    print()
    print("  [2] Native APK (beta/em testes)")
    print("      Generates complete Android project")
    print("      • No WebView dependency")
    print("      • Full native performance")
    print("      • Beta - may have rough edges")
    
    while True:
        choice = input(f"\nSelect render mode [1-2]: ").strip() or "1"
        if choice == "1":
            return "webview", None
        elif choice == "2":
            # Ask for language
            print(f"\n{Colors.BOLD}Language:{Colors.END}")
            print("  [1] Kotlin (recommended) - Modern, concise, null-safe")
            print("  [2] Java - Classic, more examples online")
            
            while True:
                lang_choice = input(f"Select language [1-2]: ").strip() or "1"
                if lang_choice == "1":
                    return "native", "kotlin"
                elif lang_choice == "2":
                    return "native", "java"
                print(f"{Colors.RED}Please enter 1 or 2{Colors.END}")
        print(f"{Colors.RED}Please enter 1 or 2{Colors.END}")

def get_webview_config() -> dict:
    """Get WebView configuration"""
    print(f"\n{Colors.BOLD}WebView mode:{Colors.END}")
    options = [
        "Local assets (file:///android_asset/)",
        "Remote URL (https://app.example.com)",
        "Hybrid (cache + offline fallback) - recommended"
    ]
    choice = ask_choice("How to load content?", options, default=3)
    
    config = {"mode": ["local", "remote", "hybrid"][choice - 1]}
    
    if choice == 2:
        config["url"] = ask_question("Remote URL", "https://")
    elif choice == 3:
        config["url"] = ask_question("Remote URL", "https://")
        config["cache"] = True
    
    return config

def run(args):
    """Run the init command"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║        ANVIL - Project Init Wizard       ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Step 1: Basic Info
    print_step("1", "Basic Information")
    name = ask_question("App name", "My App")
    author = ask_question("Author name", "")
    author_email = ask_question("Author email", "")
    website = ask_question("Website (optional)", "")
    
    while True:
        package = ask_question("Package ID", f"com.programador.{name.lower().replace(' ', '')}")
        if validate_package_id(package):
            break
        print_error("Invalid package ID format!")
        print_info("Format: com.domain.app (must start with letter)")
    
    version = ask_question("Version", "1.0.0")
    description = ask_question("Description", "")
    
    # Step 2: Source
    print_step("2", "Source")
    source_type = get_source_type()
    
    if source_type == 1:  # Local folder
        source = get_source_path()
    elif source_type == 2:  # GitHub
        source = ask_question("GitHub URL", "https://github.com/user/repo")
    elif source_type == 3:  # ZIP
        source = get_source_path()
    elif source_type == 4:  # Template
        source = get_template()
    else:  # Remote URL
        source = ask_question("Remote URL", "https://")
    
    # Step 3: Icon
    print_step("3", "Icon")
    icon_path = ask_question("Icon path (PNG, min 512x512)", "")
    if icon_path:
        icon_path = str(Path(icon_path).expanduser())
        if not Path(icon_path).exists():
            print_warning(f"Icon file not found: {icon_path}")
            icon_path = ""
    
    # Step 4: Splash Screen
    print_step("4", "Splash Screen")
    splash_enabled = ask_question("Enable splash screen?", "n").lower() in ['y', 'yes', 's', 'sim']
    
    splash_config = {"enabled": splash_enabled}
    if splash_enabled:
        splash_config["color"] = ask_question("Background color (hex)", "#000000")
        splash_image = ask_question("Splash image (optional)", "")
        if splash_image:
            splash_config["image"] = str(Path(splash_image).expanduser())
    
    # Step 5: Theme
    print_step("5", "Theme")
    theme_options = ["Light", "Dark", "System default (automatic)"]
    theme_choice = ask_choice("Theme", theme_options, default=3)
    theme = ["light", "dark", "system"][theme_choice - 1]
    
    # Step 6: Permissions
    print_step("6", "Permissions")
    print("Select required permissions:")
    permissions = ask_multiselect("", [
        "Camera",
        "Storage/Filesystem",
        "Bluetooth",
        "Notifications",
        "Contacts",
        "Location",
        "Microphone",
        "Internet"
    ])
    
    permission_map = {
        0: "camera",
        1: "storage",
        2: "bluetooth",
        3: "notifications",
        4: "contacts",
        5: "location",
        6: "microphone",
        7: "internet"
    }
    selected_permissions = [permission_map[p] for p in permissions]
    
    # Step 7: Native Features
    print_step("7", "Native Features")
    features = ask_multiselect("Enable features:", [
        "Pull-to-refresh",
        "Offline cache",
        "OTA updates (remote HTML/JS updates)",
        "Deep links",
        "Biometric authentication"
    ])
    
    feature_map = {
        0: "pull-to-refresh",
        1: "offline-cache",
        2: "ota-updates",
        3: "deep-links",
        4: "biometric"
    }
    selected_features = [feature_map[f] for f in features]
    
    # Step 8: Render Mode
    print_step("8", "Render Mode")
    render_mode, language = get_render_mode()
    
    webview_config = {}
    if render_mode == "webview":
        webview_config = get_webview_config()
    
    # Step 9: Publishing
    print_step("9", "Publishing")
    create_github = ask_question("Create GitHub repository?", "n").lower() in ['y', 'yes', 's', 'sim']
    github_private = ask_question("Private repository?", "yes").lower() in ['y', 'yes', 's', 'sim']
    
    # Build config
    config = {
        "name": name,
        "author": author,
        "authorEmail": author_email,
        "website": website if website else None,
        "package": package,
        "version": version,
        "description": description,
        "source": source,
        "language": language,
        "icon": icon_path if icon_path else None,
        "splash": splash_config,
        "theme": theme,
        "permissions": selected_permissions,
        "features": selected_features,
        "renderMode": render_mode,
        "publish": {
            "github": create_github,
            "private": github_private
        }
    }
    
    if webview_config:
        config["webview"] = webview_config
    
    # Save config
    print_step("SAVE", "Saving configuration")
    
    config_path = Path("anvil.config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print_success(f"Config saved: {config_path}")
    
    # Copy/create source structure
    project_dir = Path(".")
    
    # Create Android project structure
    print_step("GENERATE", "Generating Android project structure")
    
    from anvil.utils.generator import generate_android_project
    generate_android_project(project_dir, config)
    
    print_success("Android project generated!")
    
    # Create GitHub repo if requested
    if create_github:
        print_step("GITHUB", "Creating GitHub repository...")
        from anvil.utils.github import create_github_repo
        repo_url = create_github_repo(name, description, private=github_private)
        if repo_url:
            print_success(f"Repository created: {repo_url}")
        else:
            print_warning("Could not create GitHub repository")
            print_info("Create it manually at https://github.com/new")
    
    print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
    print(f"  {Colors.CYAN}anvil build{Colors.END}  - Build the APK")
    print(f"  {Colors.CYAN}anvil doctor{Colors.END} - Check system requirements")
    print(f"  {Colors.CYAN}anvil preview{Colors.END} - Test in browser")

def add_parser(subparsers):
    """Add init command parser"""
    parser = subparsers.add_parser(
        "init",
        help="Create new project from web app",
        description="Start interactive wizard to create new ANVIL project"
    )
    parser.add_argument("--name", help="App name")
    parser.add_argument("--package", help="Package ID (com.domain.app)")
    parser.add_argument("--source", help="Source path/URL")
    parser.add_argument("--template", help="Use template (blank, vue, react)")
    parser.add_argument("--non-interactive", action="store_true", help="Skip prompts")
    
    return parser