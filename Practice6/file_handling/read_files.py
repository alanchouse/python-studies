# Create a sample file programmatically

with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Hello Python!\nThis is a test file for Practice 6.")


# Reading the entire file

print("--- Reading entire file ---")
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)


# Reading line by line

print("\n--- Reading line by line ---")
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(f"Line content: {line.strip()}")