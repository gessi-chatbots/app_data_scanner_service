import json

# Replace 'your_file.json' with the path to your JSON file
file_path = 'data/scanApps/com.microsoft.copilot.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Count items in 'reviews' array
if 'reviews' in data[0]:
    reviews_count = len(data[0]['reviews'])
    print(f"Number of items in 'reviews': {reviews_count}")
else:
    print("'reviews' key not found in the JSON file.")
