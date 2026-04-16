import json

# Open the data file and load JSON content

with open('sample-data.json') as f:
    data = json.load(f)

# Print the table headers

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50, "-" * 20, "-" * 7, "-" * 6)

# Iterate through the JSON data and print each interface

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    print(f"{attr['dn']:<50} {attr['descr']:<20} {attr['speed']:<7} {attr['mtu']:<6}")