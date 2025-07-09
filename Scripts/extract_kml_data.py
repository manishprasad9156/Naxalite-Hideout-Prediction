import os
import xml.etree.ElementTree as ET
import pandas as pd

# Step 1: Define relative path to your Raw folder
base_path = os.path.join("..", "Data", "Raw")  # From 'Scripts/' folder, go to '../Data/Raw'

# Step 2: Link each file to its time period for labeling
files_info = {
    "kml_Rank=szcm_startDate=2025-06-01_endDate=2025-06-10_legend=Name[1].xml": "2025-06-01_to_2025-06-10",
    "kml_Rank=szcm_startDate=2025-06-11_endDate=2025-06-20_legend=Name[1].xml": "2025-06-11_to_2025-06-20",
    "kml_Rank=szcm_startDate=2025-06-21_endDate=2025-06-30_legend=Name[1].xml": "2025-06-21_to_2025-06-30",
    "kml_Rank=szcm_startDate=2025-06-30_endDate=2025-07-08_legend=Name[1].xml": "2025-06-30_to_2025-07-08"
}

# Step 3: Prepare a list to collect the extracted data
data = []

# Step 4: Loop over each KML file and extract info
for file_name, date_range in files_info.items():
    path = os.path.join(base_path, file_name)
    
    tree = ET.parse(path)  # Load XML
    root = tree.getroot()  # Get root element

    # Define XML namespace for KML
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    # Step 5: Loop through every hideout (Placemark)
    for placemark in root.findall('.//kml:Placemark', ns):
        name = placemark.find('kml:name', ns).text
        coords_text = placemark.find('.//kml:coordinates', ns).text.strip()
        lon, lat = map(float, coords_text.split(',')[:2])  # Convert "lon,lat" string to floats

        data.append({
            'name': name,
            'latitude': lat,
            'longitude': lon,
            'date_range': date_range
        })

# Step 6: Convert all collected data to a DataFrame
df = pd.DataFrame(data)

# Step 7: Save as CSV (relative path to ../Data/)
output_path = os.path.join("..", "Data", "naxal_hideouts_combined.csv")
df.to_csv(output_path, index=False)

# Step 8: Preview
print("✅ CSV saved at:", output_path)
print(df.head())
