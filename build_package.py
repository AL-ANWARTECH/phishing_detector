#!/usr/bin/env python3
"""
Script to build the phishing detector package
"""
import os
import subprocess
import sys
from pathlib import Path

def build_package():
    """Build the package using setup.py"""
    print("Building Phishing Detection System Package...")
    
    # Check if setup.py exists
    if not Path("setup.py").exists():
        print("Error: setup.py not found in current directory")
        return False
    
    # Build the package
    try:
        print("Running: python setup.py sdist bdist_wheel")
        result = subprocess.run([
            sys.executable, "setup.py", "sdist", "bdist_wheel"
        ], check=True, capture_output=True, text=True)
        
        print("✓ Package built successfully!")
        print(result.stdout)
        
        # Show built files
        dist_path = Path("dist")
        if dist_path.exists():
            print("\nBuilt files:")
            for file_path in dist_path.iterdir():
                print(f"  - {file_path}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error building package: {e}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def install_package_locally():
    """Install the package locally in development mode"""
    print("Installing package in development mode...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)
        
        print("✓ Package installed successfully!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing package: {e}")
        print(f"Output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False

def main():
    """Main function"""
    print("Phishing Detection System - Package Builder")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Build the package
    if build_package():
        print("\nPackage build completed successfully!")
        
        # Ask if user wants to install locally
        response = input("\nInstall package locally in development mode? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            install_package_locally()
    else:
        print("\nPackage build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()