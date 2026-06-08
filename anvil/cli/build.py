"""
ANVIL build - Build APK
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

try:
    from anvil.utils.mobile import is_mobile, get_mobile_optimizations, get_banner
    from anvil.cli.animations import SkeletonKingAnimation
except ImportError:
    from utils.mobile import is_mobile, get_mobile_optimizations, get_banner
    from animations import SkeletonKingAnimation

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
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def run(args):
    """Run the build command"""
    
    # Find config
    config_path = Path("anvil.config.json")
    
    if not config_path.exists():
        print_error("anvil.config.json not found!")
        print_info("Run 'anvil init' first to create a project.")
        return
    
    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    project_dir = Path(".")
    
    # Import generator
    try:
        from anvil.utils.generator import build_apk, print_step as gen_step, print_success as gen_success
    except ImportError:
        from utils.generator import build_apk, print_step as gen_step, print_success as gen_success
    
    # Get banner based on platform
    banner = get_banner() if is_mobile() else f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════╗
║           ANVIL - Build APK              ║
╚══════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)
    
    print_step("CONFIG", f"App: {config['name']}")
    print_info(f"Package: {config['package']}")
    print_info(f"Version: {config['version']}")
    print_info(f"Render: {config.get('renderMode', 'webview')}")
    
    # Apply mobile optimizations if in mobile mode
    optimizations = get_mobile_optimizations()
    if optimizations and is_mobile():
        print_info("Mobile optimizations enabled")
        if args.low_memory:
            print_info("Low memory mode active")
    
    # Build APK - Show Skeleton King animation!
    print()
    print_step("BUILD", "⚡ Forging APK...")
    
    # Run the epic animation
    anim = SkeletonKingAnimation("Compiling Android project...")
    anim.show(progress=1.0)
    
    apk_path = build_apk(project_dir, config, low_memory=args.low_memory)
    
    if apk_path:
        print_success(f"APK built: {apk_path}")
        
        # Get file size
        size_kb = os.path.getsize(apk_path) / 1024
        size_mb = size_kb / 1024
        print_info(f"Size: {size_mb:.1f} MB")
        
        # Copy to apps folder (create if not exists)
        apps_dir = project_dir / "apps"
        apps_dir.mkdir(exist_ok=True)
        
        import shutil
        dest = apps_dir / apk_path.name
        shutil.copy2(apk_path, dest)
        print_success(f"Copied to: {dest}")
        
        # Also create apks symlink for convenience
        apks_dir = project_dir / "apks"
        if apks_dir.is_symlink() or apks_dir.exists():
            if apks_dir.is_symlink():
                apks_dir.unlink()
            elif apks_dir.is_dir():
                shutil.rmtree(apks_dir)
        apks_dir.symlink_to(apps_dir)
        print_info(f"APKs available at: /apks/{apk_path.name}")
    else:
        print_error("Build failed!")
        print_info("Run 'anvil doctor' to check system requirements.")
        sys.exit(1)

def add_parser(subparsers):
    """Add build command parser"""
    parser = subparsers.add_parser(
        "build",
        help="Build APK from project",
        description="Compile the Android project and generate APK"
    )
    parser.add_argument("--release", action="store_true", help="Build release APK")
    parser.add_argument("--sign", action="store_true", help="Sign APK with keystore")
    parser.add_argument("--low-memory", action="store_true", help="Optimize for mobile/low-memory devices")
    
    return parser