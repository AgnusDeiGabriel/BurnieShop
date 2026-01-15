import csv
import os

# Configuration
CSV_FILE = "products.csv"
IMAGES_FOLDER = "images"
OUTPUT_FILE = "gallery.html"


def get_category(title):
    """Determine category from product title."""
    title_lower = title.lower()
    if 'wig' in title_lower:
        return 'wig'
    elif 'closure' in title_lower:
        return 'closure'
    elif 'frontal' in title_lower:
        return 'frontal'
    elif 'straight' in title_lower:
        return 'straight'
    elif 'wave' in title_lower or 'wavy' in title_lower:
        return 'wave'
    elif 'curly' in title_lower or 'curl' in title_lower:
        return 'curly'
    else:
        return 'bundle'


def generate_html(products):
    """Generate the gallery HTML."""

    # Generate product cards
    product_cards = []
    for i, product in enumerate(products, 1):
        title = product['title']
        category = get_category(title)

        # Find matching image file
        image_files = [f for f in os.listdir(IMAGES_FOLDER) if f.startswith(f"{i:04d}_")]
        if image_files:
            image_path = f"images/{image_files[0]}"
        else:
            image_path = "https://via.placeholder.com/400x400?text=No+Image"

        card = f'''
    <!-- Product {i} -->
    <div class="product-card group" data-category="{category}" data-title="{title.lower()}">
      <div class="relative overflow-hidden rounded-t-2xl">
        <img src="{image_path}" alt="{title}" class="w-full h-48 sm:h-56 md:h-64 object-cover group-hover:scale-110 transition-transform duration-500" loading="lazy" onerror="this.src='https://via.placeholder.com/400x400?text=Image+Not+Found'">
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <div class="absolute bottom-4 left-4 right-4">
            <button onclick="openModal({i})" class="w-full bg-white/90 backdrop-blur-sm text-black py-2 rounded-lg font-semibold hover:bg-gold transition">
              Quick View
            </button>
          </div>
        </div>
      </div>
      <div class="bg-white p-4 rounded-b-2xl">
        <h3 class="font-bold text-sm sm:text-base line-clamp-2 h-12 mb-2">{title}</h3>
        <div class="flex items-center justify-between">
          <span class="text-xs text-gray-500 uppercase tracking-wide">{category}</span>
          <button onclick="openModal({i})" class="text-gold hover:text-black transition text-sm font-semibold">Details →</button>
        </div>
      </div>
    </div>'''
        product_cards.append(card)

    # Generate modal data
    modal_data = []
    for i, product in enumerate(products, 1):
        title = product['title']
        price = product.get('price', 'N/A')
        category = get_category(title)

        image_files = [f for f in os.listdir(IMAGES_FOLDER) if f.startswith(f"{i:04d}_")]
        if image_files:
            image_path = f"images/{image_files[0]}"
        else:
            image_path = "https://via.placeholder.com/400x400?text=No+Image"

        modal_data.append(f'{{ id: {i}, title: "{title.replace('"', '\\"')}", image: "{image_path}", category: "{category}" }}')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hair Gallery - BURNIE-SHOP</title>
  <link rel="shortcut icon" href="./fille.jpeg">

  <!-- Tailwind CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Tailwind config -->
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            primary: '#000000',
            gold: '#d4af37',
            'gold-dark': '#b8960c'
          }}
        }}
      }}
    }}
  </script>

  <style>
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .product-card {{
      transition: all 0.3s ease;
    }}

    .product-card:hover {{
      transform: translateY(-8px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }}

    .filter-btn.active {{
      background-color: #000;
      color: #fff;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
    }}

    ::-webkit-scrollbar-track {{
      background: #f1f1f1;
    }}

    ::-webkit-scrollbar-thumb {{
      background: #d4af37;
      border-radius: 4px;
    }}

    /* Loading animation */
    @keyframes shimmer {{
      0% {{ background-position: -200% 0; }}
      100% {{ background-position: 200% 0; }}
    }}

    .loading {{
      background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }}
  </style>
</head>
<body class="bg-gray-100 text-gray-900">

<!-- NAVBAR -->
<nav class="flex justify-between items-center px-4 md:px-8 py-4 bg-white shadow-md sticky top-0 z-50">
  <div class="flex items-center gap-4">
    <button onclick="toggleSidebar()" class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
    </button>
    <a href="index.html" class="text-xl md:text-2xl font-bold tracking-wide">BURNIE<span class="text-gold">SHOP</span></a>
  </div>

  <div class="hidden md:flex gap-6 items-center">
    <div class="relative">
      <input type="text" id="searchInput" placeholder="Search products..." class="w-64 px-4 py-2 pl-10 bg-gray-100 border-0 rounded-full focus:outline-none focus:ring-2 focus:ring-gold" onkeyup="filterProducts()">
      <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
    </div>
    <a href="index.html" class="font-semibold hover:text-gold transition">Home</a>
    <a href="gallery.html" class="font-semibold text-gold">Gallery</a>
    <a href="contact.html" class="font-semibold hover:text-gold transition">Contact</a>
  </div>
</nav>

<!-- MOBILE SIDEBAR -->
<div id="sidebarOverlay" class="fixed inset-0 bg-black/50 z-40 hidden" onclick="closeSidebar()"></div>
<div id="sidebar" class="fixed left-0 top-0 h-full w-80 bg-white shadow-2xl z-50 transform -translate-x-full transition-transform duration-300">
  <div class="p-6">
    <button onclick="closeSidebar()" class="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full transition">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
    </button>
    <h2 class="text-xl font-bold mb-6">Menu</h2>

    <div class="mb-6">
      <input type="text" id="searchInputMobile" placeholder="Search products..." class="w-full px-4 py-3 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-gold" onkeyup="filterProducts()">
    </div>

    <nav class="space-y-2">
      <a href="index.html" class="block py-3 px-4 rounded-lg hover:bg-gray-100 transition font-medium">Home</a>
      <a href="gallery.html" class="block py-3 px-4 rounded-lg bg-gold text-black font-medium">Gallery</a>
      <a href="contact.html" class="block py-3 px-4 rounded-lg hover:bg-gray-100 transition font-medium">Contact</a>
    </nav>

    <div class="mt-8 pt-6 border-t">
      <h3 class="font-semibold mb-4">Follow Us</h3>
      <div class="flex gap-4">
        <a href="https://www.facebook.com/share/1AkCdm1ixj/" target="_blank" class="p-2 bg-gray-100 rounded-full hover:bg-gold hover:text-white transition">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
        </a>
        <a href="https://www.instagram.com/burnie_shop" target="_blank" class="p-2 bg-gray-100 rounded-full hover:bg-gold hover:text-white transition">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
        </a>
        <a href="https://www.tiktok.com/@burnie_shop" target="_blank" class="p-2 bg-gray-100 rounded-full hover:bg-gold hover:text-white transition">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
        </a>
      </div>
    </div>
  </div>
</div>

<!-- HERO SECTION -->
<section class="relative bg-gradient-to-br from-black via-gray-900 to-black text-white px-4 md:px-16 py-16 md:py-24 overflow-hidden">
  <div class="absolute inset-0 opacity-20">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,#d4af37_0%,transparent_50%)]"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,#d4af37_0%,transparent_40%)]"></div>
  </div>
  <div class="relative z-10 max-w-4xl mx-auto text-center">
    <span class="inline-block px-4 py-1 bg-gold/20 text-gold rounded-full text-sm font-semibold mb-6">Premium Collection</span>
    <h1 class="text-4xl md:text-6xl font-bold mb-6 leading-tight">Discover Your <span class="text-gold">Perfect Style</span></h1>
    <p class="text-lg md:text-xl text-gray-300 mb-8 max-w-2xl mx-auto">Explore our exclusive collection of {len(products)} premium hair products. 100% virgin hair for the perfect look.</p>
    <div class="flex flex-wrap justify-center gap-4">
      <div class="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full">
        <span class="text-2xl font-bold text-gold">{len(products)}</span>
        <span class="text-sm text-gray-300 ml-2">Products</span>
      </div>
      <div class="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full">
        <span class="text-2xl font-bold text-gold">100%</span>
        <span class="text-sm text-gray-300 ml-2">Virgin Hair</span>
      </div>
      <div class="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full">
        <span class="text-2xl font-bold text-gold">Premium</span>
        <span class="text-sm text-gray-300 ml-2">Quality</span>
      </div>
    </div>
  </div>
</section>

<!-- FILTER SECTION -->
<section class="sticky top-16 z-40 bg-white shadow-sm px-4 md:px-8 py-4">
  <div class="max-w-7xl mx-auto">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex flex-wrap gap-2">
        <button onclick="setFilter('all')" class="filter-btn active px-4 py-2 rounded-full text-sm font-semibold border-2 border-black transition hover:bg-black hover:text-white">All</button>
        <button onclick="setFilter('bundle')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Bundles</button>
        <button onclick="setFilter('wig')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Wigs</button>
        <button onclick="setFilter('closure')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Closures</button>
        <button onclick="setFilter('frontal')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Frontals</button>
        <button onclick="setFilter('straight')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Straight</button>
        <button onclick="setFilter('wave')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Wave</button>
        <button onclick="setFilter('curly')" class="filter-btn px-4 py-2 rounded-full text-sm font-semibold border-2 border-gray-300 transition hover:border-black">Curly</button>
      </div>
      <div class="flex items-center gap-4">
        <select id="sortSelect" onchange="sortProducts()" class="px-4 py-2 bg-gray-100 rounded-lg border-0 focus:ring-2 focus:ring-gold text-sm">
          <option value="default">Sort by</option>
          <option value="name">Name: A-Z</option>
        </select>
        <span id="productCount" class="text-sm text-gray-500">{len(products)} products</span>
      </div>
    </div>
  </div>
</section>

<!-- PRODUCTS GRID -->
<section class="px-4 md:px-8 py-8 md:py-12">
  <div class="max-w-7xl mx-auto">
    <div id="productsGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
      {"".join(product_cards)}
    </div>

    <!-- No Results Message -->
    <div id="noResults" class="hidden text-center py-16">
      <svg class="w-24 h-24 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <h3 class="text-xl font-bold text-gray-600 mb-2">No products found</h3>
      <p class="text-gray-500">Try adjusting your search or filter criteria</p>
      <button onclick="resetFilters()" class="mt-4 px-6 py-2 bg-gold text-black rounded-full font-semibold hover:bg-gold-dark transition">Reset Filters</button>
    </div>
  </div>
</section>

<!-- CTA SECTION -->
<section class="bg-gradient-to-r from-gold via-yellow-500 to-gold text-black px-4 md:px-16 py-12 md:py-16">
  <div class="max-w-4xl mx-auto text-center">
    <h2 class="text-3xl md:text-4xl font-bold mb-4">Ready to Transform Your Look?</h2>
    <p class="text-lg mb-8 opacity-80">Contact us today for personalized recommendations and exclusive deals</p>
    <a href="contact.html" class="inline-block bg-black text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-800 hover:scale-105 transition-all shadow-lg">
      Contact Us Now
    </a>
  </div>
</section>

<!-- FOOTER -->
<footer class="bg-gray-900 text-white py-12 px-4">
  <div class="max-w-6xl mx-auto">
    <div class="grid md:grid-cols-3 gap-8 mb-8">
      <div>
        <h3 class="text-2xl font-bold mb-4">BURNIE<span class="text-gold">SHOP</span></h3>
        <p class="text-gray-400">Premium quality hair products for the perfect look you deserve.</p>
      </div>
      <div>
        <h4 class="font-bold mb-4">Quick Links</h4>
        <nav class="space-y-2">
          <a href="index.html" class="block text-gray-400 hover:text-gold transition">Home</a>
          <a href="gallery.html" class="block text-gray-400 hover:text-gold transition">Gallery</a>
          <a href="contact.html" class="block text-gray-400 hover:text-gold transition">Contact</a>
        </nav>
      </div>
      <div>
        <h4 class="font-bold mb-4">Follow Us</h4>
        <div class="flex gap-4">
          <a href="https://www.facebook.com/share/1AkCdm1ixj/" target="_blank" class="p-3 bg-gray-800 rounded-full hover:bg-gold hover:text-black transition">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="https://www.instagram.com/burnie_shop" target="_blank" class="p-3 bg-gray-800 rounded-full hover:bg-gold hover:text-black transition">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          </a>
          <a href="https://www.tiktok.com/@burnie_shop" target="_blank" class="p-3 bg-gray-800 rounded-full hover:bg-gold hover:text-black transition">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
          </a>
        </div>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-center text-gray-500">
      <p>&copy; 2026 BURNIE-SHOP. All rights reserved.</p>
    </div>
  </div>
</footer>

<!-- MODAL -->
<div id="modal" class="hidden fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
  <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden shadow-2xl">
    <div class="relative">
      <button onclick="closeModal()" class="absolute top-4 right-4 z-10 p-2 bg-white/90 rounded-full shadow-lg hover:bg-gray-100 transition">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
      <img id="modalImage" src="" class="w-full h-64 sm:h-80 object-cover" alt="">
    </div>
    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <div>
          <span id="modalCategory" class="text-xs text-gold uppercase tracking-wide font-semibold"></span>
          <h2 id="modalTitle" class="text-xl sm:text-2xl font-bold mt-1"></h2>
        </div>
      </div>
      <div class="flex gap-3">
        <a href="contact.html" class="flex-1 bg-black text-white py-3 rounded-xl font-bold text-center hover:bg-gray-800 transition">
          Contact for Purchase
        </a>
        <button onclick="closeModal()" class="px-6 py-3 border-2 border-gray-200 rounded-xl font-semibold hover:bg-gray-100 transition">
          Close
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Back to Top Button -->
<button id="backToTop" onclick="scrollToTop()" class="fixed bottom-6 right-6 p-3 bg-gold text-black rounded-full shadow-lg opacity-0 invisible transition-all hover:bg-gold-dark hover:scale-110">
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>
</button>

<!-- JAVASCRIPT -->
<script>
  // Product data
  const products = [
    {",".join(modal_data)}
  ];

  let currentFilter = 'all';
  let currentSearch = '';

  // Filter products by category
  function setFilter(category) {{
    currentFilter = category;

    // Update button styles
    document.querySelectorAll('.filter-btn').forEach(btn => {{
      btn.classList.remove('active', 'bg-black', 'text-white', 'border-black');
      btn.classList.add('border-gray-300');
    }});
    event.target.classList.add('active', 'bg-black', 'text-white', 'border-black');
    event.target.classList.remove('border-gray-300');

    applyFilters();
  }}

  // Search products
  function filterProducts() {{
    const desktopSearch = document.getElementById('searchInput')?.value || '';
    const mobileSearch = document.getElementById('searchInputMobile')?.value || '';
    currentSearch = (desktopSearch || mobileSearch).toLowerCase().trim();

    // Sync inputs
    if (document.getElementById('searchInput')) document.getElementById('searchInput').value = currentSearch;
    if (document.getElementById('searchInputMobile')) document.getElementById('searchInputMobile').value = currentSearch;

    applyFilters();
  }}

  // Apply all filters
  function applyFilters() {{
    const cards = document.querySelectorAll('.product-card');
    let visibleCount = 0;

    cards.forEach(card => {{
      const category = card.dataset.category;
      const title = card.dataset.title;

      const matchesCategory = currentFilter === 'all' || category === currentFilter;
      const matchesSearch = currentSearch === '' || title.includes(currentSearch);

      if (matchesCategory && matchesSearch) {{
        card.style.display = 'block';
        card.style.opacity = '1';
        visibleCount++;
      }} else {{
        card.style.opacity = '0';
        setTimeout(() => card.style.display = 'none', 200);
      }}
    }});

    // Update count and show/hide no results
    document.getElementById('productCount').textContent = visibleCount + ' products';
    document.getElementById('noResults').classList.toggle('hidden', visibleCount > 0);
  }}

  // Sort products
  function sortProducts() {{
    const sortBy = document.getElementById('sortSelect').value;
    const grid = document.getElementById('productsGrid');
    const cards = Array.from(grid.querySelectorAll('.product-card'));

    cards.sort((a, b) => {{
      if (sortBy === 'name') {{
        return a.dataset.title.localeCompare(b.dataset.title);
      }}
      return 0;
    }});

    cards.forEach(card => grid.appendChild(card));
  }}

  // Reset filters
  function resetFilters() {{
    currentFilter = 'all';
    currentSearch = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('searchInputMobile').value = '';
    document.getElementById('sortSelect').value = 'default';

    document.querySelectorAll('.filter-btn').forEach((btn, i) => {{
      btn.classList.remove('active', 'bg-black', 'text-white', 'border-black');
      btn.classList.add('border-gray-300');
      if (i === 0) {{
        btn.classList.add('active', 'bg-black', 'text-white', 'border-black');
        btn.classList.remove('border-gray-300');
      }}
    }});

    applyFilters();
  }}

  // Modal functions
  function openModal(productId) {{
    const product = products.find(p => p.id === productId);
    if (!product) return;

    document.getElementById('modalImage').src = product.image;
    document.getElementById('modalTitle').textContent = product.title;
    document.getElementById('modalCategory').textContent = product.category;
    document.getElementById('modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }}

  function closeModal() {{
    document.getElementById('modal').classList.add('hidden');
    document.body.style.overflow = '';
  }}

  // Close modal on backdrop click
  document.getElementById('modal')?.addEventListener('click', function(e) {{
    if (e.target === this) closeModal();
  }});

  // Close modal on Escape key
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeModal();
  }});

  // Sidebar functions
  function toggleSidebar() {{
    document.getElementById('sidebar').classList.toggle('-translate-x-full');
    document.getElementById('sidebarOverlay').classList.toggle('hidden');
  }}

  function closeSidebar() {{
    document.getElementById('sidebar').classList.add('-translate-x-full');
    document.getElementById('sidebarOverlay').classList.add('hidden');
  }}

  // Back to top
  function scrollToTop() {{
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}

  // Show/hide back to top button
  window.addEventListener('scroll', function() {{
    const btn = document.getElementById('backToTop');
    if (window.scrollY > 500) {{
      btn.classList.remove('opacity-0', 'invisible');
      btn.classList.add('opacity-100', 'visible');
    }} else {{
      btn.classList.add('opacity-0', 'invisible');
      btn.classList.remove('opacity-100', 'visible');
    }}
  }});
</script>

</body>
</html>'''

    return html


def main():
    # Read products from CSV
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        products = list(reader)

    print(f"Loaded {len(products)} products from {CSV_FILE}")

    # Generate HTML
    html = generate_html(products)

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE} successfully!")
    print(f"Open {OUTPUT_FILE} in a browser to view the gallery.")


if __name__ == "__main__":
    main()
