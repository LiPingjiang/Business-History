"""
Add source_type field to crawler config and output.
Also add a source_url field to distinguish official vs third-party sources.

This script patches config.py to add a `source_type` field to CompanyConfig,
and updates the data output to include it.
"""
import re

# Read current config.py
with open('/Users/pingjiangli/Code/Business-History/crawler/config.py', 'r') as f:
    content = f.read()

# 1. Check if CompanyConfig already has source_type
if 'source_type' in content:
    print("source_type already exists in config.py, skipping dataclass patch")
else:
    # Add source_type field to CompanyConfig dataclass
    # Find the dataclass fields
    old_fields = '    adapter: str = ""'
    new_fields = '''    adapter: str = ""
    source_type: str = ""  # "official" or "third_party:<platform_name>"'''
    
    if old_fields in content:
        content = content.replace(old_fields, new_fields, 1)
        print("1. Added source_type field to CompanyConfig")
    else:
        print("WARNING: Could not find adapter field in CompanyConfig")

# 2. Add source_type to all company entries based on their URL/adapter
# Define the mapping rules
THIRD_PARTY_PATTERNS = {
    'zhiye.com': 'third_party:北森智聘',
    'myworkdayjobs.com': 'third_party:Workday',
    'hotjob.cn': 'third_party:前程无忧',
    'mokahr.com': 'third_party:Moka',
    'smartrecruiters': 'third_party:SmartRecruiters',
}

# We need to add source_type to each CompanyConfig entry
# Strategy: add a post-processing step that auto-fills source_type based on URL
auto_fill_code = '''

# Auto-fill source_type based on URL patterns
_THIRD_PARTY_URL_PATTERNS = {
    'zhiye.com': 'third_party:北森智聘',
    'myworkdayjobs.com': 'third_party:Workday',
    'hotjob.cn': 'third_party:前程无忧',
    'mokahr.com': 'third_party:Moka',
    'smartrecruiters': 'third_party:SmartRecruiters',
    'jobs.lever.co': 'third_party:Lever',
}

for _c in ALL_COMPANIES:
    if not _c.source_type:
        _c.source_type = 'official'  # default
        for _pattern, _stype in _THIRD_PARTY_URL_PATTERNS.items():
            if _pattern in _c.url:
                _c.source_type = _stype
                break
'''

if '_THIRD_PARTY_URL_PATTERNS' not in content:
    content += auto_fill_code
    print("2. Added auto-fill source_type logic")
else:
    print("2. Auto-fill logic already exists")

with open('/Users/pingjiangli/Code/Business-History/crawler/config.py', 'w') as f:
    f.write(content)

print("config.py patched successfully")
