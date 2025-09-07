#!/usr/bin/env python3
"""
Simple web scraper and data processor
This program demonstrates issues with outdated dependencies
"""

import requests
import pandas as pd
import json
from datetime import datetime
import sys

def fetch_data_from_api():
    """Fetch sample data from a public API"""
    try:
        # Using old requests syntax that may have security issues
        response = requests.get(
            'https://jsonplaceholder.typicode.com/posts',
            verify=False,  # This is deprecated and insecure
            timeout=30
        )
        
        # Old way of handling JSON that's less robust
        data = json.loads(response.text)
        return data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def process_data(data):
    """Process the fetched data using pandas"""
    try:
        # Create DataFrame using old pandas syntax
        df = pd.DataFrame(data)
        
        # Using deprecated pandas methods
        df['created_at'] = datetime.now()
        
        # Old way of handling missing values (deprecated in newer pandas)
        df = df.fillna(method='ffill')  # This method is deprecated
        
        # Using deprecated pandas functionality
        summary = df.describe(include='all')
        
        return df, summary
    
    except Exception as e:
        print(f"Error processing data: {e}")
        return None, None

def save_results(df, summary):
    """Save results to files"""
    try:
        # Using old pandas to_csv syntax
        df.to_csv('python_hello/results.csv', index=False, encoding='utf-8')
        
        # Save summary
        with open('python_hello/summary.txt', 'w') as f:
            f.write(str(summary))
            
        print("Results saved successfully!")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    """Main function"""
    print("Starting data processing...")
    print(f"Python version: {sys.version}")
    
    # Fetch data
    print("Fetching data from API...")
    data = fetch_data_from_api()
    
    if not data:
        print("No data fetched. Exiting.")
        return
    
    print(f"Fetched {len(data)} records")
    
    # Process data
    print("Processing data...")
    df, summary = process_data(data)
    
    if df is None:
        print("Data processing failed. Exiting.")
        return
    
    # Save results
    print("Saving results...")
    save_results(df, summary)
    
    print("Processing complete!")

if __name__ == "__main__":
    main()