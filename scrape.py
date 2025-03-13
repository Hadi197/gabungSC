import json
import asyncio
from pyppeteer import launch
from pyppeteer.chromium_downloader import download_chromium, REVISION

# Specify a different Chromium revision
REVISION = '818858'  # Example revision, you can change this to a known working revision
import csv
import time

async def scrape_data():
    url_template = "https://phinnisi.pelindo.co.id:9021/api/executing/monitoring-operational?page={page}&record=10000&data="
    access_token = "eyJhbGciOiJIUzI1NiJ9.VTJGc2RHVmtYMStRVUwyQ0pJTGhETTFyTk9LN1J4RnplMnBYd0tDMnY4VWU3d3FqemhJeDV4dWFMN1BxTDBYcHdxNDhYU1NWTHdxMTlqZFRvemlTd1dpdGIyZHdaMWZuR2tVb1QrRzA0NmhKOG1CVTJoUVI4N1BMdnNYRjYyZUFESmtxVjM1a2s0Ny81ZUtkYnFUandpZ3pxcmE4U1hPaWlOU21VTzJiYnR0VXFYOEVpUVRhM1g1bHg2Y0Zackk4VHA0aURNRmxrZVliUDF3SmxKNEdwSGFKRml0dFJhS2RscjhHdGR1Wlg1dXZrNXd6TDlPdTRFQ0doY3pVMVE5VHV3YURNT2Z1bGhaM3dFbE5WL1VzWHcwZ1QrOUNQdTVhQzNVRGxHWXErbERwRnkwa2VWMUUxLzlsQUxLSmVwcXNJNXhTak1BWjAvZENJMys5QjVBeFJraktuZlFRZnJtRVdaSVN5cFBZVW1rQ1JCMVBMYWw0MURzTG0wV0YwaFRIem9QaUtsZ3dySXRVRjR6UjNDZ1hTbm10OG5TM2JCZndQa1FOSjQvOXBvdTMwNzZZTFFlWVhoU0tTZEFnMGVwaW14dlJrV085VTNmV09Pb1pqaWdNdjh3U2FvV2tYUTRYUENxZ1ZpUGNVb0VKTHBYQVl6dTlOUkZhNGFuMmVoRkl0MHc0RzFsRGU3YVJiNUhJL1Z2MXZzSjI4S2RWNXRXQVJCNUpoQlAxVUFuTWFHcTM0N1pWQnIyZy9vOUJ1VUxLazNSTWVORXZSOHludU90UUhpWklmem5NQkxIMHVnTlFCNFZENzBjVklrS2FZZDNCZ2plNUZSeE1FSW9MdmxhTFZ0QmVoNDdLNnZJTEhPQzErNkVDS1BCVWZtQU5tbU93S1FtYm9pQi9vbkRIOTRrUEl4V2RiN3dhelBTT3RDWFlIQ0FzZlFkdG41c0pDYTVYUTlVUnNmcDlpUXZacjFFU0Jjc0IxanBnakJ3b0hXa1JBVUkwQ1oyd2dFL0EzWldCOXZUT3d1ekx5SUJrdWRHU2ZjTmVrK0l2d1ZleDlCeXhQUnJnWmVFVXlicnAxTXp6RXVodnJIZ0Y5aTVSbDlpNktSTTh4aitkOW1UTkdSWTdsZGJZQWtXVVZNRm9rd3RKRnZGN2RxZkU1eE95OWY2SEQvYzY5REV3TlQxWjQwTTAzUGRBc3RYZjk5dWdlNEZlWGNiUTFrQU5zQ2FhY3Jld2ZqNkZNODRiQldyMExPNTlrcUc2eFpZVmtWdnNmQTk1a3h6cjlrd09CM2NpYWllNVVvRVFiZWEraW5ibWV5UVlEVTc2MW5YdFUvQmduM3pWQnQxNm5tTll5V1kwdkxDZDd4bjNHREdhNXBINk1Jb001Mk1TT2dVMGt5bjlUNHBYTmN6LzFwbWJtcE82ZDFZMUI3NWV5NVQxTGNzV0pxdUVLMTVCVHFZZ2YxRDVodEtXdE10aFRMZGlmaUk3OXl4RlRweTk1WnRSVGdzM3hrbEl6cmNQQkIxY0hhZkovclNyamd4Nm9KQ3BUMVJjN2xINmgvclBEVHVoT3A0WU5pYzFZbEVUUGVjTUpiMTg3ZnpwS0tNblVRWkZTb0JMQVNSTlZ5RlQ2dlBGZVpkVUZoYkJWdXNIalBmYVVpdlNYcjFpM1RUL3BiQ2htNVl0Q3NzRm80ZHJDK3dRMjBGQzV6Q2NoZXJiR05QMUdySG1peEVTeEpWUUtuZHRXd20vajc5aVN0SjZ3N3QxK2lBM1NzQkp5YnlUNU9DUWpQcWkrelk5REhZdmhWU0duelY4bmhkOUZrbGNqOWM2T0kzQkxMenNONmlzRjNHOWNUWC8xMGpnV2ZNVEl0Qk03TFJkL0FYSXJTcmNGUlpVemZRWkxHMXJwVThWTG9Vb0JGTWJoK3lYTFVUZ0ZMNkhWbGt2WFg0WUdyd3k4MDQ3Q2FBdjlIM1RqcmY3RmgyV2ppV0FiY0VoZWZFOFhaMGJrQXRTaHozbVVhTXA3VXlpT2t4TElNK0wzdmZQODJwclg4ZWZPQmxNRWlyWWRxcm1OaWdTZnNjamk3QnFVRXBuL0k4NnZVdEwrR0ROUWNSV3MyVEhVQVVoajRtcE45eTQySXIvcVRoWkhFcXRtTG9PV2RLeEJkVXA0eGVHdXppTVRRY0tib3ZWTWsxajlBM3RsRzVTdEE4cUFFN0tZWDdDVkJGdjdWM095NTR4RTZrdzF1TVA1KzN5R2l2OUNJWmY4VVR2UU5GNzZXZUc3MTJvMERNMy9FZ1creG9RazhBNFRLenJmTyt6YjdCUlYxOGtIaW5TekdaeXIvWEFEMHZ3OVdUWHFVWkJsaHk3Yk1uYkRaUWwzSWtqNGFiUkZDR2RzcG5zZlFkOS9xSmxwaTNpODB0ZVJOcXJnbDVPdTdKNS8xTHFqbk5PWEo1QjZLZGFrWDFNZGZHNm9aUFVjSHo3Z3ZhTmlxMy9KSFRuYXd3WW4wTVowNlRLZC9qS1BCc3UwN1VhcENrRC9SYys1eU83MmIrdklObS9xSUorM1RIVms0R0ZyTkh0VUxMVkpFaUFTdk9GdWFlS2Nqci9rdTNWaGdnZmkrWFdLR0IyMm1YSDhtdXhleCtTSU0rRUt4VWROdEVCTytkRmVWZ1BCNWNrbFBZMy9EYUFuc2kwa2ttSTdGcndpNTBYRkhmczUxbERNejJVTENGVzl4L0ViNHZoYWEvQjRUUWJrR24wcmFWNWZ1VmpZMDBabUpjSWNqY2RYVFBYSURBVHhmblpRS1pOa0ZrK2RwaHhrbGkycG9iZGFHYlpCNWV3dmxnVFpOSmhDU2dBSy92OFFoQmtxcE1Ld2pRT29YRWZNdzJNSGZpa09NTk5pdTNjNFd0WG5qbHRQbzZoZlFBa2hpekJ4clR5TnNsQjBaT1pocTFWREN6MEFtRzdGV1VVUHlKcktvZVBZVmhVdmNraU1kWUFLTXo1U0xjYXNNQXJmLy93OER4RlFlL0lLbDQyYkhLcTRLdnJHK2RnWVM0UXFzL1VKU1ZTbGU3QUZTWjVJZVdJclhHanVIMFhVT05EOUo5RVgycENSUFVvSnBTREFEUmtGbUlpWUJxNG1QMHAxZHdHcHhuNVgwUnUyQjRRTXRuZUI2L0JNeS96ZGVBd2FUT0FXaUNqblNIVGhjbTY0SFk2a0lsSjdvTmR1NU9tcE5YOTFIN0gwWkd3ZitIV1hsMm9RQmFLbkgxM2RwTGJjWEJCaFVJS2F1NHV1VC9EeS82TlhzU05JcTQxSUxwZXQrc1dMSlg3UGFHaGVEZXA3Ym1xUW9UWGx0QmZMb2laTzhBWkE2RFpxaEUwWEpOSHF1S3NVbnpmZklnQlA1SnROalNCMmxJRURiR2htdm5qTDVvM3ZIWFUzdGlDZlJFbjBBMFEyQnA1azRYREJHaUpLN093ZjdaVjdhRndaSzBIYjFZcGVoR3lSQlhrN0JOQXhOYnlxMUNlV25KU3ZmWkYxeU5qTFR0d1EvMno0TjA2NC84d1JwSXlsVE1iNFRnVGw5dmxVYTBjcWdBPQ.MKwyU5d8vDVCZyqyWQgrE18OrEXFjiaME9iV7M1ENS8"

    browser = await launch(headless=True)
    page = await browser.newPage()
    
    await page.setExtraHTTPHeaders({
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "access-token": access_token
    })

    # Get the first page to determine the total number of pages
    response = await page.goto(url_template.format(page=1), {"waitUntil": "networkidle0"})
    
    if response is None:
        print("❌ Tidak mendapatkan respons dari server.")
        await browser.close()
        return

    content = await page.evaluate("document.body.innerText")

    if not content:
        print("❌ Respons kosong dari server.")
        await browser.close()
        return
    
    data = json.loads(content)
    total_pages = data['data']['totalPage']
    print(f"Total pages: {total_pages}")

    all_records = []

    # Loop through all pages
    for page_number in range(1, total_pages + 1):
        print(f"Fetching page {page_number}...")
        response = await page.goto(url_template.format(page=page_number), {"waitUntil": "networkidle0"})
        content = await page.evaluate("document.body.innerText")
        data = json.loads(content)
        filtered_data = [item for item in data['data']['dataRec'] if item.get('name_process_code') not in ['Preinvoice', 'NOTA NORMAL'] and item.get('process_code') != '0']
        all_records.extend(filtered_data)
        time.sleep(1)  # Add delay to prevent rate limiting

    # Save to CSV
    csv_filename = '/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/hasil_scraping.csv'
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(all_records[0].keys())  # Write header
        for record in all_records:
            writer.writerow(record.values())
    print(f"✅ Data berhasil disimpan dalam file {csv_filename}")

    await browser.close()

asyncio.run(scrape_data())

def scrape_data_with_requests():
    url = "URL_API_YANG_DIGUNAKAN"  # Ganti dengan URL API yang benar
    headers = {
        "Authorization": "Bearer TOKEN_API_ANDA"  # Ganti dengan token jika diperlukan
    }

    # Request pertama untuk mendapatkan total halaman
    response = requests.get(url, headers=headers)
    data = response.json()

    # Ambil total halaman
    total_pages = data["data"]["totalPage"]
    print(f"Total pages: {total_pages}")

    # List untuk menyimpan semua data
    all_records = []

    # Looping untuk mengambil semua data dari API
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page}...")
        
        params = {"page": page}  # Sesuaikan parameter jika perlu
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            page_data = response.json()
            all_records.extend(page_data["data"]["dataRec"])
        else:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
        
        time.sleep(1)  # Tambahkan delay untuk mencegah pembatasan API

    # Menyimpan ke dalam file CSV
    csv_filename = "data_kapal.csv"

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer()

        # Menulis header
        writer.writerow(["no_pkk", "no_pkk_inaportnet", "ppkb_code", "arrive_date", "departure_date", 
                         "voyage_in", "voyage_out", "visit_name", "cruise_name", "vessel_name", 
                         "call_sign", "imo_number", "flag_name", "company_name", "gt", "loa", "dwt", 
                         "name_branch", "port_code"])

        # Menulis data
        for record in all_records:
            writer.writerow([
                record["no_pkk"], record["no_pkk_inaportnet"], record["ppkb_code"], record["arrive_date"], 
                record["departure_date"], record["voyage_in"], record["voyage_out"], record["visit_name"], 
                record["cruise_name"], record["vessel_name"], record["call_sign"], record.get("imo_number", "N/A"), 
                record["flag_name"], record["company_name"], record["gt"], record["loa"], record["dwt"], 
                record["name_branch"], record["port_code"]
            ])

    print(f"Data berhasil disimpan dalam file {csv_filename}")

# Uncomment to run the requests-based scraper
# scrape_data_with_requests()
