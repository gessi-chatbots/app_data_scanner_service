import json

# Read the first JSON file
with open('data/scan-1year-reviews/microblogging-review-set.json', 'r') as file1:
    data1 = json.load(file1)

# Read the second JSON file
with open('data/scan-1year-reviews/microblogging-apps-extended.json', 'r') as file2:
    data2 = json.load(file2)

# Create a dictionary to store the merged data
merged_data = {}

# Merge data from the first JSON file
for item in data1:
    package_name = item['package_name']
    if package_name not in merged_data:
        merged_data[package_name] = item
    else:
        # Merge 'reviews' array while ensuring unique 'reviewId'
        existing_reviews = {review['reviewId']: review for review in merged_data[package_name]['reviews']}
        for review in item['reviews']:
            if review['reviewId'] not in existing_reviews:
                existing_reviews[review['reviewId']] = review
                merged_data[package_name]['reviews'].append(review)

# Merge data from the second JSON file
for item in data2:
    package_name = item['package_name']
    if package_name not in merged_data:
        merged_data[package_name] = item
    else:
        # Merge 'reviews' array while ensuring unique 'reviewId'
        existing_reviews = {review['reviewId']: review for review in merged_data[package_name]['reviews']}
        for review in item['reviews']:
            if review['reviewId'] not in existing_reviews:
                existing_reviews[review['reviewId']] = review
                merged_data[package_name]['reviews'].append(review)

# Convert the merged data back to a list
merged_list = list(merged_data.values())

# Write the merged data to a new JSON file
with open('data/scan-1year-reviews/microblogging-apps-merged.json', 'w') as merged_file:
    json.dump(merged_list, merged_file, indent=2)
