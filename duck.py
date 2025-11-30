#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import argparse
import os # For file system checks
from typing import TextIO, Optional, Set, Dict
from urllib.parse import urljoin, urlparse

# --- ANSI COLOR CODES ---
HEADER = '\033[95m'   # Purple/Magenta
OKBLUE = '\033[94m'   # Blue (for prompts/data)
OKGREEN = '\033[92m'  # Green (for success/results)
WARNING = '\033[93m'  # Yellow (for status/warnings)
FAIL = '\033[91m'     # Red (for errors)
ENDC = '\033[0m'      # Reset color
BOLD = '\033[1m'      # Bold text

# --- EXPANDED EXTRACTION CATEGORIES AND REGEX PATTERNS ---
EXTRACTION_PATTERNS = {
    # 2. Email: Standard email address pattern
    2: {"name": "Email Addresses", "regex": r"\b[A-Za-z0m', color=True)
        sys.exit(1) # Exit code 1 for configuration failure
    
    # 3. Output Validation: Check writability
    output_path = os.path.abspath(args.output)
    output_dir = os.path.dirname(output_path)
    
    if output_dir and not os.path.exists(output_dir):
        print(f"\n{FAIL}ERROR: Output directory does not exist: {output_dir}{ENDC}")
        sys.exit(3) # Exit code 3 for file system/permission failure
        
    try:
        # Check permissions by attempting to open the file for appending
        with open(output_path, 'a') as f:
            pass
    except IOError:
        print(f"\n{FAIL}ERROR: Cannot write to output file: {output_path}. Check permissions.{ENDC}")
        sys.exit(3) # Exit code 3 for file system/permission failure

def parse_arguments():
    """Defines and parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description=f"{HEADER}XERON Deep Crawler: Mechanized, deep data acquisition tool.{ENDC}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-u', '--url', 
        type=str, 
        required=True, 
        help="REQUIRED: The absolute starting URL (e.g., https://target.com)."
    )
    parser.add_argument(
        '-d', '--depth', 
        type=int, 
        default=5, 
        help="Crawl depth limit (0 for root page only). Default: 5"
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default='roxen.txt', 
        help="Output file path for saving extracted data. Default: roxen.txt"
    )
    
    return parser.parse_args()


# --- Main Execution Refactored ---
def main():
    global crawled_urls, pages_to_crawl, total_extracted_data, session_cookies
    file_handle: Optional = None
    url_input = "N/A"
    
    try:
        # 1. ACQUIRE AND VALIDATE ARGUMENTS
        args = parse_arguments()
        validate_arguments(args)
        
        # Configuration setup after validation
        url_input = args.url
        
        # 2. UI START (Non-interactive)
        output(f"{HEADER}{BOLD}\n+------------------------------------+\n{ENDC}")
        output(f"{HEADER}{BOLD}| {OKGREEN}X E R O N   W E B   C R A W L E R{ENDC} {HEADER}{BOLD}|\n{ENDC}")
        output(f"{HEADER}{BOLD}+------------------------------------+\n{ENDC}")
        output(f"{OKGREEN}Target:{ENDC} {url_input}\n")
        output(f"{OKGREEN}Depth:{ENDC} {args.depth}\n")
        output(f"{OKGREEN}Output:{ENDC} {args.output}\n\n")

        # 3. Start File Output
        file_handle = open(args.output, 'w', encoding='utf-8')
        output(f"Started analysis at: {time.ctime()}\n", file_handle, color=False)
        output(f"Target: {url_input} (Depth: {args.depth})\n", file_handle, color=False)
        
        # 4. Core Crawl and Extraction (ASSUMING ALL CATEGORIES ARE SELECTED)
        loading_animation("Initializing mechanized deep crawl", 1.5)
        # Pass depth limit directly
        crawl_website(url_input, file_handle, args.depth) 
        loading_animation("Finalizing extraction report", 1.5)
        
        # 5. Print Final Results (Console and File)
        print_results(file_handle)
        print_results(None)
        
    except SystemExit as e:
        # Catch SystemExit raised by argparse or custom validation
        if e.code!= 0:
            print(f"{FAIL}Configuration Failed. Exiting with code {e.code}.{ENDC}")
        sys.exit(e.code)
    except Exception as e:
        output(f"\n{FAIL}An unexpected runtime error occurred: {e}{ENDC}\n", file_handle, color=True)
        sys.exit(4) # Operational failure code
    finally:
        if file_handle:
            file_handle.close()
            output(f"\n{OKGREEN}Results successfully saved and finalized in {args.output}.{ENDC}\n")
        
        # Ensure a non-empty report safeguard runs if execution reached the crawl stage
        if url_input!= "N/A":
            # Check file size to ensure it's not effectively empty (more than 100 bytes of just headers/initial log)
            try:
                if os.path.getsize(args.output) < 100:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write("XERON CRAWLER REPORT\n\n")
                        f.write(f"The crawl finished with no substantial data acquired. Target URL: {url_input}.\n")
                        f.write("Check network connection or ensure the target is online.")
                    output(f"\n{FAIL}Warning: Crawl found no substantial data. Minimal report saved to {args.output}.{ENDC}\n", color=True)
            except NameError:
                # args.output might not be defined if parsing failed early
                pass
            except FileNotFoundError:
                # File might not exist if system error occurred before creation
                pass


if __name__ == "__main__":
    main()
