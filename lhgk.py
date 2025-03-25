import json
import requests
import time
import csv
from datetime import datetime

def fetch_page(base_url, headers, params, retries=5):
    for i in range(retries):
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            return response
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
    base_url = "https://phinnisi.pelindo.co.id:9014/api/reporting/daily-pilotage/list"
    
    access_token = "eyJhbGciOiJIUzI1NiJ9.VTJGc2RHVmtYMStyMFJrUUF4cGpVTGVSRzZ1M3hUQ0ZzejdvOEcrbmdRbFZkTVB2anhqMktuclZrYkVwVngxZWdIS0RoZXJ6b1hlRXl0RzZXbXVVVzJWRFVhOXFTaHFKY0R4WVUrZHdPY2NrcU94NlN3MkVPczhkVHhCUjUzaDZsUUliUmVOY3dlN3Q5MUsrWVZ6aFVDQVdFSVZ4cDNLWktVeDFvZGV4MHNDbGQvMlVxNzE4S1pzazlYdjFLdU9iTi9hb2IvLzdKTWVxTEErT0tnbWttWXl4SS9halNkK2hJZGQ4aGcrZU4xeCs0YWdLUkpxQm5SRHZHV2VNcVNLT1dCenNjWVoxcjRzZlVXdWNsa2YrMnNsb3RGMHM3R28yeUhTK1g1bXRhK2JyUEw4MmhQbkpEZ3JieWhrcU9hUitKS29RSmJBdDRGc3ArVzluYnhWVU1OUzdxK2dMQ0p1SmJ1ci9TTlFsUVc5Zk5mUlFORUkxVFpUQ3FESXFJeFN1MlB5NmZhNjl0blVzRmg1RjNHak5WUT09.zxxFzMsk4vEQkdJdXfXJ_J5NltLoAl1gA46o9DFJcOY"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "access-token": access_token,
        "connection": "keep-alive",
        "host": "phinnisi.pelindo.co.id:9014",
        "origin": "https://phinnisi.pelindo.co.id",
        "referer": "https://phinnisi.pelindo.co.id/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Opera\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sub-branch": "OTk5,MTc=,MTY=,MjU=,ODE=,NjE=,MTAx,NTc=,NzQ=,ODM=,NzU=,NzI=,Mjc=,Mjk=,NjA=",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0"
    }

    params = {
        "start": "2025-01-01",
        "end": datetime.now().strftime("%Y-%m-%d"),
        "data": "",
        "page": 1,
        "record": 10000
    }

    try:
        response = fetch_page(base_url, headers, params)
        if not response:
            print("Failed to fetch initial data.")
            return

        # Save headers to a file
        headers_filename = "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/api_headers.json"
        with open(headers_filename, 'w') as f:
            json.dump(dict(response.headers), f, indent=4)
        print(f"API headers saved to {headers_filename}")

        data = response.json()
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
                try:
                    json_data = page_data.json()
                    if "data" in json_data and "dataRec" in json_data["data"]:
                        all_records.extend(json_data["data"]["dataRec"])
                    else:
                        print(f"Failed to fetch page {page}: Invalid data format")
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON for page {page}: {e}")
            else:
                print(f"Failed to fetch page {page}")
            
            time.sleep(1)

        print(f"Total records fetched: {len(all_records)}")
        if len(all_records) > 0:
            print(f"Sample record: {json.dumps(all_records[0], indent=2)}")

        # Save to CSV
        csv_filename = "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/lhgk.csv"
        if all_records:
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Write headers
                writer.writerow(all_records[0].keys())
                # Write data
                for record in all_records:
                    writer.writerow(record.values())
            print(f"Data successfully saved to {csv_filename}")
        else:
            print("No data to save.")

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
