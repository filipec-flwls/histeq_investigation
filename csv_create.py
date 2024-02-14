import csv
import os

data = ["ufof01_ep01_pt15_0260","ufof01_ep01_pt15_0270","ufof01_ep01_pt17_0690","ufof01_ep01_pt18_0050","ufof01_ep01_pt18_0060","ufof01_ep01_pt18_0180",'ufof01_ep01_pt18_0190', "ufof01_ep01_pt18_0240", 'ufof01_ep01_pt40_0060', 'ufof01_ep01_pt47_0030','ufof01_ep01_pt49_0190', 'ufof01_ep01_pt49_0570', 'ufof01_ep01_pt55_0050', 'ufof01_ep01_pt56_0070', 'ufof01_ep01_pt63_0560']

output_directory = '/Volumes/shared/vfx/filipe.correia/pulls/Hist_EQ/csv'
file_name = 'shot_context2.csv'
output_path = os.path.join(output_directory, file_name)

# Add a header to the CSV file
header = ['ShotName']
with open(output_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for item in data:
        writer.writerow([item])

print(f'CSV file "{output_path}" created successfully.')
