import json
import requests
import time
import csv
import pandas as pd

def fetch_page(base_url, headers, params, retries=5):
    for i in range(retries):
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i + 1} failed: {e}")
            if i < retries - 1:
                sleep_time = 2 ** i
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Moving to next page.")
                return None

def scrape_data():
    base_url = "https://phinnisi.pelindo.co.id:9017/api/monitoring/ina-spb"
    
    access_token = "eyJhbGciOiJIUzI1NiJ9.VTJGc2RHVmtYMStPeHptaHhOMlhmQzFiRFVVYmJwMTVMMithZm4wenZsUjBIRnlRcFV0RVVNZFZrRVIrclBUaVE0Y1hpd1lzV0wvT3ZwMnRRcFhrVGFhdDlTRW5JQmlRMWN0L1dneERuMTFoMzRVMUlNOVhKV2lxcFUraWtsbkUvSTZjQUR4dXBPMXY5SmNjQVJkWDRzL24reU9CaU5GaWJwSG5qZHJ2N3NTN2pLUVRKZnhqMXp4Vnh4WVVycTRKanBUQUJpYUNyOURyYi9uVHNFSUhNZnV0dnFQNHpCVVFCb0JIRmdzMlJUQUlUOFVpZXZGSEZqV0dQdkdGTkFTWXYvR3hGRDJtWk8vMEVhU1A0MzNrYmFrS2h6MExNcVJVUzlPQmZjYU5RWWVmNVY0VWN1WHZwdzhJZkxSYWw5bXM4QW1XZUF0L2x4eUprRU1kUUgyVExBTmoybncvOWw1QklzRDhFSjVwQUsyMTUweS80SXFiR3lPQUQzejJ5K2tlMG1YSjVRMlRpTUlWY3NNdXFOOTY4QT09.5bTNpwkZ6kV7QHZez4DNU0XopLcT2LO8-Z43jeNQoEQ"

    headers = {
        "accept": "application/json",  # Simplified accept header
        "accept-encoding": "identity",  # Request uncompressed response
        "accept-language": "en-US,en;q=0.9",
        "access-token": access_token,
        "connection": "keep-alive",
        "host": "phinnisi.pelindo.co.id:9017",
        "origin": "https://phinnisi.pelindo.co.id",
        "referer": "https://phinnisi.pelindo.co.id/",
        "sub-branch": "MTc=,MTY=,MjU=,ODE=,NTc=,MTAx,NjE=,NzM=,NzQ=,ODM=,NzU=,NzI=,Mjc=,Mjk=,NjA="
    }

    params = {
        "page": 1,
        "record": 25000,
        "data": "",
        "start_date": "2025-01-01",
        "end_date": "2025-03-31",
        "is_success": ""
    }

    try:
        response = fetch_page(base_url, headers, params)
        if not response:
            print("Failed to fetch initial data.")
            return

        data = response
        print(f"Response content: {json.dumps(data, indent=2)[:500]}...")

        if not data or "data" not in data:
            print("Invalid response format")
            return
            
        total_pages = data["data"]["totalPage"]
        print(f"Total pages: {total_pages}")
        
        all_records = []

        for page in range(1, total_pages + 1):
            print(f"Fetching page {page}...")
            
            params["page"] = page
            page_data = fetch_page(base_url, headers, params)
            
            if page_data:
                if "data" in page_data and "dataRec" in page_data["data"]:
                    all_records.extend(page_data["data"]["dataRec"])
            else:
                print(f"Failed to fetch page {page}")
            
            time.sleep(1)

        print(f"Total records fetched: {len(all_records)}")
        if len(all_records) > 0:
            print(f"Sample record: {json.dumps(all_records[0], indent=2)}")

        filtered_records = [{"nomor_pkk": record["nomor_pkk"], "nomor_spb": record["nomor_spb"]} for record in all_records if "nomor_pkk" in record and "nomor_spb" in record]

        print(f"Filtered Records Count: {len(filtered_records)}")
        if len(filtered_records) > 0:
            print(f"Sample Filtered Record: {json.dumps(filtered_records[0], indent=2)}")

        csv_filename = "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/spb.csv"
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["nomor_pkk", "nomor_spb"])
            for record in filtered_records:
                writer.writerow([record["nomor_pkk"], record["nomor_spb"]])

        json_filename = "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/spb.json"
        with open(json_filename, mode="w", encoding="utf-8") as file:
            json.dump(filtered_records, file, ensure_ascii=False, indent=4, default=str)

        print(f"Data successfully saved to {csv_filename} and {json_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    # Load the CSV file
    df = pd.read_csv('spb.csv')

    # Display all data without any filters
    print(df.to_string(index=False))

if __name__ == "__main__":
    scrape_data()
