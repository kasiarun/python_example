#!/usr/bin/env python3
"""
Simple file processor with dependency issues
This demonstrates basic compatibility problems
"""

import os
import json
import datetime

def read_config_file():
    """Read configuration using deprecated methods"""
    config_data = {
        "input_directory": "./data",
        "output_directory": "./output", 
        "file_types": [".txt", ".json", ".csv"],
        "max_file_size": 1000000
    }
    
    # Save config using deprecated approach
    with open("config.json", "w", encoding='utf-8') as f:
        # This will cause issues with datetime serialization
        config_data["created_at"] = datetime.datetime.now()  # ERROR: Raw datetime object
        json.dump(config_data, f)
    
    return config_data

def process_text_files(directory):
    """Process text files with deprecated os methods"""
    files_processed = []
    
    # Using deprecated os.walk approach
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                
                # Deprecated file reading without proper encoding
                with open(file_path, 'r') as f:  # ERROR: No encoding specified
                    content = f.read()
                
                # Simple processing
                word_count = len(content.split())
                line_count = len(content.split('\n'))
                
                files_processed.append({
                    'filename': file,
                    'path': file_path,
                    'word_count': word_count,
                    'line_count': line_count,
                    'size': os.path.getsize(file_path)
                })
    
    return files_processed

def create_sample_data():
    """Create sample data files"""
    # Create directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Create sample text files
    sample_files = {
        "data/sample1.txt": "Hello world!\nThis is a test file.\nIt has multiple lines.",
        "data/sample2.txt": "Another test file with different content.\nMore text here.",
        "data/readme.txt": "This is a readme file.\nIt contains instructions.\nPlease read carefully."
    }
    
    for filepath, content in sample_files.items():
        with open(filepath, 'w') as f:  # ERROR: No encoding specified
            f.write(content)
    
    print("Sample data files created!")

def save_results(processed_files):
    """Save results with potential issues"""
    # Create summary
    total_files = len(processed_files)
    total_words = sum(f['word_count'] for f in processed_files)
    total_lines = sum(f['line_count'] for f in processed_files)
    
    summary = {
        'total_files': total_files,
        'total_words': total_words,
        'total_lines': total_lines,
        'processed_at': datetime.datetime.now(),  # ERROR: Raw datetime object will cause JSON serialization failure
        'files': processed_files
    }
    
    # Save with potential encoding issues
    with open('output/summary.json', 'w') as f:  # ERROR: No encoding specified
        json.dump(summary, f, indent=2)  # Will fail due to datetime object
    
    # Also save as text report
    with open('output/report.txt', 'w') as f:  # ERROR: No encoding specified
        f.write(f"File Processing Report\n")
        f.write(f"=====================\n\n")
        f.write(f"Total files processed: {total_files}\n")
        f.write(f"Total words: {total_words}\n")
        f.write(f"Total lines: {total_lines}\n\n")
        
        f.write("File Details:\n")
        for file_info in processed_files:
            f.write(f"- {file_info['filename']}: {file_info['word_count']} words, {file_info['line_count']} lines\n")

def main():
    """Main function"""
    print("Starting file processing...")
    
    # Create sample data
    create_sample_data()
    
    # Read configuration
    config = read_config_file()
    print(f"Configuration loaded: {config}")
    
    # Process files
    input_dir = config['input_directory']
    processed_files = process_text_files(input_dir)
    
    print(f"Processed {len(processed_files)} files")
    
    # Save results
    try:
        save_results(processed_files)
        print("Results saved successfully!")
    except Exception as e:
        print(f"Error saving results: {e}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()