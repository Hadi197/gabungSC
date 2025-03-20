import json
import requests
import csv
import time
import brotli  # Add this import

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
    base_url = "https://phinnisi.pelindo.co.id:9017/api/executing/monitoring-operational"
    
    # Full access token in a single line
    access_token = "eyJhbGciOiJIUzI1NiJ9.VTJGc2RHVmtYMStPeHptaHhOMlhmQzFiRFVVYmJwMTVMMithZm4wenZsUjBIRnlRcFV0RVVNZFZrRVIrclBUaVE0Y1hpd1lzV0wvT3ZwMnRRcFhrVGFhdDlTRW5JQmlRMWN0L1dneERuMTFoMzRVMUlNOVhKV2lxcFUraWtsbkUvSTZjQUR4dXBPMXY5SmNjQVJkWDRzL24reU9CaU5GaWJwSG5qZHJ2N3NTN2pLUVRKZnhqMXp4Vnh4WVVycTRKanBUQUJpYUNyOURyYi9uVHNFSUhNZnV0dnFQNHpCVVFCb0JIRmdzMlJUQUlUOFVpZXZGSEZqV0dQdkdGTkFTWXYvR3hGRDJtWk8vMEVhU1A0MzNrYmFrS2h6MExNcVJVUzlPQmZjYU5RWWVmNVY0VWN1WHZwdzhJZkxSYWw5bXM4QW1XZUF0L2x4eUprRU1kUUgyVExBTmoybncvOWw1QklzRDhFSjVwQUsyMTUweS80SXFiR3lPQUQzejJ5K2tlMG1YSjVRMlRpTUlWY3NNdXFOOTY4QT09.5bTNpwkZ6kV7QHZez4DNU0XopLcT2LO8-Z43jeNQoEQ"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "access-token": access_token,
        "connection": "keep-alive",
        "host": "phinnisi.pelindo.co.id:9017",
        "origin": "https://phinnisi.pelindo.co.id",
        "referer": "https://phinnisi.pelindo.co.id/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Opera\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sub-branch": "MTc=,MTY=,MjU=,ODE=,NTc=,MTAx,NjE=,NzM=,NzQ=,ODM=,NzU=,NzI=,Mjc=,Mjk=,NjA=",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0"
    }

    params = {
        "page": 1,
        "record": 50000,
        "data": "",
        "subBranch": "MTc=,MTY=,MjU=,ODE=,NTc=,MTAx,NjE=,NzM=,NzQ=,ODM=,NzU=,NzI=,Mjc=,Mjk=,NjA="
    }

    # Request pertama untuk mendapatkan total halaman
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
        
        # List untuk menyimpan semua data
        all_records = []

        # Looping untuk mengambil semua data dari API
        for page in range(1, total_pages + 1):
            print(f"Fetching page {page}...")
            
            params["page"] = page  # Sesuaikan parameter jika perlu
            page_data = fetch_page(base_url, headers, params)
            
            if page_data:
                if "data" in page_data and "dataRec" in page_data["data"]:
                    all_records.extend(page_data["data"]["dataRec"])
            else:
                print(f"Failed to fetch page {page}")
            
            time.sleep(1)  # Tambahkan delay untuk mencegah pembatasan API

        # Debugging information
        print(f"Total records to write: {len(all_records)}")
        if len(all_records) > 0:
            print(f"Sample record: {json.dumps(all_records[0], indent=2)}")

        # Filter out records with specific name_process_code values
        excluded_process_codes = ["Preinvoice", "Cancel PKK", "NOTA NORMAL", "NOTA BATAL", "Billing Claim", "Not to Bill", "Nota"]
        filtered_records = [record for record in all_records if record.get("name_process_code") not in excluded_process_codes]

        # Filter out records with gt less than 500
        filtered_records = [record for record in filtered_records if record.get("gt", 0) >= 500]

        # Remove duplicate records based on 'no_pkk'
        unique_records = {record["no_pkk"]: record for record in filtered_records}.values()

        # Menyimpan ke dalam file CSV
        csv_filename = "data_kapal.csv"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Menulis header
            writer.writerow(["no_pkk", "no_pkk_inaportnet", "ppkb_code", "vessel_name", "company_name", "gt", "loa", "name_branch", "port_code", "name_process_code", "departure_date"])

            # Menulis data
            for record in unique_records:
                try:
                    writer.writerow([
                        record.get("no_pkk", ""), 
                        record.get("no_pkk_inaportnet", ""), 
                        record.get("ppkb_code", ""), 
                        record.get("vessel_name", ""), 
                        record.get("company_name", ""), 
                        record.get("gt", ""), 
                        record.get("loa", ""), 
                        record.get("name_branch", ""), 
                        record.get("port_code", ""),
                        record.get("name_process_code", ""),
                        record.get("departure_date", "")
                    ])
                except Exception as e:
                    print(f"Error writing record: {record}")
                    print(f"Exception: {e}")

        print(f"Data berhasil disimpan dalam file {csv_filename}")

        # Menyimpan ke dalam file JSON
        json_filename = "data_kapal.json"
        with open(json_filename, mode="w", encoding="utf-8") as file:
            json.dump(list(unique_records), file, ensure_ascii=False, indent=4, default=str)
        print(f"Data berhasil disimpan dalam file {json_filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

if __name__ == "__main__":
    scrape_data()
