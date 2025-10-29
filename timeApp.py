import requests
import os
from dotenv import load_dotenv
load_dotenv()
TIME_APP_KEY = os.getenv("TIME_APP_KEY")
if not TIME_APP_KEY:
    raise ValueError("The API key is missing!")

def get_timezone_by_country(country: str):
    url="http://api.timezonedb.com/v2.1/list-time-zone"
    params={
        "key": TIME_APP_KEY,
        "format": "json"
    }
    response=requests.get(url, params=params)
    data=response.json()
    if data.get("status") != "OK":
        raise Exception(f"API ERROR: {data.get('message', '<no message>')}")
    for zone in data["zones"]:
        if zone["countryName"].lower()==country.lower():
            return zone["zoneName"]
    raise Exception("Country not found!")

def get_local_time(zone_name: str):
    url="http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": TIME_APP_KEY,
        "format": "json",
        "by": "zone",
        "zone": zone_name
    }
    response=requests.get(url, params=params)
    data=response.json()
    if data.get("status")!="OK":
        raise Exception(f"API ERROR: {data.get('message', '<no message>')}")
    return data["formatted"]

def main():
    while True:
        country=input("Enter a country or 'exit' to stop the app: ").strip()
        if country.lower() in ("exit", "quit"):
            print("Good bye!")
            break
        try:
            timezone = get_timezone_by_country(country)
            time_str = get_local_time(timezone)
            print(f"🕒  The time in {country} (area {timezone}) is: {time_str}")
        except Exception as e:
            print(f"Error: {e}")
        print()
if __name__ == "__main__":
    main()