#!/usr/bin/env python3
"""
Script to answer all homework questions for Module 2.
This script downloads and analyzes the required taxi data files.
"""

import os
import gzip
import shutil
import pandas as pd
import requests
from typing import Dict, Any


def download_file(taxi_type: str, year: str, month: str) -> tuple:
    """Download and decompress a taxi data file."""
    month = month.zfill(2)
    filename = f"{taxi_type}_tripdata_{year}-{month}"
    gz_file = f"{filename}.csv.gz"
    csv_file = f"{filename}.csv"
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/{gz_file}"
    
    print(f"  Downloading: {url}")
    response = requests.get(url, stream=True)
    
    if response.status_code != 200:
        print(f"  Error: HTTP {response.status_code}")
        return None, None
    
    with open(gz_file, 'wb') as f:
        f.write(response.content)
    
    with gzip.open(gz_file, 'rb') as f_in:
        with open(csv_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(gz_file)
    return csv_file, filename


def get_file_info(csv_file: str) -> Dict[str, Any]:
    """Get file size and row count."""
    file_size = os.path.getsize(csv_file)
    file_size_mb = file_size / (1024 * 1024)
    
    df = pd.read_csv(csv_file)
    row_count = len(df)
    
    return {
        'size_mb': file_size_mb,
        'size_bytes': file_size,
        'row_count': row_count
    }


def question_1():
    """Question 1: Yellow Taxi Dec 2020 uncompressed file size."""
    print("\n" + "="*70)
    print("QUESTION 1: Yellow Taxi December 2020 - Uncompressed File Size")
    print("="*70)
    
    csv_file, _ = download_file('yellow', '2020', '12')
    if csv_file:
        info = get_file_info(csv_file)
        print(f"\nFile: {csv_file}")
        print(f"Uncompressed size: {info['size_mb']:.1f} MiB")
        print(f"Row count: {info['row_count']:,}")
        
        # Determine answer
        if 128 <= info['size_mb'] <= 129:
            answer = "A. 128.3 MiB"
        elif 134 <= info['size_mb'] <= 135:
            answer = "B. 134.5 MiB"
        elif 364 <= info['size_mb'] <= 365:
            answer = "C. 364.7 MiB"
        elif 692 <= info['size_mb'] <= 693:
            answer = "D. 692.6 MiB"
        else:
            answer = f"Closest match needed for {info['size_mb']:.1f} MiB"
        
        print(f"\nANSWER: {answer}")
        os.remove(csv_file)
    

def question_2():
    """Question 2: Rendered variable value."""
    print("\n" + "="*70)
    print("QUESTION 2: Rendered Variable Value")
    print("="*70)
    print("\nGiven:")
    print("  - inputs.taxi = 'green'")
    print("  - inputs.year = '2020'")
    print("  - inputs.month = '04'")
    print("  - variable: file = '{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv'")
    print("\nRendered value: green_tripdata_2020-04.csv")
    print("\nANSWER: B. green_tripdata_2020-04.csv")


def question_3():
    """Question 3: Yellow Taxi 2020 - Total rows for all CSV files."""
    print("\n" + "="*70)
    print("QUESTION 3: Yellow Taxi 2020 - Total Row Count (All Months)")
    print("="*70)
    
    total_rows = 0
    
    for month in range(1, 13):
        month_str = str(month).zfill(2)
        try:
            csv_file, _ = download_file('yellow', '2020', month_str)
            if csv_file:
                info = get_file_info(csv_file)
                print(f"  Month {month_str}: {info['row_count']:,} rows")
                total_rows += info['row_count']
                os.remove(csv_file)
        except Exception as e:
            print(f"  Month {month_str}: Error - {e}")
    
    print(f"\nTotal rows for Yellow Taxi 2020: {total_rows:,}")
    
    # Determine answer
    if 13_500_000 <= total_rows <= 13_600_000:
        answer = "A. 13,537,299"
    elif 24_600_000 <= total_rows <= 24_700_000:
        answer = "B. 24,648,499"
    elif 18_300_000 <= total_rows <= 18_400_000:
        answer = "C. 18,324,219"
    elif 29_400_000 <= total_rows <= 29_500_000:
        answer = "D. 29,430,127"
    else:
        answer = f"Closest match needed for {total_rows:,}"
    
    print(f"\nANSWER: {answer}")


def question_4():
    """Question 4: Green Taxi 2020 - Total rows for all CSV files."""
    print("\n" + "="*70)
    print("QUESTION 4: Green Taxi 2020 - Total Row Count (All Months)")
    print("="*70)
    
    total_rows = 0
    
    for month in range(1, 13):
        month_str = str(month).zfill(2)
        try:
            csv_file, _ = download_file('green', '2020', month_str)
            if csv_file:
                info = get_file_info(csv_file)
                print(f"  Month {month_str}: {info['row_count']:,} rows")
                total_rows += info['row_count']
                os.remove(csv_file)
        except Exception as e:
            print(f"  Month {month_str}: Error - {e}")
    
    print(f"\nTotal rows for Green Taxi 2020: {total_rows:,}")
    
    # Determine answer
    if 5_300_000 <= total_rows <= 5_400_000:
        answer = "A. 5,327,301"
    elif 900_000 <= total_rows <= 1_000_000:
        answer = "B. 936,199"
    elif 1_700_000 <= total_rows <= 1_800_000:
        answer = "C. 1,734,051"
    elif 1_300_000 <= total_rows <= 1_400_000:
        answer = "D. 1,342,034"
    else:
        answer = f"Closest match needed for {total_rows:,}"
    
    print(f"\nANSWER: {answer}")


def question_5():
    """Question 5: Yellow Taxi March 2021 - Row count."""
    print("\n" + "="*70)
    print("QUESTION 5: Yellow Taxi March 2021 - Row Count")
    print("="*70)
    
    csv_file, _ = download_file('yellow', '2021', '03')
    if csv_file:
        info = get_file_info(csv_file)
        print(f"\nFile: {csv_file}")
        print(f"Row count: {info['row_count']:,}")
        
        # Determine answer
        if 1_400_000 <= info['row_count'] <= 1_450_000:
            answer = "A. 1,428,092"
        elif 700_000 <= info['row_count'] <= 750_000:
            answer = "B. 706,911"
        elif 1_900_000 <= info['row_count'] <= 1_950_000:
            answer = "C. 1,925,152"
        elif 2_550_000 <= info['row_count'] <= 2_600_000:
            answer = "D. 2,561,031"
        else:
            answer = f"Closest match needed for {info['row_count']:,}"
        
        print(f"\nANSWER: {answer}")
        os.remove(csv_file)


def question_6():
    """Question 6: Timezone configuration."""
    print("\n" + "="*70)
    print("QUESTION 6: Configure Timezone to New York in Schedule Trigger")
    print("="*70)
    print("\nOptions:")
    print("  A. timezone: EST")
    print("  B. timezone: America/New_York")
    print("  C. timezone: UTC-5")
    print("  D. location: New_York")
    print("\nIn Kestra, timezone configuration follows the IANA Time Zone Database format.")
    print("The correct format for New York is 'America/New_York'.")
    print("\nExample configuration:")
    print("```yaml")
    print("triggers:")
    print("  - id: monthly_schedule")
    print("    type: io.kestra.plugin.core.trigger.Schedule")
    print("    cron: '0 0 1 * *'")
    print("    timezone: America/New_York")
    print("```")
    print("\nANSWER: B. Add a timezone property set to America/New_York in the Schedule trigger configuration")


def main():
    """Run all homework questions."""
    print("\n" + "="*70)
    print("MODULE 2 HOMEWORK - Data Engineering Zoomcamp")
    print("Kestra Workflow Orchestration Assignment")
    print("="*70)
    
    # Question 2 doesn't require downloads
    question_2()
    
    # Question 6 is conceptual
    question_6()
    
    # Questions requiring data downloads
    print("\n" + "="*70)
    print("DOWNLOADING AND ANALYZING DATA FILES")
    print("This may take several minutes...")
    print("="*70)
    
    question_1()
    question_3()
    question_4()
    question_5()
    
    print("\n" + "="*70)
    print("HOMEWORK COMPLETE!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
