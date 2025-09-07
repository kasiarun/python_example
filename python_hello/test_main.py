#!/usr/bin/env python3
"""
Test file for main.py to demonstrate compatibility issues
"""

import unittest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import main
except ImportError as e:
    raise ImportError(f"Import error: {e}")

class TestMainFunctionality(unittest.TestCase):
    """Test cases for main.py functionality"""
    
    def test_fetch_data_from_api(self):
        """Test API data fetching"""
        data = main.fetch_data_from_api()
        self.assertIsInstance(data, list)
        if data:  # If we got data
            self.assertGreater(len(data), 0)
    
    def test_process_data(self):
        """Test data processing with sample data"""
        sample_data = [
            {"id": 1, "title": "Test Post", "body": "Test content"},
            {"id": 2, "title": "Another Post", "body": "More content"}
        ]
        
        df, summary = main.process_data(sample_data)
        
        # This test will likely fail due to deprecated pandas methods
        self.assertIsNotNone(df)
        self.assertIsNotNone(summary)

if __name__ == "__main__":
    print("Running tests with potential compatibility issues...")
    unittest.main()