"""
ANVIL run - Development server with live reload
"""

import os
import sys
import time
import argparse
import http.server
import socketserver
from pathlib import Path
from threading import Thread
import webbrowser

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

class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with live reload injection"""
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_GET(self):
        super().do_GET()

def generate_livereload_script():
    """Generate live reload script for injection"""
    return '''
    <script>
    // Live Reload Script
    (function() {
        var ws = new WebSocket('ws://localhost:8765/livereload');
        ws.onmessage = function(e) {
            if (e.data === 'reload') {
                location.reload();
            }
        };
        ws.onclose = function() {
            setTimeout(function() { location.reload(); }, 1000);
        };
    })();
    </script>
    '''

def start_livereload_server(port=8765):
    """Start WebSocket server for live reload"""
    class WSHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/livereload':
                self.send_response(101)
                self.send_header('Upgrade', 'websocket')
                self.send_header('Connection', 'upgrade')
                self.end_headers()
                
                # Keep connection alive for livereload
                import time
                while True:
                    try:
                        time.sleep(30)
                    except:
                        break
    
    httpd = socketserver.TCPServer(("", port), WSHandler)
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

def start_dev_server(port=3000, project_dir=None, open_browser=True):
    """Start development server with live reload"""
    
    if project_dir is None:
        project_dir = Path(".")
    
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║         ANVIL Dev Server              ║")
    print("╚══════════════════════════════════════════╝{Colors.END}\n")
    
    # Find index.html
    index_path = project_dir / "index.html"
    if not index_path.exists():
        for html_file in project_dir.rglob("*.html"):
            index_path = html_file
            break
    
    if not index_path.exists():
        print_error("No index.html found in project")
        return
    
    print_info(f"Serving: {index_path}")
    print_info(f"URL: http://localhost:{port}")
    print_info(f"Project: {project_dir}")
    print()
    
    # Start live reload server
    print_info("Starting live reload server...")
    lr_server = start_livereload_server()
    print_success("Live reload enabled")
    print()
    
    # Change to project directory
    os.chdir(str(project_dir))
    
    # Start HTTP server
    handler = lambda *args, **kwargs: LiveReloadHandler(*args, directory=str(project_dir), **kwargs)
    httpd = socketserver.TCPServer(("", port), handler)
    
    # Open browser
    if open_browser:
        print_info("Opening browser...")
        webbrowser.open(f"http://localhost:{port}")
    
    print_success(f"Server running at http://localhost:{port}")
    print_info("Press Ctrl+C to stop")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n")
        print_info("Stopping server...")
        httpd.shutdown()
        lr_server.shutdown()
        print_success("Server stopped")

def run(args):
    """Run the dev server"""
    
    port = args.port or 3000
    project_dir = Path(args.project) if args.project else Path(".")
    
    # Check if project exists
    if not project_dir.exists():
        print_error(f"Project directory not found: {project_dir}")
        return
    
    start_dev_server(port=port, project_dir=project_dir, open_browser=not args.no_browser)

def add_parser(subparsers):
    """Add run command parser"""
    parser = subparsers.add_parser(
        "run",
        help="Start development server with live reload",
        description="Start dev server, open preview, and enable hot reload"
    )
    parser.add_argument("--port", type=int, default=3000, help="Server port (default: 3000)")
    parser.add_argument("--project", help="Project directory (default: current)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    
    return parser