#!/usr/bin/env python3
"""
Simple file processor with deprecated libraries for testing
"""

import os
import datetime
import importlib  # DEPRECATED: Removed in Python 3.12+
import platform
from distutils.util import strtobool
from distutils.util import strtobool
import distutils.util


def strtobool(input):
    try:
        return distutils.util.strtobool(input)
    except ValueError:
        return False  # DEPRECATED: Removed in Python 3.12+

def main():
    """Main function with deprecated methods"""
    print("Starting file processing...")
    
    # Using deprecated distutils
    try:
        debug_mode = strtobool(os.environ.get('DEBUG', 'false'))
        print(f"Debug mode: {debug_mode}")
    except (ValueError, AttributeError):
        print("Debug mode: False")
    
    # Using deprecated datetime method
    timestamp = datetime.datetime.utcnow().isoformat(' ')  # DEPRECATED
    print(f"Timestamp: {timestamp}")
    
    # Using deprecated platform method
    try:
        system_info = platform.platform()  # DEPRECATED: Removed in Python 3.8+
        print(f"System info: {system_info}")
    except AttributeError:
        print("Could not get system info (deprecated method)")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()