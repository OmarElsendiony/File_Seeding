import json
import re

# Read the input JSON file
with open('files_fixes_info.json', 'r') as f:
    data = json.load(f)

# Extract priority from each record
priority_data = {}

for key, value in data.items():
    # Search for the PRIORITY line in the bug description
    match = re.search(r'PRIORITY:\s*(P\d+)', value)
    if match:
        priority = match.group(1)
        priority_data[key] = priority
    else:
        priority_data[key] = "Not found"

# Save to output JSON file
with open('priorities.json', 'w') as f:
    json.dump(priority_data, f, indent=2)

print("Priority extraction complete!")
print(json.dumps(priority_data, indent=2))