# write_exif_metadata.py
import os
import subprocess
import openpyxl

# --- Configuration ---
EXCEL_PATH = "/Users/henrys/source/colorado_the_beautiful/Outreach list.xlsx"

# Path to the directory containing your local images before you upload them.
# Change this to the actual folder path where your photos are stored locally.
IMAGE_DIR = "/Users/henrys/source/colorado_the_beautiful/images"

# Path to your exiftool installation (we detected it at /opt/homebrew/bin/exiftool)
EXIFTOOL_PATH = "/opt/homebrew/bin/exiftool"

def tag_image_metadata(filepath, author, title, story):
    """Runs exiftool to write EXIF, IPTC, and XMP metadata tags to an image file."""
    # Build standard tags
    # - Artist / By-line / Creator: Author credit
    # - Copyright / CopyrightNotice / Rights: Licensing info
    # - ImageDescription / Caption-Abstract / Description: Story
    # - ObjectName / Title: Landmark name
    
    cmd = [
        EXIFTOOL_PATH,
        # 1. Author tags
        f"-Artist={author}",
        f"-By-line={author}",
        f"-Creator={author}",
        
        # 2. License tags
        "-Copyright=Used by permission",
        "-CopyrightNotice=Used by permission",
        "-Rights=Used by permission",
        
        # 3. Story / Description tags
        f"-ImageDescription={story}",
        f"-Caption-Abstract={story}",
        f"-Description={story}",
        
        # 4. Title / Object Name tags
        f"-ObjectName={title}",
        f"-Title={title}",
        
        # Overwrite the file in-place without creating a '_original' backup file
        "-overwrite_original",
        
        filepath
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"      Error tagging {os.path.basename(filepath)}: {e.stderr.decode().strip()}")
        return False

def main():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Excel file not found at {EXCEL_PATH}")
        return
        
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Local image directory '{IMAGE_DIR}' not found. Please create it or adjust the script configuration.")
        return

    print(f"Reading spreadsheet: {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb['SUBMISSION Yeses']
    
    tagged_count = 0
    missing_count = 0
    
    # Read rows skipping header
    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        submitter = row[0]
        place_name = row[2]
        photo_url = row[4]
        story = row[5]
        
        # Skip empty rows
        if not submitter or not place_name or not photo_url:
            continue
            
        # Extract the filename from the URL (e.g. 'Arliss_Blackledge_AZ_h.jpg')
        filename = os.path.basename(photo_url.split('?')[0]) # Strip query parameters if any
        local_path = os.path.join(IMAGE_DIR, filename)
        
        print(f"Row {idx}: Submitter='{submitter}', Place='{place_name}', Filename='{filename}'")
        
        if os.path.exists(local_path):
            print(f"  -> File found! Tagging metadata...")
            success = tag_image_metadata(
                filepath=local_path,
                author=submitter.strip(),
                title=place_name.strip(),
                story=story.strip() if story else ""
            )
            if success:
                tagged_count += 1
        else:
            print(f"  -> [Skip] Local file not found in '{IMAGE_DIR}'.")
            missing_count += 1
            
    print("\nMetadata tagging summary:")
    print(f"  Successfully tagged: {tagged_count} files")
    print(f"  Local files missing: {missing_count} files")

if __name__ == "__main__":
    main()
