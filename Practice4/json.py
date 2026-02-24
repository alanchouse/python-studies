# Convert from JSON to Python:

import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])

# Convert Python objects into JSON strings, and print the values:

import json

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

import json

# --- Convert from JSON to Python (json.loads) ---

# Example 1
json_data1 = '{"brand": "Nvidia", "model": "RTX 4070", "vram": 12}'
python_dict1 = json.loads(json_data1)
print(python_dict1["model"])

# Example 2
json_data2 = '{"game": "CS2", "platform": "FACEIT", "rank": 10}'
python_dict2 = json.loads(json_data2)
print(python_dict2["rank"])

# Example 3
json_data3 = '{"cpu": "Ryzen 7 7800X3D", "cores": 8, "threads": 16}'
python_dict3 = json.loads(json_data3)
print(python_dict3["cpu"])

# Example 4
json_data4 = '{"city": "Almaty", "temp": -5, "is_snowing": true}'
python_dict4 = json.loads(json_data4)
print(python_dict4["is_snowing"])

# Example 5
json_data5 = '{"user": "Kurban", "status": "online", "friends_count": 5}'
python_dict5 = json.loads(json_data5)
print(python_dict5["user"])


# --- Convert Python objects into JSON strings (json.dumps) ---

# Example 1 (Dictionaries)
print(json.dumps({"item": "Keyboard", "type": "Mechanical"}))
print(json.dumps({"mouse": "Logitech", "dpi": 800}))
print(json.dumps({"monitor": "Zowie", "hz": 240}))
print(json.dumps({"case": "Lian Li", "color": "Black"}))
print(json.dumps({"psu": "750W", "gold": True}))

# Example 2 (Lists / Arrays)
print(json.dumps(["Python", "C++", "JavaScript"]))
print(json.dumps([144, 165, 240, 360]))
print(json.dumps(["Dust 2", "Mirage", "Inferno"]))
print(json.dumps([True, False, True]))
print(json.dumps([]))

# Example 3 (Strings and Numbers)
print(json.dumps("Hello Python"))
print(json.dumps(1000))
print(json.dumps(99.9))
print(json.dumps("Gamer"))
print(json.dumps(7800))

# Example 4 (Booleans and None)
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))
print(json.dumps(1 > 0))
print(json.dumps(5 < 2))

# Example 5 (Nested structures)
print(json.dumps({"player": {"name": "Alex", "level": 50}}))
print(json.dumps([{"id": 1}, {"id": 2}, {"id": 3}]))
print(json.dumps({"tags": ["pc", "build", "gaming"]}))
print(json.dumps({"active": True, "details": None}))
print(json.dumps({"points": [10, 20, 30], "total": 60}))

