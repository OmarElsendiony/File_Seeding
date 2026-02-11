import json

# Read input JSON file
with open("priorities.json", "r") as f:
    data = json.load(f)

output = {}
counter = 1

# For each file path, assign two sequential numeric keys
for _, value in data.items():
    output[str(counter)] = value
    counter += 1
    output[str(counter)] = value
    counter += 1

# Print result
print(json.dumps(output, indent=2))

# Optional: write to file
with open("priorities_with_ids.json", "w") as f:
    json.dump(output, f, indent=2)
