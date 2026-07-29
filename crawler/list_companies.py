#!/usr/bin/env python3
"""List all companies by adapter and crawl status."""
from config import ALL_COMPANIES
from collections import defaultdict

cats = defaultdict(list)
for c in ALL_COMPANIES:
    cats[c.adapter].append(c.name)

print(f"Total: {len(ALL_COMPANIES)} companies\n")
for k, v in sorted(cats.items(), key=lambda x: -len(x[1])):
    print(f"[{k}] ({len(v)}): {', '.join(v)}")
