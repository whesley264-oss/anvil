"""
ANVIL clean - Clean build artifacts, cache, and generated files
"""

import os
import shutil
import argparse
from pathlib import Path

from anvil.utils.i18n import _

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

def get_size(path: Path) -> str:
    """Get human-readable size"""
    size = 0
    if path.is_file():
        size = path.stat().st_size
    elif path.is_dir():
        for item in path.rglob("*"):
            if item.is_file():
                size += item.stat().st_size
    
    # Convert to MB
    size_mb = size / (1024 * 1024)
    if size_mb < 1:
        return f"{size / 1024:.1f} KB"
    return f"{size_mb:.1f} MB"

def clean_directory(dir_path: Path, dry_run: bool = False) -> int:
    """Clean a directory and return size freed"""
    if not dir_path.exists():
        return 0
    
    total_size = 0
    deleted_count = 0
    
    try:
        for item in list(dir_path.rglob("*")):
            if item.is_file():
                size = item.stat().st_size
                total_size += size
                
                if not dry_run:
                    item.unlink()
                deleted_count += 1
            elif item.is_dir() and not any(item.iterdir()):
                if not dry_run:
                    item.rmdir()
        
        # Remove the directory itself
        if not dry_run and dir_path.exists():
            shutil.rmtree(dir_path)
        
    except Exception as e:
        print_error(f"Error cleaning {dir_path}: {e}")
    
    return total_size

def run(args):
    """Run the clean command"""
    
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║         ANVIL Clean                   ║")
    print("╚══════════════════════════════════════════╝{Colors.END}\n")
    
    project_dir = Path(args.project) if args.project else Path(".")
    
    # Define targets to clean
    targets = []
    
    if args.all or args.gradle:
        targets.append(("Gradle", project_dir / "android" / ".gradle"))
        targets.append(("Gradle (root)", project_dir / ".gradle"))
    
    if args.all or args.build:
        targets.append(("Build", project_dir / "android" / "build"))
        targets.append(("Build (root)", project_dir / "build"))
    
    if args.all or args.dist:
        targets.append(("Dist", project_dir / "dist"))
    
    if args.all or args.cache:
        targets.append(("Cache", project_dir / "__pycache__"))
        targets.append(("Android cache", project_dir / "android" / ".cxx"))
    
    if args.all or args.temp:
        targets.append(("Temp", project_dir / "tmp"))
        targets.append(("Temp", project_dir / "temp"))
    
    if not targets:
        print_info("No targets specified. Use --all or specific options.")
        print()
        print(f"{Colors.BOLD}Options:{Colors.END}")
        print("  --all      Clean everything")
        print("  --gradle    Clean Gradle cache")
        print("  --build     Clean build directories")
        print("  --dist      Clean dist folder")
        print("  --cache     Clean Python/Android cache")
        print("  --temp      Clean temp folders")
        print()
        return
    
    if args.dry_run:
        print_warning("DRY RUN - No files will be deleted")
        print()
    
    total_freed = 0
    
    print(f"{Colors.BOLD}Cleaning targets:{Colors.END}\n")
    
    for name, path in targets:
        if path.exists():
            size = get_size(path)
            print_info(f"  {name}: {path} ({size})")
            
            if not args.dry_run:
                freed = clean_directory(path)
                if freed > 0:
                    print_success(f"  Cleaned: {freed / (1024*1024):.1f} MB")
        else:
            print(f"  {Colors.YELLOW}⚠{Colors.END} {name}: not found")
    
    print()
    
    # Calculate total freed
    for _, path in targets:
        if path.exists() and not args.dry_run:
            pass  # Already counted above
    
    if args.dry_run:
        print_warning("DRY RUN complete - run without --dry-run to actually delete")
    else:
        print_success("Clean complete!")
    
    print()
    print_info(f"Project: {project_dir.absolute()}")
    print()

def add_parser(subparsers):
    """Add clean command parser"""
    parser = subparsers.add_parser(
        "clean",
        help="Clean build artifacts, cache, and temp files",
        description="Remove Gradle cache, build directories, and temporary files to free space"
    )
    parser.add_argument("--all", action="store_true", help="Clean everything")
    parser.add_argument("--gradle", action="store_true", help="Clean Gradle cache")
    parser.add_argument("--build", action="store_true", help="Clean build directories")
    parser.add_argument("--dist", action="store_true", help="Clean dist folder")
    parser.add_argument("--cache", action="store_true", help="Clean Python/Android cache")
    parser.add_argument("--temp", action="store_true", help="Clean temp folders")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    parser.add_argument("--project", help="Project directory (default: current)")
    
    return parser