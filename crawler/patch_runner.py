import re
with open('/Users/pingjiangli/Code/Business-History/crawler/runner.py','r') as f:
    content=f.read()
old = '    # 过滤企业\n    companies = ALL_COMPANIES'
new = '    # 过滤企业（跳过dead/suspended站点）\n    companies = [c for c in ALL_COMPANIES if c.status == "active"]'
content = content.replace(old, new)
# Also update the list command to show source_type and status
old_list = '        for i, c in enumerate(ALL_COMPANIES, 1):\n            table.add_row(str(i), c.name, c.adapter, c.url[:60])'
new_list = '        for i, c in enumerate(ALL_COMPANIES, 1):\n            st = c.source_type[:20] if c.source_type else ""\n            table.add_row(str(i), c.name, c.adapter, c.url[:50], st, c.status)'
content = content.replace(old_list, new_list)
# Add columns for source_type and status in list table
old_cols = '        table.add_column("#", justify="right")\n        table.add_column("企业", style="cyan")\n        table.add_column("Adapter")\n        table.add_column("URL")'
new_cols = '        table.add_column("#", justify="right")\n        table.add_column("企业", style="cyan")\n        table.add_column("Adapter")\n        table.add_column("URL")\n        table.add_column("来源")\n        table.add_column("状态")'
content = content.replace(old_cols, new_cols)
with open('/Users/pingjiangli/Code/Business-History/crawler/runner.py','w') as f:
    f.write(content)
print('runner.py updated successfully')
