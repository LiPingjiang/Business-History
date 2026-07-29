"""Backfill source_type into existing JSON data based on source_adapter and company name."""
import json
from pathlib import Path

DATA_DIR = Path('/Users/pingjiangli/Code/Business-History/crawler/data')

# Mapping from source_adapter to source_type
ADAPTER_TO_SOURCE_TYPE = {
    'workday': 'third_party:Workday',
    'zhiye': 'third_party:北森智聘',
    'zhiye_pw': 'third_party:北森智聘',
    'beisen': 'third_party:北森智聘',
    'hotjob_json': 'third_party:前程无忧',
    'hotjob_pw': 'third_party:前程无忧',
    'mokahr': 'third_party:Moka',
    'smartrecruiters': 'third_party:SmartRecruiters',
    'jibe': 'third_party:Jibe/Google',
    'phenom': 'third_party:Phenom',
    # Official site adapters
    'amazon': 'official',
    'microsoft': 'official',
    'siemens': 'official',
    'bmw': 'official',
    'astrazeneca': 'official',
    'citicbank': 'official',
    'spdb': 'official',
    'cmbc': 'official',
    'custom_pw': 'official',
}

# Companies with empty source_adapter that are official
OFFICIAL_COMPANIES = {'浦发银行', '民生银行', '中信银行', '智源研究院', '苏商银行', '中信百信银行'}
# Actually 智源/苏商/中信百信 are on Moka
MOKA_COMPANIES = {'智源研究院', '苏商银行', '中信百信银行'}

for json_file in sorted(DATA_DIR.glob('202*.json')):
    data = json.loads(json_file.read_text())
    jobs = data if isinstance(data, list) else data.get('jobs', [])
    
    updated = 0
    for job in jobs:
        if job.get('source_type'):
            continue  # already has source_type
        
        adapter = job.get('source_adapter', '')
        company = job.get('company', '')
        
        if adapter and adapter in ADAPTER_TO_SOURCE_TYPE:
            job['source_type'] = ADAPTER_TO_SOURCE_TYPE[adapter]
            updated += 1
        elif company in MOKA_COMPANIES:
            job['source_type'] = 'third_party:Moka'
            updated += 1
        elif company in OFFICIAL_COMPANIES:
            job['source_type'] = 'official'
            updated += 1
    
    if updated > 0:
        if isinstance(data, list):
            json_file.write_text(json.dumps(jobs, ensure_ascii=False, indent=2))
        else:
            data['jobs'] = jobs
            json_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        print(f"  {json_file.name}: backfilled {updated} jobs")

print("\nDone! source_type backfill complete.")
