"""
ANVIL utils - Generator and helpers
"""

from .generator import generate_android_project, build_apk, ensure_dir, generate_gradle_files, generate_manifest
from .mobile import is_mobile, is_termux, is_android, get_platform_info, get_mobile_optimizations
from .i18n import i18n, LANGUAGES, _

__all__ = [
    "generate_android_project", "build_apk", "ensure_dir", "generate_gradle_files", "generate_manifest",
    "is_mobile", "is_termux", "is_android", "get_platform_info", "get_mobile_optimizations",
    "i18n", "LANGUAGES", "_"
]
