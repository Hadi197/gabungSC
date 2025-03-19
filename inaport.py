import asyncio
import json
import csv
import datetime
from pyppeteer import launch

# Konfigurasi parameter scraping
PORTS = ["IDGRE", "IDSUB","IDBDJ"]
TYPES = ["ln", "dn"]
START_YEAR = 2024

async def scrape_data():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.setExtraHTTPHeaders({
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0"
    })

    all_data = []

    for year in range(START_YEAR, current_year + 1):
        for month in range(1, 13):
            if year == current_year and month > current_month:
                break  # Hentikan jika melewati bulan saat ini

            for port in PORTS:
                for trip_type in TYPES:
                    url = f"https://monitoring-inaportnet.dephub.go.id/monitoring/byPort/list/{port}/{trip_type}/{year}/{month:02d}"
                    print(f"📡 Scraping {port} - {trip_type} - {year}/{month}...")

                    try:
                        response = await page.goto(url, {"waitUntil": "networkidle0"})
                        content = await response.text()
                        data = json.loads(content)

                        if isinstance(data, dict) and "data" in data:
                            entries = data["data"]
                            for entry in entries:
                                entry["tahun"] = year
                                entry["bulan"] = month
                                entry["pelabuhan"] = port
                                entry["jenis_perjalanan"] = trip_type
                            all_data.extend(entries)
                            print(f"✅ {port} - {trip_type} - {year}/{month}: {len(entries)} entries.")
                        else:
                            print(f"⚠️ Data format incorrect: {data}")

                    except Exception as e:
                        print(f"❌ Error fetching {port} - {trip_type} - {year}/{month}: {e}")

    await browser.close()
    await save_results(all_data)
    print("🎉 Data scraping completed!")

async def save_results(data):
    csv_filename = "/Users/hadipurwana/Library/CloudStorage/GoogleDrive-pjmdataapps@gmail.com/My Drive/WEB/GabungSC/inaport_all.csv"

    if data:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["nomor_pkk", "no_spb", "waktu_spb", "tahun", "bulan", "pelabuhan", "jenis_perjalanan"])
            for item in data:
                writer.writerow([
                    item.get("nomor_pkk"),
                    item.get("no_spb"),
                    item.get("waktu_spb"),
                    item.get("tahun"),
                    item.get("bulan"),
                    item.get("pelabuhan"),
                    item.get("jenis_perjalanan")
                ])

        print(f"📂 Data saved: {csv_filename}")
    else:
        print(f"⚠️ No data to save")

asyncio.run(scrape_data())
