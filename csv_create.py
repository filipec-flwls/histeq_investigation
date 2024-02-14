import csv
import os

data = ["']

output_directory = 'output'
file_name = 'shot_context.csv'
output_path = os.path.join(output_directory, file_name)

# Add a header to the CSV file
header = ['ShotName']
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for item in data:
        writer.writerow([item])

print(f'CSV file "{output_path}" created successfully.')
