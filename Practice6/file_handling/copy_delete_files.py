import shutil
import os

# Create a dummy file for testing 

open("test_to_copy.txt", "w").close()

# Copying the file

shutil.copy("test_to_copy.txt", "test_backup.txt")
print("File copied to test_backup.txt")

# Safe deletion

if os.path.exists("test_to_copy.txt"):
    os.remove("test_to_copy.txt")
    print("Original file deleted successfully.")