import os
import pillow_heif
from PIL import Image

# Enable HEIC support
pillow_heif.register_heif_opener()

# --- CONFIGURATION ---
INPUT_DIR = 'Daddy Chug_z' 
OUTPUT_DIR = 'Public/Daddy Chug_z'

# The quality level (1 to 95). 40 is a very AGGRESSIVE setting for max size reduction.
QUALITY_LEVEL = 85

# File extensions to look for (case-insensitive)
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.heic')
# ---------------------

def resize_image(img, max_size=(3000, 3000)):
    # Resize only if the image is larger than the maximum size
    # if img.width > max_size[0] or img.height > max_size[1]:
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

def compress_image(filepath, output_dir, quality):
    """Opens an image, compresses it aggressively, and saves it."""
    try:
        img = Image.open(filepath)
        img = resize_image(img)
        filename = os.path.basename(filepath)
        
        # Determine the output format based on compression goal
        output_format = "JPEG"
        
        # 1. Convert to RGB for maximum JPEG compatibility (and size reduction)
        if img.mode in ('RGBA', 'P', 'L'):
            img = img.convert('RGB')

        # 2. Define the new file path, ensuring a .jpg extension
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}.jpg"
        output_filepath = os.path.join(output_dir, output_filename)

        # 3. Save the image with aggressive compression parameters
        img.save(
            output_filepath, 
            output_format, 
            quality=quality, 
            optimize=True
        )
        
        # Display file size change (optional, but useful)
        original_size = os.path.getsize(filepath) / (1024 * 1024)
        new_size = os.path.getsize(output_filepath) / (1024 * 1024)
        
        print(f"✅ Processed: {filename}")
        print(f"   - Original Size: {original_size:.2f} MB")
        print(f"   - Compressed Size: {new_size:.2f} MB")
        print(f"   - Reduction: {((original_size - new_size) / original_size) * 100:.2f}%")
        
    except Exception as e:
        print(f"❌ Error compressing {filename}: {e}")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    if not os.path.exists(INPUT_DIR):
        print(f"🛑 Input directory '{INPUT_DIR}' not found. Please create it and add images.")
        return

    print(f"Starting aggressive compression (Quality={QUALITY_LEVEL}) in '{INPUT_DIR}'...")
    
    file_list = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(IMAGE_EXTENSIONS)]
    
    if not file_list:
        print("No images found in the input directory.")
        return

    for filename in file_list:
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(filepath):
            compress_image(filepath, OUTPUT_DIR, QUALITY_LEVEL)
            
    print("\n✨ Aggressive compression complete!")

if __name__ == "__main__":
    main()