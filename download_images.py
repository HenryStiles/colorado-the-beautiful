# download_images.py
import os
import urllib.request
import openpyxl

# --- Configuration ---
EXCEL_PATH = "/Users/henrys/source/colorado_the_beautiful/Outreach list.xlsx"
TARGET_DIR = "/Users/henrys/source/colorado_the_beautiful/local copy of images"

def download_file(url, target_path):
    """Downloads a file from a URL using urllib."""
    print(f"Downloading: {url} -> {os.path.basename(target_path)}")
    try:
        # Standard user-agent header to bypass simple bot blocks
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req) as response:
            with open(target_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"  -> Success!")
        return True
    except Exception as e:
        print(f"  -> Error downloading file: {e}")
        return False

def main():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Excel file not found at {EXCEL_PATH}")
        return
        
    os.makedirs(TARGET_DIR, exist_ok=True)
    print(f"Created/verified target directory: '{TARGET_DIR}'")

    print(f"Loading spreadsheet: {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb['SUBMISSION Yeses']
    
    download_count = 0
    skipped_count = 0
    
    # Read rows skipping header
    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        submitter = row[0]
        place_name = row[2]
        photo_url = row[4]
        
        # Skip empty rows
        if not submitter or not place_name or not photo_url:
            continue
            
        # Extract the filename from the URL (e.g. 'Arliss_Blackledge_AZ_h.jpg')
        filename = os.path.basename(photo_url.split('?')[0])
        local_path = os.path.join(TARGET_DIR, filename)
        
        if os.path.exists(local_path):
            print(f"Row {idx}: {filename} already exists locally. Skipping.")
            skipped_count += 1
        else:
            print(f"Row {idx}: New photo found.")
            success = download_file(photo_url, local_path)
            if success:
                download_count += 1
                
    print("\nDownload Summary:")
    print(f"  Successfully downloaded: {download_count} files")
    print(f"  Already existed: {skipped_count} files")

if __name__ == "__main__":
    main()
