#!/usr/bin/env python3
"""
Colorado the Beautiful - Batch Image Resizer
Downscales all images in the temp_images directory to fit within a 1600x900 box
while maintaining their aspect ratio and preserving EXIF metadata.
"""

import os
from PIL import Image

IMAGE_DIR = "/Users/henrys/source/colorado_the_beautiful/temp_images"
MAX_WIDTH = 1600
MAX_HEIGHT = 900
QUALITY = 85  # Standard web optimization quality

def resize_image(filepath):
    try:
        with Image.open(filepath) as img:
            orig_width, orig_height = img.size
            
            # Check if resizing is needed
            if orig_width <= MAX_WIDTH and orig_height <= MAX_HEIGHT:
                print(f"Skipping '{os.path.basename(filepath)}' - already within {MAX_WIDTH}x{MAX_HEIGHT} ({orig_width}x{orig_height}px)")
                return False
            
            # Preserve orientation & calculate new size
            ratio = min(MAX_WIDTH / orig_width, MAX_HEIGHT / orig_height)
            new_width = int(orig_width * ratio)
            new_height = int(orig_height * ratio)
            
            # If it's a portrait image, fit the long edge to the larger constraint
            if orig_height > orig_width:
                # Long edge (height) becomes 900 or 1600? 
                # Colleague said 1600x900 max, which usually refers to landscape.
                # For portrait, we want the long edge (height) to be max 1600, short edge (width) max 900.
                portrait_ratio = min(MAX_HEIGHT / orig_width, MAX_WIDTH / orig_height)
                new_width = int(orig_width * portrait_ratio)
                new_height = int(orig_height * portrait_ratio)
                
            # Perform resize
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Preserve EXIF metadata if present
            exif = img.info.get('exif')
            
            # Save back to same file, replacing the heavy original
            if exif:
                resized_img.save(filepath, format=img.format, quality=QUALITY, exif=exif, optimize=True)
            else:
                resized_img.save(filepath, format=img.format, quality=QUALITY, optimize=True)
                
            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"Resized '{os.path.basename(filepath)}': {orig_width}x{orig_height}px ➡️ {new_width}x{new_height}px ({file_size_mb:.2f} MB)")
            return True
            
    except Exception as e:
        print(f"Error processing '{os.path.basename(filepath)}': {e}")
        return False

def main():
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Target directory '{IMAGE_DIR}' not found.")
        return

    print("=" * 80)
    print(" COLORADO THE BEAUTIFUL - IMAGE RESIZER & OPTIMIZER")
    print(f" Target Box: {MAX_WIDTH}x{MAX_HEIGHT} max | Quality: {QUALITY}%")
    print("=" * 80)

    extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    all_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(extensions)]
    
    print(f"Found {len(all_files)} images in '{IMAGE_DIR}'. Starting processing...\n")
    
    resized_count = 0
    skipped_count = 0
    
    for filename in all_files:
        filepath = os.path.join(IMAGE_DIR, filename)
        was_resized = resize_image(filepath)
        if was_resized:
            resized_count += 1
        else:
            skipped_count += 1
            
    print("\n" + "=" * 80)
    print(" RESIZING SUMMARY")
    print("=" * 80)
    print(f"Total processed: {len(all_files)}")
    print(f"  Successfully resized: {resized_count}")
    print(f"  Skipped (already small): {skipped_count}")

if __name__ == "__main__":
    main()
