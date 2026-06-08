#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANVIL - Web to APK CLI
Transform websites into Android APKs without Android Studio hell.
"""

import sys
import os
from pathlib import Path

# Add ANVIL_HOME to Python path for module imports
_anvil_home = os.environ.get('ANVIL_HOME', str(Path(__file__).parent))
if _anvil_home not in sys.path:
    sys.path.insert(0, _anvil_home)

# Version
__version__ = "0.3.0"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="anvil",
        description="ANVIL - Transform websites into Android APKs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  anvil init                    Start interactive wizard
  anvil build                   Build APK
  anvil build apk               Build APK (explicit)
  anvil build aab               Build AAB bundle
  anvil deploy --device=usb     Build and install
  anvil doctor                  Check system requirements
  anvil inspect https://site.com  Analyze website
  anvil run                     Start dev server with live reload
  anvil logs                    View build logs
  anvil clean                   Remove build artifacts

Run 'anvil <command> --help' for more information on a command.
        """
    )
    
    parser.add_argument("--version", action="version", version=f"anvil {__version__}")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Import and add all command parsers
    from anvil.cli import (
        init, build, sign, doctor, preview, config, plugin, deploy, setup, 
        quick_build, lang, run, logs, clean, inspect, update, demo
    )
    
    init.add_parser(subparsers)
    build.add_parser(subparsers)
    sign.add_parser(subparsers)
    doctor.add_parser(subparsers)
    preview.add_parser(subparsers)
    config.add_parser(subparsers)
    plugin.add_parser(subparsers)
    deploy.add_parser(subparsers)
    setup.add_parser(subparsers)
    quick_build.add_parser(subparsers)
    lang.add_parser(subparsers)
    run.add_parser(subparsers)
    logs.add_parser(subparsers)
    clean.add_parser(subparsers)
    inspect.add_parser(subparsers)
    update.add_parser(subparsers)
    demo.add_parser(subparsers)
    
    from anvil.cli.banner import BANNER, BANNER_SMALL
    
    args = parser.parse_args()
    
    if not args.command:
        print(BANNER)
        print(BANNER_SMALL.format(version=__version__))
        print("\033[1mCommands:\033[0m")
        print("  init         Create new project from web app")
        print("  build        Compile APK (use 'build apk' or 'build release')")
        print("  build apk    Build debug APK")
        print("  build aab    Build App Bundle for Play Store")
        print("  sign         Sign APK or generate keystore")
        print("  deploy       Build and deploy to connected device via ADB")
        print("  doctor       Check system requirements")
        print("  preview      Test app in browser or emulator")
        print("  run          Start dev server with live reload")
        print("  inspect      Analyze website for APK conversion")
        print("  clean        Remove Gradle cache and build artifacts")
        print("  logs         View and manage build logs")
        print("  config       Manage project configuration")
        print("  plugin       Manage plugins")
        print("  setup        Setup ANVIL on different platforms")
        print("  lang         Change interface language (en, pt, es, zh)")
        print("  update       Update ANVIL to the latest version")
        print("  demo         Create a demo APK to test installation")
        print()
        print("\033[1mQuick Build:\033[0m")
        print("  quick-build   Build APK from GitHub, ZIP, or URL")
        print()
        print("Run '\033[94manvil <command> --help\033[0m' for more information.")
        print()
        sys.exit(1)
    
    # Route to command handler
    commands = {
        "init": init.run,
        "build": build.run,
        "sign": sign.run,
        "doctor": doctor.run,
        "preview": preview.run,
        "config": config.run,
        "plugin": plugin.run,
        "deploy": deploy.run,
        "setup": setup.run,
        "quick-build": quick_build.run,
        "lang": lang.run,
        "run": run.run,
        "logs": logs.run,
        "clean": clean.run,
        "inspect": inspect.run,
        "update": update.run,
        "demo": demo.run,
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()