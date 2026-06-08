"""
ANVIL inspect - Analyze websites for conversion to APK
"""

import os
import sys
import re
import json
import argparse
import urllib.request
from urllib.parse import urlparse
from typing import Dict, List, Optional

try:
    from anvil.utils.i18n import _
except ImportError:
    from utils.i18n import _

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
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

def print_section(title: str):
    print(f"\n{Colors.BOLD}{'═' * 40}{Colors.END}")
    print(f"{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.BOLD}{'═' * 40}{Colors.END}\n")

def fetch_url(url: str) -> Optional[str]:
    """Fetch HTML content from URL"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def check_pwa(html: str) -> Dict:
    """Check if site is a PWA"""
    result = {
        "detected": False,
        "manifest": False,
        "service_worker": False,
        "icons": [],
        "name": None,
        "short_name": None
    }
    
    # Check for manifest link
    manifest_match = re.search(r'<link[^>]*rel=["\']manifest["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if manifest_match:
        result["manifest"] = True
        result["detected"] = True
    
    # Check for service worker
    if 'serviceworker' in html.lower() or 'service-worker' in html.lower():
        result["service_worker"] = True
        result["detected"] = True
    
    # Check meta theme color
    theme_color = re.search(r'<meta[^>]*name=["\']theme-color["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if theme_color:
        result["theme_color"] = theme_color.group(1)
    
    return result

def check_responsive(html: str) -> Dict:
    """Check if site is responsive"""
    result = {
        "viewport": False,
        "media_queries": 0,
        "flexbox": False,
        "grid": False
    }
    
    # Check viewport meta
    if re.search(r'<meta[^>]*name=["\']viewport["\']', html, re.IGNORECASE):
        result["viewport"] = True
    
    # Count media queries
    result["media_queries"] = len(re.findall(r'@media', html, re.IGNORECASE))
    
    # Check for flexbox/grid
    if 'display: flex' in html or 'display:-webkit-flex' in html:
        result["flexbox"] = True
    
    if 'display: grid' in html or 'display:-ms-grid' in html:
        result["grid"] = True
    
    return result

def check_offline_support(html: str, url: str) -> Dict:
    """Check for offline support"""
    result = {
        "manifest": False,
        "service_worker": False,
        "cache_manifest": False
    }
    
    # Service worker
    if 'serviceworker' in html.lower():
        result["service_worker"] = True
    
    # Cache manifest (older technique)
    if 'manifest.appcache' in html or 'manifest="*.appcache"' in html:
        result["cache_manifest"] = True
    
    return result

def check_performance_hints(html: str) -> List[str]:
    """Get performance hints"""
    hints = []
    
    # Large images
    img_count = len(re.findall(r'<img', html, re.IGNORECASE))
    if img_count > 20:
        hints.append(f"⚠️ High image count ({img_count}) - consider lazy loading")
    
    # Inline styles
    inline_styles = len(re.findall(r'style=["\']', html))
    if inline_styles > 10:
        hints.append(f"⚠️ Many inline styles ({inline_styles}) - consider external CSS")
    
    # Scripts at top
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
    above_fold = html.find('</head>')
    head_scripts = sum(1 for s in scripts if html.find(s) < above_fold)
    if head_scripts > 5:
        hints.append(f"⚠️ {head_scripts} scripts in head - consider defer/async")
    
    # No minification hints
    if '    ' in html and 'webpack' not in html.lower():
        hints.append("💡 Not minified - consider minification for production")
    
    return hints

def analyze_assets(html: str) -> Dict:
    """Analyze assets"""
    result = {
        "images": 0,
        "scripts": 0,
        "styles": 0,
        "fonts": 0,
        "total_size_estimate": 0
    }
    
    result["images"] = len(re.findall(r'<img', html, re.IGNORECASE))
    result["scripts"] = len(re.findall(r'<script[^>]*src=["\'][^"\']+["\']', html, re.IGNORECASE))
    result["styles"] = len(re.findall(r'<link[^>]*rel=["\']stylesheet["\']', html, re.IGNORECASE))
    result["fonts"] = len(re.findall(r'@font-face|fonts\.google', html, re.IGNORECASE))
    
    # Estimate size (rough)
    html_size = len(html)
    result["total_size_estimate"] = html_size + (result["images"] * 50000) + (result["scripts"] * 20000)
    
    return result

def check_framework(html: str) -> Optional[str]:
    """Detect JavaScript framework"""
    frameworks = {
        "React": ["react", "createelement", "__react"],
        "Vue": ["vue", "vuejs", "__vue"],
        "Angular": ["angular", "ng-version", "@angular"],
        "Next.js": ["next", "__next"],
        "Svelte": ["svelte", "_svelte"],
        "jQuery": ["jquery", "$().jquery"],
        "Bootstrap": ["bootstrap"],
        "Tailwind": ["tailwind"],
        "WordPress": ["wp-content", "wordpress"],
    }
    
    html_lower = html.lower()
    for framework, patterns in frameworks.items():
        for pattern in patterns:
            if pattern in html_lower:
                return framework
    
    return None

def run(args):
    """Run the inspect command"""
    
    if not args.url:
        print_error("URL required")
        print_info("Usage: anvil inspect https://example.com")
        return
    
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║         ANVIL Inspect                ║")
    print("╚══════════════════════════════════════════╝{Colors.END}")
    print()
    print(f"{Colors.CYAN}Inspecting: {args.url}{Colors.END}\n")
    
    # Fetch the page
    print_info("Fetching page...")
    html = fetch_url(args.url)
    
    if not html:
        print_error("Failed to fetch page")
        return
    
    print_success("Page fetched")
    print()
    
    # Analyze
    print_section("📱 PWA Status")
    
    pwa = check_pwa(html)
    if pwa["detected"]:
        print_success("PWA detected!")
        if pwa["manifest"]:
            print_success("  • Web App Manifest found")
        if pwa["service_worker"]:
            print_success("  • Service Worker detected")
    else:
        print_warning("Not a PWA")
        print_info("  Consider adding manifest and service worker for better mobile experience")
    
    print_section("🎨 Responsive Design")
    
    responsive = check_responsive(html)
    if responsive["viewport"]:
        print_success("Viewport meta tag found")
    else:
        print_warning("No viewport meta tag")
        print_info("  Add <meta name='viewport'> for mobile support")
    
    print(f"  • Media queries: {responsive['media_queries']}")
    print(f"  • Flexbox: {'Yes' if responsive['flexbox'] else 'No'}")
    print(f"  • CSS Grid: {'Yes' if responsive['grid'] else 'No'}")
    
    print_section("📦 Assets")
    
    assets = analyze_assets(html)
    print(f"  • Images: {assets['images']}")
    print(f"  • Scripts: {assets['scripts']}")
    print(f"  • Stylesheets: {assets['styles']}")
    print(f"  • Font references: {assets['fonts']}")
    
    estimated_mb = assets["total_size_estimate"] / (1024 * 1024)
    print(f"  • Estimated size: {estimated_mb:.1f} MB")
    
    if assets['images'] > 20:
        print_warning("High image count - consider optimization")
    
    print_section("⚡ Performance Hints")
    
    hints = check_performance_hints(html)
    if hints:
        for hint in hints:
            print(hint)
    else:
        print_success("No obvious performance issues")
    
    print_section("🔧 Framework Detection")
    
    framework = check_framework(html)
    if framework:
        print_success(f"Detected: {framework}")
    else:
        print_info("No common framework detected (vanilla JS)")
    
    print_section("🌐 Offline Support")
    
    offline = check_offline_support(html, args.url)
    if offline["service_worker"]:
        print_success("Service Worker detected")
    else:
        print_warning("No offline support")
        print_info("  Add service worker for offline capability")
    
    print_section("📋 Recommendations")
    
    recommendations = []
    
    if not pwa["detected"]:
        recommendations.append("Add web app manifest for installable experience")
    
    if not responsive["viewport"]:
        recommendations.append("Add viewport meta tag for proper mobile rendering")
    
    if not offline["service_worker"]:
        recommendations.append("Consider PWA for offline support")
    
    if assets['images'] > 15:
        recommendations.append("Implement lazy loading for images")
    
    if framework == "jQuery":
        recommendations.append("Modernize from jQuery to vanilla JS (optional)")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    if not recommendations:
        print_success("Site is well optimized for APK conversion!")
    
    print()
    print_info(f"Analysis complete for: {args.url}")
    print()

def add_parser(subparsers):
    """Add inspect command parser"""
    parser = subparsers.add_parser(
        "inspect",
        help="Analyze website for APK conversion",
        description="Inspect a website and get detailed analysis for APK conversion"
    )
    parser.add_argument("url", nargs="?", help="URL to inspect")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    return parser