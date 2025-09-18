# Config.py
import os

# Go up one level, then into pics/
IMAGE_NAME = os.path.join("..", "pics", "backgroundpage1.jpg")

# Debug
print(f"🔍 Looking for: {os.path.abspath(IMAGE_NAME)}")