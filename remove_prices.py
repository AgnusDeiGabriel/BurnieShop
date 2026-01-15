import re

with open('gallery.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the price div
pattern = r'<div class="absolute top-3 right-3">\s*<span class="bg-gold text-black px-3 py-1 rounded-full text-sm font-bold shadow-lg">[^<]*</span>\s*</div>'

# Remove all matches
new_content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Prices removed from gallery.html")
