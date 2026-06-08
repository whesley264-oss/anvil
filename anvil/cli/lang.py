"""
ANVIL lang - Change language command
"""

import os
import argparse
from pathlib import Path

from anvil.utils.i18n import i18n, LANGUAGES, _

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

def list_languages():
    """List all available languages"""
    print(f"\n{Colors.BOLD}Available Languages:{Colors.END}\n")
    
    current = i18n.get_language()
    
    for code, info in LANGUAGES.items():
        marker = f"{Colors.GREEN}[Current]{Colors.END}" if code == current else ""
        print(f"  {Colors.CYAN}{code.upper()}{Colors.END} - {info['native']} ({info['name']}) {marker}")
    
    print()

def show_current_language():
    """Show current language"""
    current = i18n.get_language()
    info = LANGUAGES.get(current, LANGUAGES["en"])
    
    print(f"\n{Colors.BOLD}Current Language:{Colors.END}")
    print(f"  {Colors.CYAN}{current.upper()}{Colors.END} - {info['native']} ({info['name']})")
    print()

def set_language_interactive():
    """Interactive language selection"""
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════╗")
    print("║         Change Language / Mudar Idioma        ║")
    print("╚══════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"{Colors.BOLD}Select language / Selecione o idioma:{Colors.END}\n")
    
    lang_list = list(LANGUAGES.items())
    
    for i, (code, info) in enumerate(lang_list, 1):
        print(f"  [{i}] {info['native']} - {info['name']} ({code})")
    
    print(f"  [0] Cancel")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Choice / Escolha [1-{len(lang_list)}]: {Colors.END}").strip()
        
        if choice == '0':
            print_info("Cancelled / Cancelado")
            return False
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(lang_list):
                code, info = lang_list[idx]
                
                if i18n.set_language(code):
                    print_success(f"Language changed to: {info['native']} ({info['name']})")
                    print_info(f"\n{Colors.YELLOW}Restart ANVIL to apply changes / Reinicie o ANVIL para aplicar as mudanças{Colors.END}")
                    return True
                else:
                    print_error("Failed to change language")
                    return False
            else:
                print_error(f"Please enter a number between 1 and {len(lang_list)}")
        except ValueError:
            print_error("Please enter a valid number")

def run(args):
    """Run the lang command"""
    
    # Show current language if no args
    if args.list:
        list_languages()
        return
    
    if args.show:
        show_current_language()
        return
    
    # Set specific language
    if args.set:
        code = args.set.lower()
        if code in LANGUAGES:
            if i18n.set_language(code):
                info = LANGUAGES[code]
                print_success(f"Language changed to: {info['native']} ({info['name']})")
                print_info(f"\nRestart ANVIL to apply changes")
            else:
                print_error("Failed to change language")
        else:
            print_error(f"Unknown language: {code}")
            print_info("Available: en, pt, es, zh")
        return
    
    # Interactive selection
    set_language_interactive()

def add_parser(subparsers):
    """Add lang command parser"""
    parser = subparsers.add_parser(
        "lang",
        help="Change language",
        description="Change ANVIL interface language (English, Portuguese, Spanish, Mandarin)"
    )
    parser.add_argument("--list", action="store_true", help="List available languages")
    parser.add_argument("--show", action="store_true", help="Show current language")
    parser.add_argument("--set", metavar="LANG", help="Set language (en, pt, es, zh)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive selection")
    
    return parser