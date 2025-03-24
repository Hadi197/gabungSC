import pandas as pd
import subprocess

# File paths
data_kapal_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/data_kapal.csv'
spb_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/spb.csv'
output_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/gabung.csv'

# Execute scrape.py
subprocess.run(['python3', '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/scrape.py'])

# Execute spbphi.py
subprocess.run(['python3', '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/spbphi.py'])

# Load CSV files
data_kapal_df = pd.read_csv(data_kapal_path)
spb_df = pd.read_csv(spb_path)

# Print columns to debug
print("Columns in data_kapal_df:", data_kapal_df.columns)
print("Columns in spb_df:", spb_df.columns)

# Print the first few rows of each DataFrame to debug
print("First few rows of data_kapal_df:")
print(data_kapal_df.head())
print("First few rows of spb_df:")
print(spb_df.head())

# Select only the specified columns that exist in both DataFrames
columns_to_select_data_kapal = [
    'no_pkk_inaportnet', 'no_pkk', 'vessel_name', 
    'gt', 'loa', 'company_name', 'name_process_code', 'name_branch','departure_date'
]
columns_to_select_spb = [
    'nomor_pkk', 'nomor_spb'
]

# Ensure the columns exist in the DataFrames
selected_data_kapal = data_kapal_df[columns_to_select_data_kapal]
selected_spb = spb_df[columns_to_select_spb]

# Print the selected data to debug
print("Selected data from data_kapal_df:")
print(selected_data_kapal.head())
print("Selected data from spb_df:")
print(selected_spb.head())

# Merge dataframes using 'no_pkk_inaportnet' from data_kapal_df and 'nomor_pkk' from spb_df
merged_df = pd.merge(selected_data_kapal, selected_spb, left_on='no_pkk_inaportnet', right_on='nomor_pkk', how='inner')

# Print merged DataFrame to debug
print("Contents of merged_df:")
print(merged_df.head())

# Save merged dataframe to CSV
merged_df.to_csv(output_path, index=False)

print(f"✅ Data berhasil digabungkan dan disimpan dalam file {output_path}")
