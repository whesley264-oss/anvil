"""
ANVIL Mobile Detection - Detect platform and optimize behavior
"""

import os
import sys
import platform
from pathlib import Path

def is_termux():
    """Check if running in Termux"""
    return os.environ.get('TERMUX') == 'true' or os.environ.get('TERMUX_APP') == 'true'

def is_android():
    """Check if running on Android device"""
    if os.environ.get('ANDROID_ROOT'):
        return True
    
    try:
        with open('/proc/version', 'r') as f:
            content = f.read().lower()
            return 'android' in content
    except:
        pass
    
    return False

def is_mobile():
    """Check if running on mobile device (Termux, Android, etc.)"""
    return is_termux() or is_android()

def get_platform_info():
    """Get detailed platform information"""
    info = {
        'platform': platform.system(),
        'release': platform.release(),
        'machine': platform.machine(),
        'is_mobile': is_mobile(),
        'is_termux': is_termux(),
        'is_android': is_android(),
        'termux_prefix': os.environ.get('PREFIX', ''),
        'android_home': os.environ.get('ANDROID_HOME', ''),
        'java_home': os.environ.get('JAVA_HOME', ''),
    }
    
    # Check available RAM
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    info['total_ram_mb'] = int(line.split()[1]) // 1024
                    break
    except:
        info['total_ram_mb'] = None
    
    return info

def get_mobile_optimizations():
    """Get optimized settings for mobile devices"""
    if not is_mobile():
        return None
    
    return {
        # Gradle optimizations
        'gradle': {
            'heap_size': '1536m',  # Reduced from 2048m
            'parallel': False,
            'daemon': True,
            'caching': True,
        },
        
        # Build optimizations
        'build': {
            'incremental': True,
            'offline': False,
            'max_workers': 1,  # Single thread for mobile
        },
        
        # APK optimizations
        'apk': {
            'minify': True,
            'split_abis': False,  # Single APK for all architectures
            'resource_optimization': True,
        },
        
        # Display optimizations
        'display': {
            'color': False,  # Disable colors if terminal doesn't support
            'animations': False,
            'compact': True,  # Shorter output
        }
    }

def get_recommended_packages():
    """Get recommended packages for current platform"""
    packages = {
        'termux': [
            'python',
            'git',
            'openjdk-17',
            'android-sdk',
            'termux-api',
        ],
        'android': [
            'termux-api',
        ]
    }
    
    if is_termux():
        return packages['termux']
    elif is_android():
        return packages['android']
    
    return []

def get_sdk_path():
    """Find Android SDK path"""
    # Check common locations
    paths = [
        os.environ.get('ANDROID_HOME'),
        os.environ.get('ANDROID_SDK_ROOT'),
        os.environ.get('ANDROID_SDK'),
        
        # Termux default
        '/data/data/com.termux/files/usr/lib/android-sdk',
        os.path.join(os.environ.get('PREFIX', ''), 'lib/android-sdk'),
        
        # Linux/Android common
        os.path.expanduser('~/android-sdk'),
        os.path.expanduser('~/Android/Sdk'),
        
        # Standard
        '/opt/android-sdk',
        '/usr/local/android-sdk',
    ]
    
    for path in paths:
        if path and Path(path).exists():
            return path
    
    return None

def get_java_path():
    """Find Java installation path"""
    paths = [
        os.environ.get('JAVA_HOME'),
        
        # Termux
        os.path.join(os.environ.get('PREFIX', ''), 'lib/jvm/java-17-openjdk'),
        
        # Common
        '/usr/lib/jvm/java-17-openjdk',
        '/usr/lib/jvm/java-11-openjdk',
        '/opt/java/openjdk',
        os.path.expanduser('~/.jdk17'),
    ]
    
    for path in paths:
        if path and Path(path).exists():
            return path
    
    return None

def format_mobile_output(text: str, compact: bool = True) -> str:
    """Format output for mobile display"""
    if not is_mobile():
        return text
    
    lines = text.split('\n')
    if compact:
        # Remove empty lines and reduce spacing
        lines = [line for line in lines if line.strip()]
    
    return '\n'.join(lines)

# Banner for mobile
MOBILE_BANNER = """
╔═══════════════════╗
║   ANVIL (Mobile)   ║
╚═══════════════════╝
"""

def get_banner():
    """Get appropriate banner for platform"""
    if is_mobile():
        return MOBILE_BANNER
    return """
╔══════════════════════════════════════════╗
║               ANVIL - Build APK            ║
╚══════════════════════════════════════════╝
"""