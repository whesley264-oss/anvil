#!/usr/bin/env python3
"""
ANVIL Animation Demo - Test all animations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from anvil.cli.animations import SkeletonKingAnimation

def main():
    print("\033[1m╔══════════════════════════════════════════╗\033[0m")
    print("\033[1m║\033[0m         ANVIL Animation Demo          \033[1m║\033[0m")
    print("\033[1m╚══════════════════════════════════════════╝\033[0m")
    print()
    
    print("Testing Skeleton King Loading Animation...")
    print()
    
    # Run the animation
    anim = SkeletonKingAnimation("Forging your APK...")
    anim.animate(duration=2, loops=1)
    
    print("\033[92mAnimation complete!\033[0m")
    print()
    print("Press ENTER to see it again...")
    input()
    
    # Run again
    anim.animate(duration=2, loops=1)
    
    print()
    print("\033[1m✓ Demo complete!\033[0m")

if __name__ == "__main__":
    main()