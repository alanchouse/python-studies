# Write mode ('w') overwrites the file

with open("data.txt", "w", encoding="utf-8") as f:
    f.write("First line of data.\n")



# Append mode ('a') adds text to the end

with open("data.txt", "a", encoding="utf-8") as f:
    f.write("Second line added via append mode.\n")

print("Data written and appended successfully.")