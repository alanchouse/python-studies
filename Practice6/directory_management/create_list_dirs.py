import os

# Creating nested directories
path = "nested/level1/level2"
os.makedirs(path, exist_ok=True)
print(f"Directories created: {path}")

# Listing current directory content
print("Current directory content:", os.listdir("."))