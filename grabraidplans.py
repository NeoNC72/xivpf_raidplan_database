import json
import re
import sqlite3
import requests
import schedule
import time

def fetch_and_store_plans():
    print("Fetching and storing raid plans...")
    try:
        data = requests.get("https://xivpf.com/api/listings").json()

        conn = sqlite3.connect('raidplans.db')
        cursor = conn.cursor()

        cursor.execute('''

        CREATE TABLE IF NOT EXISTS raidplans (
            duty_name TEXT,
            url TEXT,
            UNIQUE(duty_name, url)
        )
        ''')

        count = 0
        link_pattern = re.compile(r"(raidplan\.io/\S+|pastebin\.com/[a-zA-Z0-9]+|ff14\.toolboxgaming\.space/\S+)")

        for item in data:
            listing = item.get("listing")
            if listing and listing.get("category") == "HighEndDuty":
                desc = listing.get("description", {}).get("en", "")
                match = link_pattern.search(desc)
                if match:
                    plan_url = match.group(1)

                    duty_info = listing.get("duty_info", {})
                    duty_name = duty_info.get("name", {}).get("en", "Unknown Duty")
                    try:
                        cursor.execute("INSERT OR IGNORE INTO raidplans (duty_name, url) VALUES (?, ?)",
                                       (duty_name, plan_url))
                        if cursor.rowcount > 0:
                            count += 1
                    except sqlite3.Error as e:
                        print(f"Database error inserting {duty_name} - {plan_url}: {e}")


        conn.commit()
        conn.close()
        print(f"Finished. Added {count} new unique plans.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

schedule.every(2).minute.do(fetch_and_store_plans)

print("Scheduler started. Will run fetch_and_store_plans every minute.")
fetch_and_store_plans()
while True:
    schedule.run_pending()
    time.sleep(1)