import os
import subprocess
import shutil

def get_phash(image_path):
    """Compute perceptual hash (pHash) for an image using the Perl script."""
    try:
        result = subprocess.run(["perl", "/app/bin/phash.pl", image_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None  # Return None so we skip failed images

def find_and_remove_duplicates(image_dir):
    """Find and move duplicate images into separate 'duplicates' folders inside each team folder."""
    
    if not os.path.exists(image_dir):
        print(f"⚠️ Directory '{image_dir}' does not exist. Creating it now...")
        os.makedirs(image_dir, exist_ok=True)
        return  # Exit function if no images exist

    phash_dict = {}  # Stores {phash: first_seen_image_path}

    for team_folder in os.listdir(image_dir):
        team_path = os.path.join(image_dir, team_folder)
        if not os.path.isdir(team_path):  # Skip non-directories
            continue
        
        duplicates_folder = os.path.join(team_path, "duplicates")
        os.makedirs(duplicates_folder, exist_ok=True)  # Ensure duplicate directory exists

        for filename in os.listdir(team_path):
            image_path = os.path.join(team_path, filename)

            if not os.path.isfile(image_path):
                continue  # Skip non-files

            phash = get_phash(image_path)
            if phash is None:
                print(f"⚠️ Skipping {image_path} due to hash failure.")
                continue  # Skip images that failed hashing

            if phash in phash_dict:
                duplicate_path = os.path.join(duplicates_folder, filename)
                print(f"🛠 Moving duplicate: {image_path} → {duplicate_path}")
                shutil.move(image_path, duplicate_path)  # Move duplicate image
            else:
                phash_dict[phash] = image_path  # Store first occurrence

    commit_and_push_changes(image_dir)

def commit_and_push_changes(image_dir):
    """Commit and push duplicate images to GitHub."""
    print("📌 Committing and pushing duplicate images to GitHub...")

    try:
        subprocess.run(["git", "status"], check=True)  # Debugging step
        subprocess.run(["git", "add", image_dir], check=True)
        
        result = subprocess.run(["git", "diff", "--staged", "--quiet"])
        if result.returncode == 0:
            print("✅ No new duplicates to commit.")
            return

        subprocess.run(["git", "commit", "-m", "Moved duplicate images [Automated]"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Duplicates pushed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error while committing changes: {e}")

if __name__ == "__main__":
    IMAGE_DIRECTORY = "/images"
    find_and_remove_duplicates(IMAGE_DIRECTORY)
