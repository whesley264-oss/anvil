"""
ANVIL CLI Tests
Tests for ANVIL CLI functionality
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add anvil to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_banner_import():
    """Test that banner can be imported"""
    from anvil.cli.banner import BANNER, BANNER_SMALL
    assert BANNER is not None
    assert BANNER_SMALL is not None
    print("✓ Banner import test passed")

def test_config_creation():
    """Test creating a minimal config"""
    from anvil.cli.init import validate_package_id
    
    # Valid package IDs
    assert validate_package_id("com.example.app") == True
    assert validate_package_id("org.test.myapp") == True
    
    # Invalid package IDs
    assert validate_package_id("1invalid.app") == False
    assert validate_package_id("invalid") == False
    
    print("✓ Config validation test passed")

def test_generator_import():
    """Test that generator modules can be imported"""
    from anvil.utils.generator import (
        ensure_dir, 
        generate_gradle_files,
        generate_manifest
    )
    assert ensure_dir is not None
    assert generate_gradle_files is not None
    assert generate_manifest is not None
    print("✓ Generator import test passed")

def test_package_name_validation():
    """Test package name validation"""
    from anvil.cli.init import validate_package_id
    
    # Valid
    assert validate_package_id("com.test.app") == True
    assert validate_package_id("org.whesley.anvil") == True
    
    # Invalid - must start with letter
    assert validate_package_id("123.test") == False
    assert validate_package_id("test") == False
    
    print("✓ Package name validation test passed")

def test_gradle_files_generation():
    """Test that gradle files can be generated"""
    from anvil.utils.generator import generate_gradle_files
    import tempfile
    
    config = {
        "name": "TestApp",
        "package": "com.test.app",
        "version": "1.0.0"
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        android_dir = Path(tmpdir) / "android"
        android_dir.mkdir()
        
        # Create required directories
        (android_dir / "app" / "src" / "main" / "res" / "values").mkdir(parents=True, exist_ok=True)
        (android_dir / "gradle" / "wrapper").mkdir(parents=True, exist_ok=True)
        
        generate_gradle_files(android_dir, config)
        
        # Check files exist
        assert (android_dir / "settings.gradle.kts").exists()
        assert (android_dir / "build.gradle.kts").exists()
        
        print("✓ Gradle files generation test passed")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("ANVIL CLI Tests")
    print("="*50 + "\n")
    
    tests = [
        test_banner_import,
        test_config_creation,
        test_generator_import,
        test_package_name_validation,
        test_gradle_files_generation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)