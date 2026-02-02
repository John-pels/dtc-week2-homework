#!/usr/bin/env python3
"""
Script to download and analyze taxi data files.
Usage: python analyze_file.py <taxi_type> <year> <month>
Example: python analyze_file.py yellow 2020 12
"""

import sys
import os
import gzip
import shutil
import pandas as pd
import requests
from pathlib import Path


def download_and_analyze(taxi_type: str, year: str, month: str):
    """Download and analyze a specific taxi data file."""
    
    # Format month with leading zero
    month = month.zfill(2)
    
    # Construct URLs and file names
    filename = f"{taxi_type}_tripdata_{year}-{month}"
    gz_file = f"{filename}.csv.gz"
    csv_file = f"{filename}.csv"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/{gz_file}"
    
    print(f"Downloading: {url}")
    
    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"Error: Failed to download file. Status code: {response.status_code}")
        return
    
    # Save compressed file
    with open(gz_file, 'wb') as f:
        f.write(response.content)
    
    print(f"Downloaded: {gz_file}")
    
    # Decompress the file
    with gzip.open(gz_file, 'rb') as f_in:
        with open(csv_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print(f"Decompressed: {csv_file}")
    
    # Get file size
    file_size = os.path.getsize(csv_file)
    file_size_mb = file_size / (1024 * 1024)
    
    # Read and analyze the CSV
    print(f"\nReading CSV file...")
    df = pd.read_csv(csv_file)
    
    row_count = len(df)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"File: {csv_file}")
    print(f"{'='*60}")
    print(f"Uncompressed file size: {file_size_mb:.1f} MiB ({file_size:,} bytes)")
    print(f"Row count: {row_count:,}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")
    print(f"{'='*60}\n")
    
    # Clean up compressed file
    os.remove(gz_file)
    
    return {
        'file': csv_file,
        'size_mb': file_size_mb,
        'size_bytes': file_size,
        'row_count': row_count,
        'columns': list(df.columns)
    }


def analyze_year(taxi_type: str, year: str, start_month: int = 1, end_month: int = 12):
    """Analyze all months in a year."""
    
    total_rows = 0
    results = []
    
    print(f"\nAnalyzing {taxi_type} taxi data for year {year}")
    print(f"Months: {start_month} to {end_month}\n")
    
    for month in range(start_month, end_month + 1):
        month_str = str(month).zfill(2)
        try:
            result = download_and_analyze(taxi_type, year, month_str)
            if result:
                total_rows += result['row_count']
                results.append(result)
                # Clean up CSV file
                if os.path.exists(result['file']):
                    os.remove(result['file'])
        except Exception as e:
            print(f"Error processing {year}-{month_str}: {e}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL for {taxi_type} taxi {year}:")
    print(f"Total rows: {total_rows:,}")
    print(f"Files processed: {len(results)}")
    print(f"{'='*60}\n")
    
    return total_rows


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python analyze_file.py <taxi_type> <year> <month>")
        print("       python analyze_file.py <taxi_type> <year> all")
        print("\nExamples:")
        print("  python analyze_file.py yellow 2020 12")
        print("  python analyze_file.py yellow 2020 all")
        print("  python analyze_file.py green 2020 all")
        sys.exit(1)
    
    taxi_type = sys.argv[1]
    year = sys.argv[2]
    month = sys.argv[3]
    
    if month.lower() == 'all':
        analyze_year(taxi_type, year)
    else:
        download_and_analyze(taxi_type, year, month)
