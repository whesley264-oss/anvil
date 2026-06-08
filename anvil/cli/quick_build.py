"""
ANVIL quick-build - Quick build from URL or GitHub
Designed for mobile workflows where you want to build fast from remote sources
"""

import os
import sys
import json
import tempfile
import shutil
import argparse
from pathlib import Path
import urllib.request
import zipfile

# Import mobile detection
try:
    from anvil.utils.mobile import is_mobile, is_termux, get_mobile_optimizations, get_banner
except ImportError:
    from utils.mobile import is_mobile, is_termux, get_mobile_optimizations, get_banner

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

def print_step(step: str, message: str):
    print(f"\n{Colors.BOLD}[{step}]{Colors.END} {message}")

def download_file(url: str, dest: Path) -> bool:
    """Download file from URL"""
    try:
        print_info(f"Downloading: {url}")
        
        # Add progress callback
        def reporthook(blocknum, blocksize, totalsize):
            if totalsize > 0:
                percent = min(100, blocknum * blocksize * 100 // totalsize)
                if blocknum % 100 == 0:
                    print(f"\r  Progress: {percent}%", end='', flush=True)
        
        urllib.request.urlretrieve(url, dest, reporthook)
        print()  # New line after progress
        return True
        
    except Exception as e:
        print_error(f"Download failed: {e}")
        return False

def clone_git_repo(url: str, dest: Path) -> bool:
    """Clone GitHub repository"""
    import subprocess
    
    try:
        print_info(f"Cloning: {url}")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(dest)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print_success("Repository cloned!")
            return True
        else:
            print_error(f"Git clone failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print_error("git not found. Install git first.")
        return False
    except subprocess.TimeoutExpired:
        print_error("Git clone timed out")
        return False

def extract_zip(path: Path, dest: Path):
    """Extract ZIP file"""
    try:
        print_info("Extracting...")
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(dest)
        
        # Find the actual content (ignore root folder)
        items = list(dest.iterdir())
        if len(items) == 1 and items[0].is_dir():
            return items[0]
        
        return dest
        
    except Exception as e:
        print_error(f"Extraction failed: {e}")
        return None

def find_source_dir(temp_dir: Path) -> Path:
    """Find the actual source directory"""
    # Look for common web app markers
    markers = ['index.html', 'package.json', 'src', 'public', 'app']
    
    for marker in markers:
        found = list(temp_dir.rglob(marker))
        if found:
            # Get the parent directory containing the marker
            return found[0].parent
    
    # Default to temp_dir if nothing found
    return temp_dir

def quick_build_from_url(url: str, name: str = None, install: bool = True):
    """Quick build from a URL (ZIP, HTML, or GitHub)"""
    
    banner = get_banner()
    print(banner)
    
    print_step("SOURCE", f"Processing: {url}")
    
    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="anvil_"))
    print_info(f"Temp directory: {temp_dir}")
    
    try:
        # Determine source type
        if url.startswith('https://github.com') and not url.endswith('.zip'):
            # GitHub repo - add .git extension for download
            git_url = url + ("" if url.endswith('.git') else ".git")
            clone_git_repo(git_url, temp_dir)
            source_dir = temp_dir
            
        elif url.endswith('.zip'):
            # ZIP file
            zip_path = temp_dir / "source.zip"
            if download_file(url, zip_path):
                extracted = extract_zip(zip_path, temp_dir)
                if extracted:
                    source_dir = extracted
                else:
                    return
            else:
                return
                
        elif url.endswith(('.html', '.htm')):
            # Single HTML file
            html_path = temp_dir / "index.html"
            if download_file(url, html_path):
                source_dir = temp_dir
            else:
                return
                
        else:
            print_error("Unsupported URL format")
            return
        
        # Find actual source
        source_dir = find_source_dir(source_dir)
        print_success(f"Source found: {source_dir}")
        
        # Generate name if not provided
        if not name:
            name = source_dir.name.replace('-', ' ').replace('_', ' ').title()
        
        # Create minimal config
        package = f"com.anvil.quickbuild.{source_dir.name.lower().replace(' ', '').replace('-', '')}"
        
        config = {
            "name": name,
            "package": package,
            "version": "1.0.0",
            "source": str(source_dir),
            "renderMode": "webview",
            "webview": {"mode": "local"},
            "permissions": ["internet"],
            "features": [],
            "theme": "system"
        }
        
        # Save config
        config_path = temp_dir / "anvil.config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print_success("Config created!")
        print_info(f"Name: {config['name']}")
        print_info(f"Package: {config['package']}")
        
        # Build
        print_step("BUILD", "Starting build...")
        
        from anvil.utils.generator import generate_android_project, build_apk
        
        generate_android_project(temp_dir, config)
        
        # Apply mobile optimizations if needed
        optimizations = get_mobile_optimizations()
        if optimizations:
            print_info("Mobile optimization applied")
        
        # Build APK
        apk_path = build_apk(temp_dir, config)
        
        if apk_path:
            print_success(f"APK built: {apk_path}")
            
            # Get file size
            size_mb = os.path.getsize(apk_path) / (1024 * 1024)
            print_info(f"Size: {size_mb:.1f} MB")
            
            # Copy to current directory
            dest_apk = Path(".") / f"{config['name'].replace(' ', '-')}-{config['version']}.apk"
            shutil.copy2(apk_path, dest_apk)
            print_success(f"Copied to: {dest_apk}")
            
            # Install if requested
            if install:
                print_step("INSTALL", "Installing on device...")
                
                import subprocess
                try:
                    result = subprocess.run(
                        ["adb", "install", "-r", str(dest_apk)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    if result.returncode == 0:
                        print_success("Installed on device!")
                    else:
                        print_warning("Install failed - APK ready at current directory")
                        
                except FileNotFoundError:
                    print_warning("adb not found - APK ready at current directory")
        else:
            print_error("Build failed")
            
    finally:
        # Cleanup temp
        print_info("Cleaning up temp files...")
        shutil.rmtree(temp_dir, ignore_errors=True)

def quick_build_interactive():
    """Interactive quick build"""
    
    banner = get_banner()
    print(banner)
    
    print(f"{Colors.BOLD}Quick Build - Fast APK creation from URL{Colors.END}\n")
    
    # Get URL
    url = input(f"{Colors.BOLD}URL (GitHub, ZIP, or HTML){Colors.END}: ").strip()
    
    if not url:
        print_error("URL required")
        return
    
    # Get name (optional)
    name = input(f"{Colors.BOLD}App name{Colors.END} (optional): ").strip()
    
    # Auto-install option
    auto_install = input("Auto-install on device? [Y/n]: ").strip().lower() != 'n'
    
    # Run build
    quick_build_from_url(url, name or None, auto_install)

def run(args):
    """Run the quick-build command"""
    
    if args.url:
        quick_build_from_url(args.url, args.name, not args.no_install)
    else:
        quick_build_interactive()

def add_parser(subparsers):
    """Add quick-build command parser"""
    parser = subparsers.add_parser(
        "quick-build",
        help="Quick build APK from URL",
        description="Fast build from GitHub, ZIP, or HTML URL (optimized for mobile)"
    )
    parser.add_argument("--url", help="Source URL (GitHub, ZIP, or HTML)")
    parser.add_argument("--name", help="App name")
    parser.add_argument("--no-install", action="store_true", help="Skip auto-install")
    parser.add_argument("--source", help="Local source path (alternative to --url)")
    
    return parser