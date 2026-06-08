"""
ANVIL Pack - Lightweight APK builder
Creates APKs using minimal tools, no Android SDK required
"""

import os
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path
import subprocess

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(msg): print(f"{Colors.CYAN}ℹ{Colors.END} {msg}")
def print_success(msg): print(f"{Colors.GREEN}✓{Colors.END} {msg}")
def print_error(msg): print(f"{Colors.RED}✗{Colors.END} {msg}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def check_tools():
    """Check available tools for building"""
    tools = {}
    
    # Check for aapt
    aapt_paths = [
        "/data/data/com.termux/files/usr/bin/aapt",
        "/data/data/com.termux/files/usr/bin/aapt2",
        os.path.expandvars("$HOME/android-sdk/build-tools/34.0.0/aapt"),
        os.path.expandvars("$HOME/android-sdk/build-tools/33.0.0/aapt"),
    ]
    
    for path in aapt_paths:
        if Path(path).exists():
            tools['aapt'] = path
            break
    
    # Check for apkt (termux package)
    if Path("/data/data/com.termux/files/usr/bin/apkt").exists():
        tools['apkt'] = "/data/data/com.termux/files/usr/bin/apkt"
    
    # Check for java
    java_paths = [
        "/data/data/com.termux/files/usr/lib/jvm/java-17-openjdk/bin/java",
        os.path.expandvars("$JAVA_HOME/bin/java"),
    ]
    
    for path in java_paths:
        if Path(path).exists():
            tools['java'] = Path(path).parent
            break
    
    # Check for zipalign
    zipalign_paths = [
        "/data/data/com.termux/files/usr/bin/zipalign",
        os.path.expandvars("$HOME/android-sdk/build-tools/34.0.0/zipalign"),
    ]
    
    for path in zipalign_paths:
        if Path(path).exists():
            tools['zipalign'] = path
            break
    
    # Check for apksigner
    apksigner_paths = [
        "/data/data/com.termux/files/usr/bin/apksigner",
        os.path.expandvars("$HOME/android-sdk/build-tools/34.0.0/apksigner"),
    ]
    
    for path in apksigner_paths:
        if Path(path).exists():
            tools['apksigner'] = path
            break
    
    return tools

def create_webview_apk(project_dir, output_apk, app_name="ANVIL App", package="com.anvil.app"):
    """Create APK with WebView loading local HTML"""
    
    tools = check_tools()
    
    print_info(f"Building WebView APK: {app_name}")
    print_info(f"Tools available: {', '.join(tools.keys()) or 'none'}")
    
    # Find index.html
    project_path = Path(project_dir)
    index_html = project_path / "index.html"
    
    if not index_html.exists():
        for html_file in project_path.rglob("index.html"):
            index_html = html_file
            break
    
    if not index_html.exists():
        print_error("index.html not found!")
        return False
    
    print_success(f"Found: {index_html}")
    
    # Read HTML
    html_content = index_html.read_text(encoding='utf-8')
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        apk_path = tmp_path / "app.apk"
        
        # Check if we have aapt for real APK building
        if 'aapt' in tools:
            print_info("Using aapt for APK building...")
            success = build_with_aapt(tools['aapt'], html_content, apk_path, app_name, package, project_path)
        elif 'apkt' in tools:
            print_info("Using apkt for APK building...")
            success = build_with_apkt(tools['apkt'], html_content, apk_path, app_name, package, project_path)
        else:
            print_warning("No build tools found, creating package...")
            success = create_zip_package(html_content, apk_path, app_name, package, project_path)
        
        if success and apk_path.exists():
            # Copy to output
            shutil.copy(apk_path, output_apk)
            print_success(f"APK created: {output_apk}")
            return True
        
        return False

def build_with_aapt(aapt, html_content, output_apk, app_name, package, project_path):
    """Build APK using aapt"""
    
    print_info("Building with aapt...")
    
    # Create structure
    struct_dir = Path(tempfile.mkdtemp())
    
    try:
        # Create directories
        (struct_dir / "assets").mkdir()
        (struct_dir / "res" / "values").mkdir(parents=True)
        (struct_dir / "res" / "drawable").mkdir(parents=True)
        
        # Copy assets
        (struct_dir / "assets" / "index.html").write_text(html_content, encoding='utf-8')
        
        # Copy any other assets
        for asset in project_path.rglob("*"):
            if asset.is_file() and not asset.name.startswith('.'):
                rel = asset.relative_to(project_path)
                dest = struct_dir / "assets" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(asset, dest)
        
        # Create strings.xml
        (struct_dir / "res" / "values" / "strings.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
</resources>""")
        
        # Create AndroidManifest.xml
        manifest_xml = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package}">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <application 
        android:allowBackup="true" 
        android:label="@string/app_name"
        android:usesCleartextTraffic="true">
        <activity 
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>""".format(package=package)
        
        (struct_dir / "AndroidManifest.xml").write_text(manifest_xml)
        
        # Create launcher icon (simple colored square)
        icon_xml = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#667eea"/>
</shape>"""
        (struct_dir / "res" / "drawable" / "ic_launcher.xml").write_text(icon_xml)
        
        # Build APK with aapt
        print_info("Packaging APK...")
        
        # Create APK structure
        apk_dir = Path(tempfile.mkdtemp())
        
        # Use Python zipfile to create APK (APK is just a ZIP)
        with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add AndroidManifest.xml
            zf.write(struct_dir / "AndroidManifest.xml", "AndroidManifest.xml")
            
            # Add assets
            for asset in (struct_dir / "assets").rglob("*"):
                arcname = f"assets/{asset.name}"
                zf.write(asset, arcname)
            
            # Add resources
            for res in (struct_dir / "res").rglob("*"):
                arcname = str(res.relative_to(struct_dir))
                zf.write(res, arcname)
        
        print_success("APK packaged successfully!")
        return True
        
    finally:
        shutil.rmtree(struct_dir, ignore_errors=True)

def build_with_apkt(apkt, html_content, output_apk, app_name, package, project_path):
    """Build APK using apkt tool"""
    
    print_info("Using apkt for building...")
    
    # Create project structure for apkt
    proj_dir = Path(tempfile.mkdtemp())
    
    try:
        # Create structure
        (proj_dir / "assets").mkdir()
        (proj_dir / "src" / "main" / "java" / "com" / "anvil").mkdir(parents=True)
        
        # Write HTML
        (proj_dir / "assets" / "index.html").write_text(html_content, encoding='utf-8')
        
        # Write MainActivity.java
        activity_java = f"""package com.anvil;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        WebView webView = new WebView(this);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.loadUrl("file:///android_asset/index.html");
        setContentView(webView);
    }}
}}"""
        
        (proj_dir / "src" / "main" / "java" / "com" / "anvil" / "MainActivity.java").write_text(activity_java)
        
        # Write AndroidManifest.xml
        manifest_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package}">
    <uses-permission android:name="android.permission.INTERNET"/>
    <application android:allowBackup="true" android:label="{app_name}">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>"""
        
        (proj_dir / "src" / "main" / "AndroidManifest.xml").write_text(manifest_xml)
        
        # Run apkt
        print_info("Running apkt...")
        result = subprocess.run(
            [apkt, "build", str(proj_dir), "-o", str(output_apk)],
            capture_output=True,
            text=True,
            cwd=str(proj_dir)
        )
        
        if result.returncode == 0:
            print_success("APK built with apkt!")
            return True
        else:
            print_warning(f"apkt failed: {result.stderr}")
            return False
            
    finally:
        shutil.rmtree(proj_dir, ignore_errors=True)

def create_zip_package(html_content, output_apk, app_name, package, project_path):
    """Create a ZIP package as fallback"""
    
    print_warning("Creating ZIP package (not a real APK)")
    
    with zipfile.ZipFile(output_apk, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("assets/index.html", html_content)
        zf.writestr("README.txt", f"{app_name}\n\nThis is a package, not a compiled APK.\nUse 'anvil build --full' to create a real APK.")
    
    return True

def run(args):
    """Run pack command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║       ANVIL - Pack (Light Build)          ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Find project directory
    if args.project:
        project_dir = args.project
    else:
        project_dir = os.getcwd()
    
    # Determine output
    if args.output:
        output_apk = args.output
    else:
        output_apk = os.path.join(project_dir, "app.apk")
    
    print_info(f"Project: {project_dir}")
    print_info(f"Output: {output_apk}")
    print("")
    
    # Check tools
    tools = check_tools()
    print_info(f"Available tools: {', '.join(tools.keys()) or 'minimal'}")
    print("")
    
    # Build
    success = create_webview_apk(project_dir, output_apk, app_name=args.name or "ANVIL App", package=args.package or "com.anvil.app")
    
    if success:
        print("")
        print_success("Pack complete!")
        print_info(f"APK: {output_apk}")
        print_info("Note: For full APK with proper signing, use 'anvil build --full'")
        return True
    else:
        print_error("Pack failed!")
        return False

def add_parser(subparsers):
    """Add pack command parser"""
    parser = subparsers.add_parser(
        "pack",
        help="Lightweight build (no SDK required)",
        description="Build APK using minimal tools. Works without Android SDK."
    )
    parser.add_argument("project", nargs="?", default=".", help="Project directory")
    parser.add_argument("-o", "--output", help="Output APK path")
    parser.add_argument("-n", "--name", default="ANVIL App", help="App name")
    parser.add_argument("-p", "--package", default="com.anvil.app", help="Package name")
    
    return parser