"""
Script to make dashboard analytics cards compact
"""
import re

# Read the file
with open('sirms/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace analytics card padding and styling
# Pattern: rounded-xl p-6 border-l-4 ... cursor-pointer
pattern = r'(class="bg-gradient-to-r[^"]*rounded-xl p-6 border-l-4[^"]*cursor-pointer[^"]*")'
replacement = lambda m: m.group(0).replace('rounded-xl p-6', 'rounded-lg analytics-card-compact')

content = re.sub(pattern, replacement, content)

# Also reduce text-3xl to text-2xl for counters
content = content.replace('text-3xl font-bold', 'text-2xl font-bold')

# Reduce icon sizes
content = content.replace('text-2xl"></i>', 'text-xl"></i>')

# Write back
with open('sirms/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Dashboard compacted successfully!")
print("Changes made:")
print("- Analytics cards: p-6 → analytics-card-compact")
print("- Counter text: text-3xl → text-2xl")
print("- Icons: text-2xl → text-xl")
