import pandas as pd
import subprocess

# File paths
hasil_scraping_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/hasil_scraping.csv'
monitoring_data_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/monitoring_data.csv'
output_path = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/gabung.csv'

# Execute scrape.py
subprocess.run(['python3', '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/scrape.py'])

# Execute inaport.py
subprocess.run(['python3', '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/inaport.py'])

# Load CSV files
hasil_scraping_df = pd.read_csv(hasil_scraping_path)
monitoring_data_df = pd.read_csv(monitoring_data_path)

# Print columns to debug
print("Columns in hasil_scraping_df:", hasil_scraping_df.columns)
print("Columns in monitoring_data_df:", monitoring_data_df.columns)

# Filter rows where 'gt' is greater than or equal to 500
filtered_hasil_scraping_df = hasil_scraping_df[hasil_scraping_df['gt'] >= 500]

# Select only the specified columns that exist in both DataFrames
columns_to_select_hasil_scraping = [
    'no_pkk_inaportnet', 'no_pkk', 'arrive_date', 'vessel_name', 
    'gt', 'loa', 'company_name', 'name_process_code', 'name_branch'
]
columns_to_select_monitoring_data = [
    'nomor_pkk', 'no_spb', 'waktu_spb'
]

# Ensure the columns exist in the DataFrames
selected_hasil_scraping = filtered_hasil_scraping_df[columns_to_select_hasil_scraping]
selected_monitoring_data = monitoring_data_df[columns_to_select_monitoring_data]

# Print the selected data to debug
print("Selected data from hasil_scraping_df:")
print(selected_hasil_scraping.head())
print("Selected data from monitoring_data_df:")
print(selected_monitoring_data.head())

# Merge dataframes using 'no_pkk_inaportnet' from hasil_scraping_df and 'nomor_pkk' from monitoring_data_df
merged_df = pd.merge(selected_hasil_scraping, selected_monitoring_data, left_on='no_pkk_inaportnet', right_on='nomor_pkk', how='inner')

# Add Periode_SPB column with formatted waktu_spb
merged_df['Periode_SPB'] = pd.to_datetime(merged_df['waktu_spb']).dt.strftime('%Y-%m')

# Print merged DataFrame to debug
print("Contents of merged_df:")
print(merged_df.head())

# Save merged dataframe to CSV
merged_df.to_csv(output_path, index=False)

print(f"✅ Data berhasil digabungkan dan disimpan dalam file {output_path}")
