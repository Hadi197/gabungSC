import asyncio
import json
import time
from pyppeteer import launch
import csv

async def scrape_data():
    base_url = "https://monitoring-inaportnet.dephub.go.id/monitoring/byPort/list/IDSUB/{type}/{year}/{month}?_={timestamp}"
    
    years = range(2024, 2026)  # Tahun dari 2024 sampai 2025
    months = range(1, 13)  # Bulan dari 01 sampai 12
    types = ["ln", "Dn"]  # Luar Negeri & Dalam Negeri
    
    all_data = []  # List untuk menyimpan semua hasil

    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.setExtraHTTPHeaders({
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "SRVNAME=cookie_app1; XSRF-TOKEN=eyJpdiI6ImlQbDAreUwwcnladHo1QXNUNHh3WHc9PSIsInZhbHVlIjoiOXlOWEduaWQ3VHNodll5OU5GRnRucXZCWG5DcTRQd3hLa1ZMVHZMZGUvKy9LT2RUcEJYWktSZWZHWUh4blZlZWRiaE1EcEtHemJ6c25LM2JzYlFyYiszNHRoMHR2VDZuLzU1MG5SMUlZZ1daN1ptNHBhVnRDbXczOURHb21kWkciLCJtYWMiOiJmZjk5ZDViMjdkZDFiZmI4NWEzNDNlMTAzNmM0OWMxYjA5ODVjNjM0MzFlNjdkOGRkNTI4ODZiMWY0ZjJkNzQ5IiwidGFnIjoiIn0%3D; monitoring_inaportnet_session=eyJpdiI6ImZwdGtLSkxkT1JNcGpzb0ZlTzF0cWc9PSIsInZhbHVlIjoiU29YM2JlMFJsbjNsNzFLWUZjNnJ2L3VXVUVEUHNYVE5peEU4ZkJzTUluM1ZzbW9FMmZwR3F3SzFqNk9WVXJ5R2NlNzNtem4yQjNRa1V0aXBQSEFsWElDUWJ2UTFWcCtveUZoRVFtMk9BWEpaREtvUG1EbXNmWXF1a0g4R1ZZK2kiLCJtYWMiOiI3MzZhYWUyOWNmZTNkZThlZGRkNjJlYmU0Nzg3NTgyYTIxMmU2MDdjOTY5MDdiN2Y5ODg0ZGJjNzU2MzBlMGU0IiwidGFnIjoiIn0%3D",
        "referer": "https://monitoring-inaportnet.dephub.go.id/monitoring/byPort/IDSUB/ln/2025/01",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Opera";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    })

    for year in years:
        for month in months:
            for type_ in types:
                # Format URL dengan tahun, bulan, dan tipe pelayaran
                url = base_url.format(
                    type=type_,
                    year=year,
                    month=str(month).zfill(2),  # Pastikan bulan dalam format 01, 02, dst.
                    timestamp=int(time.time() * 1000)  # Gunakan timestamp dinamis
                )
                
                print(f"Scraping: {url}")  # Tampilkan URL yang sedang diproses
                
                try:
                    response = await page.goto(url, {"waitUntil": "networkidle0"})
                    content = await response.text()
                    data = json.loads(content)
                    
                    print(f"Data fetched from {url}: {data}")  # Debugging line to print fetched data
                    
                    if isinstance(data, dict) and 'data' in data:
                        all_data.extend(data['data'])
                    else:
                        print(f"Unexpected data type: {type(data)} - {data}")

                except Exception as e:
                    print(f"Error saat mengambil data {url}: {e}")

    await browser.close()

    # Simpan semua hasil scraping ke file JSON
    with open("monitoring_data.json", "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, indent=4, ensure_ascii=False)

    # Save data to CSV
    if all_data:
        save_csv(all_data, 'monitoring_data.csv')
    else:
        print("❌ Data format tidak sesuai.")

    print("✅ Semua data berhasil disimpan ke monitoring_data.json dan monitoring_data.csv")

def save_csv(data, filepath):
    if not data:
        print("❌ No data to save.")
        return
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["nomor_pkk", "nama_kapal", "no_spb", "waktu_spb"])
        # Write data
        for item in data:
            writer.writerow([
                item.get("nomor_pkk"),
                item.get("nama_kapal"),
                item.get("no_spb"),
                item.get("waktu_spb")
            ])

# Jalankan scraping
asyncio.run(scrape_data())
