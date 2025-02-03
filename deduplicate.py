import os
import subprocess
import shutil

def get_phash(image_path):
    """Compute perceptual hash (pHash) for an image using the Perl script."""
    try:
        result = subprocess.run(["perl", "/bin/phash.pl", image_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def find_and_remove_duplicates(image_dir):
    """Find and move duplicate images to a 'duplicates' folder."""
    
    # ✅ Ensure the images directory exists
    if not os.path.exists(image_dir):
        print(f"⚠️ Directory '{image_dir}' does not exist. Creating it now...")
        os.makedirs(image_dir, exist_ok=True)
        return  # Exit the function since no images are available

    duplicates_folder = os.path.join(image_dir, "duplicates")
    os.makedirs(duplicates_folder, exist_ok=True)  # Ensure duplicate directory exists

    phash_dict = {}  # Stores {phash: first_seen_image_path}

    for filename in os.listdir(image_dir):
        image_path = os.path.join(image_dir, filename)

        if not os.path.isfile(image_path):
            continue  # Skip non-files

        phash = get_phash(image_path)
        if phash is None:
            continue  # Skip images that failed hashing

        if phash in phash_dict:
            duplicate_path = os.path.join(duplicates_folder, filename)
            print(f"🛠 Moving duplicate: {image_path} → {duplicate_path}")
            shutil.move(image_path, duplicate_path)  # Move duplicate image
        else:
            phash_dict[phash] = image_path  # Store first occurrence

if __name__ == "__main__":
    IMAGE_DIRECTORY = "/images"  # Change this to your image directory
    find_and_remove_duplicates(IMAGE_DIRECTORY)
