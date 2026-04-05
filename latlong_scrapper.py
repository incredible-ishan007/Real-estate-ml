import requests
import pandas as pd
import time

def get_coordinates(sector):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"Sector {sector}, Gurgaon, Haryana, India",
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "real-estate-project"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if len(data) > 0:
        return data[0]["lat"], data[0]["lon"]

    return None, None


rows = []

for sector in range(1, 116):
    print(f"Fetching Sector {sector}...")

    lat, lon = get_coordinates(sector)

    rows.append({
        "Sector": f"Sector {sector}",
        "Latitude": lat,
        "Longitude": lon
    })

    time.sleep(1)


df = pd.DataFrame(rows)
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)

print("Done ")