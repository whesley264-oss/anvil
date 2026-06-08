"""
ANVIL logs - View and manage build logs
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

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
    BOLD = '\033[1m'
    END = '\033[0m'
    GRAY = '\033[90m'

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ{Colors.END} {message}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def get_log_dir() -> Path:
    """Get the logs directory"""
    log_dir = Path.home() / ".anvil" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def list_logs():
    """List all log files"""
    log_dir = get_log_dir()
    
    if not log_dir.exists() or not list(log_dir.glob("*.log")):
        print_warning("No logs found")
        return []
    
    logs = sorted(log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"\n{Colors.BOLD}Build Logs:{Colors.END}\n")
    
    for log in logs:
        # Parse filename: build_2024-01-15_14-30-45.log
        name = log.stem
        size = log.stat().st_size
        mtime = datetime.fromtimestamp(log.stat().st_mtime)
        
        # Format size
        if size < 1024:
            size_str = f"{size}B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f}KB"
        else:
            size_str = f"{size/(1024*1024):.1f}MB"
        
        # Format time
        time_str = mtime.strftime("%Y-%m-%d %H:%M")
        
        # Log type
        if "build" in name:
            icon = "🔨"
            color = Colors.CYAN
        elif "error" in name:
            icon = "❌"
            color = Colors.RED
        elif "deploy" in name:
            icon = "📱"
            color = Colors.GREEN
        else:
            icon = "📋"
            color = Colors.GRAY
        
        print(f"  {icon} {color}{name}{Colors.END}")
        print(f"     {Colors.GRAY}{time_str} • {size_str}{Colors.END}")
        print()
    
    return logs

def show_log(log_name: str, lines: int = 50, error_only: bool = False):
    """Show contents of a log file"""
    log_dir = get_log_dir()
    log_path = log_dir / f"{log_name}.log"
    
    # Also try without extension
    if not log_path.exists():
        log_path = log_dir / log_name
        if not log_path.exists() and not log_name.endswith(".log"):
            log_path = log_dir / f"{log_name}.log"
    
    if not log_path.exists():
        print_error(f"Log not found: {log_name}")
        print_info("Available logs:")
        list_logs()
        return
    
    print(f"\n{Colors.BOLD}Log: {log_path.name}{Colors.END}\n")
    
    # Read log
    try:
        with open(log_path, 'r') as f:
            content = f.read()
        
        if error_only:
            lines_list = content.split('\n')
            error_lines = [l for l in lines_list if 'error' in l.lower() or 'fail' in l.lower() or '✗' in l]
            content = '\n'.join(error_lines[-lines:])
        else:
            content_lines = content.split('\n')
            content = '\n'.join(content_lines[-lines:])
        
        print(f"{Colors.GRAY}{content}{Colors.END}")
        
    except Exception as e:
        print_error(f"Error reading log: {e}")

def tail_log(log_name: str, follow: bool = False):
    """Tail a log file (like tail -f)"""
    import time
    
    log_dir = get_log_dir()
    log_path = log_dir / f"{log_name}.log"
    
    if not log_path.exists():
        print_error(f"Log not found: {log_name}")
        return
    
    print(f"{Colors.BOLD}Tailing: {log_path.name}{Colors.END}")
    print(f"{Colors.GRAY}(Press Ctrl+C to stop){Colors.END}\n")
    
    # Get initial position
    with open(log_path, 'r') as f:
        f.seek(0, 2)  # Seek to end
        position = f.tell()
    
    try:
        while True:
            with open(log_path, 'r') as f:
                f.seek(position)
                new_lines = f.readlines()
                
                for line in new_lines:
                    print(f"{Colors.GRAY}{line.rstrip()}{Colors.END}")
                
                if new_lines:
                    position = f.tell()
            
            if not follow:
                break
            
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Stopped tailing{Colors.END}")

def clear_logs():
    """Clear all logs"""
    log_dir = get_log_dir()
    
    if not log_dir.exists() or not list(log_dir.glob("*.log")):
        print_warning("No logs to clear")
        return
    
    count = 0
    for log in log_dir.glob("*.log"):
        log.unlink()
        count += 1
    
    print_success(f"Cleared {count} log file(s)")

def run(args):
    """Run the logs command"""
    
    if args.list:
        list_logs()
    elif args.clear:
        clear_logs()
    elif args.tail and args.name:
        tail_log(args.name, follow=args.follow)
    elif args.name:
        show_log(args.name, lines=args.lines, error_only=args.errors)
    else:
        # Default: list logs
        list_logs()

def add_parser(subparsers):
    """Add logs command parser"""
    parser = subparsers.add_parser(
        "logs",
        help="View and manage build logs",
        description="List, view, tail, or clear build logs"
    )
    parser.add_argument("--list", "-l", action="store_true", help="List all logs")
    parser.add_argument("--clear", "-c", action="store_true", help="Clear all logs")
    parser.add_argument("--tail", "-t", action="store_true", help="Tail log (like tail -f)")
    parser.add_argument("--follow", "-f", action="store_true", help="Follow log updates")
    parser.add_argument("--errors", "-e", action="store_true", help="Show only errors")
    parser.add_argument("--lines", "-n", type=int, default=50, help="Number of lines to show")
    parser.add_argument("name", nargs="?", help="Log name to view")
    
    return parser