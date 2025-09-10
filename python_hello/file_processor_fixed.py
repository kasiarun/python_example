#!/usr/bin/env python3
"""
Simple file processor with one deprecated method for testing
"""

import os
import datetime

def main():
    """Main function with one deprecated method"""
    print("Starting file processing...")
    
    # Using deprecated datetime method - this will show deprecation warning
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()  # DEPRECATED: Use datetime.datetime.now(datetime.timezone.utc) instead
    print(f"Timestamp: {timestamp}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()