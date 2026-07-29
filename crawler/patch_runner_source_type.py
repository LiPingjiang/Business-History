"""
Patch the runner.py to inject source_type from company config into each job after crawling.
This is the cleanest approach - set source_type at the runner level after jobs are returned.
"""

with open('/Users/pingjiangli/Code/Business-History/crawler/runner.py', 'r') as f:
    content = f.read()

# After jobs are crawled, inject source_type from company config
old_code = '''        result = adapter.crawl(company)
        results.append(result)'''

new_code = '''        result = adapter.crawl(company)
        # Inject source_type from company config into each job
        if result.success and result.jobs:
            for job in result.jobs:
                job.source_type = company.source_type
        results.append(result)'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("runner.py patched: source_type injection added")
else:
    print("ERROR: target code not found in runner.py")
    import sys; sys.exit(1)

with open('/Users/pingjiangli/Code/Business-History/crawler/runner.py', 'w') as f:
    f.write(content)

print("Done!")
