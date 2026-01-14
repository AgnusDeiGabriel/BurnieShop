import csv
import os
import requests
import time
from urllib.parse import urlparse

# Configuration
CSV_FILE = "products.csv"
OUTPUT_FOLDER = "images"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def sanitize_filename(title):
    """Convert product title to a safe filename."""
    # Remove/replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    filename = title
    for char in invalid_chars:
        filename = filename.replace(char, '')
    # Limit length and strip whitespace
    filename = filename.strip()[:100]
    return filename


def get_extension(url):
    """Extract file extension from URL."""
    parsed = urlparse(url.split('?')[0])
    path = parsed.path
    if '.' in path:
        ext = path.rsplit('.', 1)[-1].lower()
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            return f".{ext}"
    return ".jpg"  # Default


def download_image(url, filepath):
    """Download an image from URL to filepath."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    # Create output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created folder: {OUTPUT_FOLDER}")

    # Read CSV
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)

    print(f"Found {len(products)} products to download")
    print("=" * 50)

    downloaded = 0
    skipped = 0
    failed = 0

    for i, product in enumerate(products, 1):
        title = product.get('title', f'product_{i}')
        image_url = product.get('image', '')

        if not image_url or image_url == 'N/A':
            print(f"[{i}/{len(products)}] {title[:40]}... - SKIPPED (no image)")
            skipped += 1
            continue

        # Create filename
        safe_title = sanitize_filename(title)
        ext = get_extension(image_url)
        filename = f"{i:04d}_{safe_title}{ext}"
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"[{i}/{len(products)}] {title[:40]}... - EXISTS")
            downloaded += 1
            continue

        print(f"[{i}/{len(products)}] {title[:40]}...", end=" ")

        if download_image(image_url, filepath):
            print("OK")
            downloaded += 1
        else:
            failed += 1

        # Small delay to be polite
        time.sleep(0.2)

    print("=" * 50)
    print(f"Downloaded: {downloaded}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Images saved to: {OUTPUT_FOLDER}/")


if __name__ == "__main__":
    main()
