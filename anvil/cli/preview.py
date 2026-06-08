"""
ANVIL preview - Test app in browser/emulator
"""

import os
import webbrowser
import http.server
import socketserver
import threading
import argparse
from pathlib import Path
import io

class Colors:
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that suppresses logs"""
    def log_message(self, format, *args):
        pass  # Suppress request logs

def start_server(port: int, directory: Path):
    """Start a simple HTTP server"""
    os.chdir(str(directory))
    with socketserver.TCPServer(("", port), QuietHandler) as httpd:
        httpd.serve_forever()

def open_browser_preview():
    """Open browser preview with live reload"""
    print_info("Starting HTTP server...")
    
    # Check for index.html
    possible_paths = [
        Path("android/app/src/main/assets/index.html"),
        Path("android/app/src/main/assets/"),
        Path("src/index.html"),
        Path("."),
    ]
    
    preview_dir = None
    for path in possible_paths:
        if path.exists():
            if path.is_file():
                preview_dir = path.parent
            else:
                preview_dir = path
            break
    
    if not preview_dir:
        print("No web content found for preview.")
        return None
    
    # Start server
    port = 8080
    server_thread = threading.Thread(target=start_server, args=(port, preview_dir), daemon=True)
    server_thread.start()
    
    url = f"http://localhost:{port}"
    
    print_info(f"Server running at {url}")
    print_info("Opening browser...")
    
    webbrowser.open(url)
    
    return url

def generate_qr_code(url: str):
    """Generate QR code for mobile testing"""
    try:
        import qrcode
    except ImportError:
        print("qrcode library not installed. Install with: pip install qrcode")
        return
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code
    qr_path = Path("dist/qr-code.png")
    qr_path.parent.mkdir(exist_ok=True)
    img.save(qr_path)
    
    print(f"\nQR Code saved to: {qr_path}")
    print("Scan with your phone to test on mobile.")

def check_emulator():
    """Check for running emulators"""
    import subprocess
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True
        )
        
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip() and '\t' in line:
                status = line.split('\t')[1].strip()
                if status == 'device':
                    devices.append(line.split('\t')[0])
        
        return devices
        
    except FileNotFoundError:
        return []

def run(args):
    """Run the preview command"""
    
    print(f"{Colors.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║          ANVIL - Preview                   ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    print(f"{Colors.BOLD}Preview options:{Colors.END}")
    print("  [1] Browser preview")
    print("  [2] QR Code for mobile")
    print("  [3] List connected devices")
    
    choice = input("\nSelect option [1-3]: ").strip() or "1"
    
    if choice == "1":
        print_info("Starting browser preview...")
        url = open_browser_preview()
        if url:
            print(f"\n{Colors.BOLD}Preview URL:{Colors.END} {url}")
            print("Press Ctrl+C to stop server")
            
            # Keep server running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nServer stopped.")
    
    elif choice == "2":
        print_info("Generating QR code...")
        url = open_browser_preview()
        if url:
            generate_qr_code(url)
    
    elif choice == "3":
        devices = check_emulator()
        if devices:
            print(f"{Colors.BOLD}Connected devices:{Colors.END}")
            for i, device in enumerate(devices, 1):
                print(f"  [{i}] {device}")
        else:
            print("No devices found.")
            print_info("Connect a device via USB or start an emulator")

def add_parser(subparsers):
    """Add preview command parser"""
    parser = subparsers.add_parser(
        "preview",
        help="Test app in browser or emulator",
        description="Preview web app in browser, generate QR code, or list devices"
    )
    parser.add_argument("--browser", action="store_true", help="Open in browser")
    parser.add_argument("--qr", action="store_true", help="Generate QR code")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    
    return parser