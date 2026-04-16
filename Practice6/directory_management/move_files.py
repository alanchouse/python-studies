import shutil
import os
from pathlib import Path

# Create a file and a destination folder for testing
Path("move_me.txt").touch()
os.makedirs("destination", exist_ok=True)

# Moving the file
shutil.move("move_me.txt", "destination/moved_file.txt")
print("File moved to the destination folder successfully.")