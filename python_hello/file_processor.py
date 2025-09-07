#!/usr/bin/env python3
"""
Simple file processor - Fixed version
This demonstrates resolved compatibility problems
"""

import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any

def read_config_file() -> Dict[str, Any]:
    """Read configuration using modern methods"""
    config_data = {
        "input_directory": "./data",
        "output_directory": "./output", 
        "file_types": [".txt", ".json", ".csv"],
        "max_file_size": 1000000
    }
    
    # Save config using proper datetime handling
    try:
        with open("config.json", "w", encoding='utf-8') as f:
            # Fixed: Convert datetime to string for JSON serialization
            config_data["created_at"] = datetime.datetime.now().isoformat()
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing config file: {e}")
    
    return config_data

def process_text_files(directory: str) -> List[Dict[str, Any]]:
    """Process text files using modern pathlib methods"""
    files_processed = []
    
    try:
        # Using modern pathlib approach instead of deprecated os.walk
        data_path = Path(directory)
        if not data_path.exists():
            print(f"Directory {directory} does not exist")
            return files_processed
            
        # Use pathlib.glob for better file handling
        for file_path in data_path.rglob('*.txt'):
            try:
                # Modern file reading with proper error handling
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Improved processing with better error handling
                word_count = len(content.split())
                line_count = len(content.splitlines())
                
                files_processed.append({
                    'filename': file_path.name,
                    'path': str(file_path),
                    'word_count': word_count,
                    'line_count': line_count,
                    'size': file_path.stat().st_size
                })
                
            except (IOError, UnicodeDecodeError) as e:
                print(f"Error processing file {file_path}: {e}")
                continue
                
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")
    
    return files_processed

def create_sample_data() -> None:
    """Create sample data files with proper error handling"""
    try:
        # Use pathlib for directory creation
        Path("data").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)
        
        # Create sample text files
        sample_files = {
            "data/sample1.txt": "Hello world!\nThis is a test file.\nIt has multiple lines.",
            "data/sample2.txt": "Another test file with different content.\nMore text here.",
            "data/readme.txt": "This is a readme file.\nIt contains instructions.\nPlease read carefully."
        }
        
        for filepath, content in sample_files.items():
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            except IOError as e:
                print(f"Error creating file {filepath}: {e}")
        
        print("Sample data files created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

def save_results(processed_files: List[Dict[str, Any]]) -> None:
    """Save results with proper error handling"""
    try:
        # Create summary
        total_files = len(processed_files)
        total_words = sum(f['word_count'] for f in processed_files)
        total_lines = sum(f['line_count'] for f in processed_files)
        
        summary = {
            'total_files': total_files,
            'total_words': total_words,
            'total_lines': total_lines,
            'processed_at': datetime.datetime.now().isoformat(),  # Fixed: Already a string
            'files': processed_files
        }
        
        # Ensure output directory exists
        Path('output').mkdir(exist_ok=True)
        
        # Save JSON with proper error handling
        try:
            with open('output/summary.json', 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving JSON summary: {e}")
        
        # Save text report with proper error handling
        try:
            with open('output/report.txt', 'w', encoding='utf-8') as f:
                f.write("File Processing Report\n")
                f.write("=====================\n\n")
                f.write(f"Total files processed: {total_files}\n")
                f.write(f"Total words: {total_words}\n")
                f.write(f"Total lines: {total_lines}\n\n")
                
                f.write("File Details:\n")
                for file_info in processed_files:
                    f.write(f"- {file_info['filename']}: {file_info['word_count']} words, {file_info['line_count']} lines\n")
        except IOError as e:
            print(f"Error saving text report: {e}")
            
    except Exception as e:
        print(f"Error in save_results: {e}")

def main() -> None:
    """Main function with improved error handling"""
    print("Starting file processing...")
    
    try:
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
        save_results(processed_files)
        print("Results saved successfully!")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()