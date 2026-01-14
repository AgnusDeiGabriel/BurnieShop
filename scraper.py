import csv
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Configuration
BASE_URL = "https://shop.mayvenn.com/collections"
MAX_PAGES = 10
OUTPUT_FILE = "products.csv"


def create_driver(headless=True, proxy=None):
    """Create a Selenium WebDriver instance."""
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def fetch_page_selenium(driver, url, wait_time=5):
    """Fetch a page using Selenium and wait for content to load."""
    try:
        driver.get(url)
        # Wait for product elements to load
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']"))
        )
        # Extra wait for prices to render
        time.sleep(2)
        return driver.page_source
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_products(soup):
    """Parse product items from the page."""
    products = []
    seen_titles = set()

    # Find all product cards/containers
    product_containers = soup.select(
        ".product-card, .product-item, .grid__item, "
        "[class*='product'], [data-product]"
    )

    if product_containers:
        for container in product_containers:
            # Find product link
            link = container.select_one("a[href*='/products/']")
            if not link:
                continue

            title = link.get("title") or link.get_text(strip=True)
            if not title or title in seen_titles or len(title) < 3:
                continue

            seen_titles.add(title)

            # Find price - try multiple selectors
            price = "N/A"
            price_selectors = [
                ".price", "[class*='price']", ".money",
                "[class*='Price']", "span[class*='price']"
            ]
            for selector in price_selectors:
                price_el = container.select_one(selector)
                if price_el:
                    price_text = price_el.get_text(strip=True)
                    if "$" in price_text or price_text.replace(".", "").replace(",", "").isdigit():
                        price = price_text
                        break

            # Find image URL
            image_url = "N/A"
            img_selectors = [
                "img[src*='/products/']", "img[src*='/files/']",
                "img[data-src]", "img.product-image", "img"
            ]
            for selector in img_selectors:
                img_el = container.select_one(selector)
                if img_el:
                    # Try different attributes for image URL
                    img_src = (
                        img_el.get("src") or
                        img_el.get("data-src") or
                        img_el.get("data-srcset", "").split()[0] or
                        img_el.get("srcset", "").split()[0]
                    )
                    if img_src and len(img_src) > 5:
                        # Clean up URL
                        if img_src.startswith("//"):
                            img_src = "https:" + img_src
                        # Get higher resolution image
                        if "width=" in img_src:
                            img_src = img_src.split("&width=")[0] + "&width=500"
                        image_url = img_src
                        break

            products.append({"title": title, "price": price, "image": image_url})

    # Fallback: find products by links if no containers found
    if not products:
        product_links = soup.select("a[href*='/products/']")

        for link in product_links:
            title = link.get("title") or link.get_text(strip=True)
            if not title or title in seen_titles or len(title) < 3:
                continue

            seen_titles.add(title)

            # Look for price in parent elements
            price = "N/A"
            image_url = "N/A"
            parent = link.find_parent(["div", "li", "article", "section"])
            if parent:
                price_el = parent.find(string=lambda x: x and "$" in x)
                if price_el:
                    price = price_el.strip()

                # Find image in parent
                img_el = parent.select_one("img")
                if img_el:
                    img_src = img_el.get("src") or img_el.get("data-src")
                    if img_src:
                        if img_src.startswith("//"):
                            img_src = "https:" + img_src
                        image_url = img_src

            products.append({"title": title, "price": price, "image": image_url})

    return products


def has_next_page(soup, current_page):
    """Check if there's a next page."""
    # Look for next page link
    next_page = current_page + 1
    next_link = soup.select_one(f"a[href*='page={next_page}']")
    if next_link:
        return True

    # Check for "Next" button
    next_btn = soup.find("a", string=lambda x: x and "next" in x.lower() if x else False)
    return next_btn is not None


def save_to_csv(products, filename):
    """Save products to a CSV file."""
    if not products:
        print("No products to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "image"])
        writer.writeheader()
        writer.writerows(products)

    print(f"Saved {len(products)} products to {filename}")


def scrape_with_selenium(headless=True):
    """Main scraping function using Selenium."""
    all_products = []
    page = 1

    print("Starting Selenium WebDriver...")
    driver = create_driver(headless=headless)

    try:
        while page <= MAX_PAGES:
            url = f"{BASE_URL}?page={page}"
            print(f"\n{'='*50}")
            print(f"Scraping page {page}: {url}")

            html = fetch_page_selenium(driver, url)
            if not html:
                print("Failed to fetch page. Stopping.")
                break

            soup = BeautifulSoup(html, "html.parser")
            products = parse_products(soup)

            if not products:
                print("No products found on this page. Stopping.")
                break

            all_products.extend(products)
            print(f"Found {len(products)} products (Total: {len(all_products)})")

            # Print first 5 products with image info
            for p in products[:5]:
                img_status = "[IMG]" if p['image'] != "N/A" else "[NO IMG]"
                print(f"  - {p['title']}: {p['price']} {img_status}")
            if len(products) > 5:
                print(f"  ... and {len(products) - 5} more")

            if not has_next_page(soup, page):
                print("No next page found. Stopping.")
                break

            page += 1
            delay = random.uniform(2, 4)
            print(f"Waiting {delay:.1f}s before next request...")
            time.sleep(delay)

    finally:
        print("\nClosing browser...")
        driver.quit()

    return all_products


def main():
    """Entry point."""
    print("Web Scraper with Selenium (JavaScript Rendering)")
    print("=" * 50)

    # Set headless=False to see the browser in action
    products = scrape_with_selenium(headless=True)

    if products:
        save_to_csv(products, OUTPUT_FILE)
        print(f"\nScraping complete! Total: {len(products)} products")
    else:
        print("\nNo products scraped.")


if __name__ == "__main__":
    main()
