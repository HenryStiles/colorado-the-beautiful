# sanitize_names.py
import os
import re
import uuid

# Change this to the folder you want to sanitize (e.g. "./temp_images")
TARGET_DIR = "./temp_images"

def sanitize_filename(filename):
    """Sanitizes a filename by replacing spaces/hyphens with underscores,

    removing all shell-unsafe characters, and handling empty names.

    """
    # Separate the name and extension (e.g. "My Photo" and ".jpg")
    name, ext = os.path.splitext(filename)
    
    # 1. Replace spaces and consecutive hyphens/underscores with a single underscore
    cleaned = re.sub(r'[\s-]+', '_', name)
    
    # 2. Strip out all characters that aren't alphanumeric, dot, hyphen, or underscore
    cleaned = re.sub(r'[^a-zA-Z0-9._-]', '', cleaned)
    
    # 3. Trim leading/trailing underscores and dots
    cleaned = cleaned.strip('_').strip('.')
    
    # 4. Handle edge case: if the filename is now empty (e.g., it was originally "%$#&.jpg")
    if not cleaned:
        cleaned = f"file_{uuid.uuid4().hex[:8]}"
        
    return cleaned + ext

def main():
    import sys
    
    # 1. Handle command line arguments (e.g. globs like temp_images/*.jpg)
    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]
        print(f"Sanitizing {len(file_paths)} specified file paths...")
        renamed_count = 0
        
        for filepath in file_paths:
            if not os.path.isfile(filepath):
                continue
                
            dir_name = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            
            # Skip hidden files
            if filename.startswith('.'):
                continue
                
            new_name = sanitize_filename(filename)
            
            if filename != new_name:
                new_path = os.path.join(dir_name, new_name)
                
                # Prevent overwriting if the new name already exists
                if os.path.exists(new_path):
                    name, ext = os.path.splitext(new_name)
                    new_name = f"{name}_{uuid.uuid4().hex[:4]}{ext}"
                    new_path = os.path.join(dir_name, new_name)
                    
                print(f"Renaming: '{filepath}' -> '{os.path.join(dir_name, new_name)}'")
                os.rename(filepath, new_path)
                renamed_count += 1
                
        print(f"\nCompleted! Renamed {renamed_count} files.")
        return

    # 2. Default: Scan default directory if no arguments are passed
    if not os.path.exists(TARGET_DIR):
        print(f"Directory '{TARGET_DIR}' not found. Usage: python3 sanitize_names.py [files/globs]")
        return
        
    print(f"No files specified. Sanitizing all files in default directory '{TARGET_DIR}'...")
    
    files = [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f))]
    renamed_count = 0
    
    for filename in files:
        # Skip hidden files like .DS_Store
        if filename.startswith('.'):
            continue
            
        new_name = sanitize_filename(filename)
        
        if filename != new_name:
            old_path = os.path.join(TARGET_DIR, filename)
            new_path = os.path.join(TARGET_DIR, new_name)
            
            # Prevent overwriting if the new name already exists
            if os.path.exists(new_path):
                name, ext = os.path.splitext(new_name)
                new_name = f"{name}_{uuid.uuid4().hex[:4]}{ext}"
                new_path = os.path.join(TARGET_DIR, new_name)
                
            print(f"Renaming: '{filename}' -> '{new_name}'")
            os.rename(old_path, new_path)
            renamed_count += 1
            
    print(f"\nCompleted! Renamed {renamed_count} files.")

if __name__ == "__main__":
    main()
