import pandas as pd
import subprocess

# Execute inaport.py
subprocess.run(["python", "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/inaport.py"])

# Execute scrape.py
subprocess.run(["python", "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/scrape.py"])

# File paths
hasil_scraping_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/hasil_scraping.csv'
inaport_all_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/inaport_all.csv'
output_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/gabung.csv'

# Load CSV files
hasil_scraping_df = pd.read_csv(hasil_scraping_path)
inaport_all_df = pd.read_csv(inaport_all_path)

# Print columns to debug
print("Columns in hasil_scraping_df:", hasil_scraping_df.columns)
print("Columns in inaport_all_df:", inaport_all_df.columns)

# Print the first few rows of each DataFrame to debug
print("First few rows of hasil_scraping_df:")
print(hasil_scraping_df.head())
print("First few rows of inaport_all_df:")
print(inaport_all_df.head())

# Filter rows where 'gt' is greater than or equal to 500
filtered_hasil_scraping_df = hasil_scraping_df[hasil_scraping_df['gt'] >= 500]

# Select only the specified columns that exist in both DataFrames
columns_to_select_hasil_scraping = [
    'no_pkk_inaportnet', 'no_pkk', 'arrive_date', 'vessel_name', 
    'gt', 'loa', 'company_name', 'name_process_code', 'name_branch'
]
columns_to_select_inaport_all = [
    'nomor_pkk', 'no_spb', 'waktu_spb'
]

# Ensure the columns exist in the DataFrames
selected_hasil_scraping = filtered_hasil_scraping_df[columns_to_select_hasil_scraping]
selected_inaport_all = inaport_all_df[columns_to_select_inaport_all]

# Print the selected data to debug
print("Selected data from hasil_scraping_df:")
print(selected_hasil_scraping.head())
print("Selected data from inaport_all_df:")
print(selected_inaport_all.head())

# Merge dataframes using 'no_pkk_inaportnet' from hasil_scraping_df and 'nomor_pkk' from inaport_all_df
merged_df = pd.merge(selected_hasil_scraping, selected_inaport_all, left_on='no_pkk_inaportnet', right_on='nomor_pkk', how='inner')

# Add Periode_SPB column with formatted waktu_spb
merged_df['Periode_SPB'] = pd.to_datetime(merged_df['waktu_spb']).dt.strftime('%Y-%m')

# Print merged DataFrame to debug
print("Contents of merged_df:")
print(merged_df.head())

# Save merged dataframe to CSV
merged_df.to_csv(output_path, index=False)

print(f"✅ Data berhasil digabungkan dan disimpan dalam file {output_path}")
