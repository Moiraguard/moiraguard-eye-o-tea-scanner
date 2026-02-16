#!/usr/bin/env python3
"""
MOIRAGUARD Setup Verification Script
Checks if all dependencies and files are properly configured
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"[CHECK] Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("  ✓ Python version is compatible (3.7+)")
        return True
    else:
        print("  ✗ Python version too old. Need 3.7+")
        return False

def check_shodan_module():
    """Check if Shodan is installed"""
    try:
        import shodan
        print(f"[CHECK] Shodan Module")
        print(f"  ✓ Shodan library installed (version: {shodan.__version__ if hasattr(shodan, '__version__') else 'unknown'})")
        return True
    except ImportError:
        print("[CHECK] Shodan Module")
        print("  ✗ Shodan not installed. Run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if API key file exists"""
    key_file = Path("shodan_api.key")
    print("[CHECK] API Key File")
    if key_file.exists():
        with open(key_file, 'r') as f:
            key = f.read().strip()
        if len(key) > 0:
            print(f"  ✓ API key file exists ({len(key)} characters)")
            return True
        else:
            print("  ✗ API key file is empty")
            return False
    else:
        print("  ✗ API key file not found (shodan_api.key)")
        return False

def check_config_files():
    """Check if configuration files exist"""
    files = {
        "countries.json": "Country configuration",
        "targets.json": "Target profiles",
        "requirements.txt": "Dependencies list",
        "README.md": "Documentation"
    }

    all_exist = True
    print("[CHECK] Configuration Files")
    for filename, description in files.items():
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {filename} ({size} bytes) - {description}")
        else:
            print(f"  ✗ {filename} missing - {description}")
            all_exist = False

    return all_exist

def check_main_script():
    """Check if main scanner exists"""
    script = Path("moiraguard_iot_scanner.py")
    print("[CHECK] Main Scanner Script")
    if script.exists():
        size = script.stat().st_size
        with open(script, 'r') as f:
            lines = len(f.readlines())
        print(f"  ✓ moiraguard_iot_scanner.py ({size} bytes, {lines} lines)")
        return True
    else:
        print("  ✗ moiraguard_iot_scanner.py not found")
        return False

def test_api_connection():
    """Test Shodan API connection"""
    try:
        import shodan
        key_file = Path("shodan_api.key")
        if not key_file.exists():
            print("[CHECK] API Connection")
            print("  ⊘ Skipped - no API key file")
            return None

        with open(key_file, 'r') as f:
            api_key = f.read().strip()

        print("[CHECK] API Connection")
        print("  ... Testing connection to Shodan API ...")
        api = shodan.Shodan(api_key)
        info = api.info()

        print(f"  ✓ API connection successful")
        print(f"  ✓ Query credits: {info.get('query_credits', 'N/A')}")
        print(f"  ✓ Scan credits: {info.get('scan_credits', 'N/A')}")
        return True
    except shodan.APIError as e:
        print(f"  ✗ API Error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("MOIRAGUARD Setup Verification")
    print("=" * 60)
    print()

    results = []
    results.append(("Python Version", check_python_version()))
    results.append(("Shodan Module", check_shodan_module()))
    results.append(("API Key", check_api_key()))
    results.append(("Config Files", check_config_files()))
    results.append(("Main Script", check_main_script()))

    # Only test API if previous checks passed
    if all(r[1] for r in results):
        api_result = test_api_connection()
        if api_result is not None:
            results.append(("API Connection", api_result))

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    total = len(results)

    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status:10s} {check_name}")

    print()
    print(f"Results: {passed}/{total} checks passed")

    if failed == 0:
        print("\n✓ All checks passed! You're ready to run MOIRAGUARD.")
        print("\nRun the scanner with:")
        print("  python3 moiraguard_iot_scanner.py")
        return 0
    else:
        print(f"\n✗ {failed} check(s) failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip3 install -r requirements.txt")
        print("  - Create API key file: echo 'YOUR_KEY' > shodan_api.key")
        return 1

if __name__ == "__main__":
    sys.exit(main())
