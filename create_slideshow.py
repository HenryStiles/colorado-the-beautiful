# create_slideshow.py
import os
import subprocess

# --- Configuration ---
IMAGE_DIR = "/Users/henrys/source/colorado_the_beautiful/temp_images"
OUTPUT_PATH = "/Users/henrys/source/colorado_the_beautiful/slideshow.mp4"
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"

# The 9 photos in the exact order recommended for visual contrast
ORDERED_FILES = [
    "Christie_Green_Kenosha_Pass_CO_h-1024x768.jpg",
    "Lauren_Wallace_Island_Lake_02_h.jpg",
    "Christie_Green_Evergreen_CO_h-1024x768.jpg",
    "Arliss_Blackledge_AZ_h.jpg",
    "TatumSneedIdahoSpgs_v.jpg",
    "Pat_Fischer_James_Peak_Wilderness_CO_h-1024x768.jpg",
    "Christie_Green_Telluride_CO_v-768x1024.jpg",
    "Pat_Fischer_Mt_Bierstadt_CO_h-1024x768.jpg",
    "Laurie_Randolph_RMNP_CO_v-768x1024.jpg"
]

def main():
    # Verify ffmpeg exists
    if not os.path.exists(FFMPEG_PATH):
        print(f"Error: ffmpeg not found at {FFMPEG_PATH}")
        return

    # Check for images
    missing_files = []
    for f in ORDERED_FILES:
        path = os.path.join(IMAGE_DIR, f)
        if not os.path.exists(path):
            missing_files.append(f)
            
    if missing_files:
        print("Error: The following images are missing from temp_images folder:")
        for f in missing_files:
            print(f"  - {f}")
        return

    print("Generating video clips for the 9 slideshow images...")
    
    clip_list_path = os.path.join(IMAGE_DIR, "clips_list.txt")
    temp_clips = []
    
    with open(clip_list_path, "w") as f_list:
        for idx, filename in enumerate(ORDERED_FILES):
            input_img = os.path.join(IMAGE_DIR, filename)
            output_clip = os.path.join(IMAGE_DIR, f"clip_{idx}.mp4")
            
            # FFMPEG Command:
            # -loop 1: Loop the static image
            # -t 2: Duration of 2 seconds
            # -vf "scale... pad...": Fits the image to 1080x1920 vertical with black padding, keeping aspect ratio
            # -c:v libx264: H.264 video codec (Instagram-compatible)
            # -pix_fmt yuv420p: Pixel format required for mobile playback
            cmd = [
                FFMPEG_PATH,
                "-y",
                "-loop", "1",
                "-i", input_img,
                "-c:v", "libx264",
                "-t", "2",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
                "-r", "30",
                output_clip
            ]
            
            print(f"  [{idx+1}/9] Processing {filename} -> clip_{idx}.mp4...")
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Write to concat text file (use relative path or absolute path formatted for ffmpeg)
                f_list.write(f"file 'clip_{idx}.mp4'\n")
                temp_clips.append(output_clip)
            except subprocess.CalledProcessError as e:
                print(f"    Failed to process {filename}: {e}")
                return

    print("\nConcatenating clips into final slideshow...")
    # FFMPEG command to concatenate clips
    concat_cmd = [
        FFMPEG_PATH,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", clip_list_path,
        "-c", "copy",
        OUTPUT_PATH
    ]
    
    try:
        subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"\nSuccess! Slideshow saved to: {OUTPUT_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"Error during concatenation: {e}")
        return
        
    # Clean up temporary files
    print("Cleaning up temporary clips...")
    os.remove(clip_list_path)
    for clip in temp_clips:
        os.remove(clip)
    print("Clean-up complete!")

if __name__ == "__main__":
    main()
