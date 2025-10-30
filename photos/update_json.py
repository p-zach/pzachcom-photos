import os
import json
from PIL import Image

def update_photos_json(json_path="photos.json", image_dir="."):
    # Load existing photos.json or initialize new one
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"photos": []}

    # Get list of current JPGs in the directory
    jpg_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(".jpg")])
    existing_names = {photo["name"] for photo in data["photos"]}

    # --- Add new photos ---
    for filename in jpg_files:
        if filename not in existing_names:
            try:
                with Image.open(os.path.join(image_dir, filename)) as img:
                    width, height = img.size
            except Exception as e:
                print(f"Warning: Could not open {filename}: {e}")
                continue

            data["photos"].append({
                "name": filename,
                "width": width,
                "height": height,
                "alt": ""
            })

    # --- Remove missing photos ---
    data["photos"] = [photo for photo in data["photos"] if photo["name"] in jpg_files]

    # --- Sort alphabetically ---
    data["photos"] = sorted(data["photos"], key=lambda x: x["name"])

    # --- Save JSON ---
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated {json_path}: {len(data['photos'])} entries total.")

if __name__ == "__main__":
    update_photos_json()
