# This script reads the JSON file at the URL https://web.cluster.iz3mez.it/spots.json, returns the first 3 lines in decreasing spot_datetime
# order on first launch and then checks for new lines every 5 seconds.
# 73 de Francesco IZ3MEZ
import requests
import time
import json
from operator import itemgetter

def get_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data.sort(key=itemgetter('spot_datetime'), reverse=True)  # Sorts data by spot datetime in descending order
    return data

def print_data(data, fields):
    for row in data:
        for field in fields:
            print(f"{field}: {row.get(field, 'N/A')}")
        print("\n")

def main():
    url = "https://web.cluster.iz3mez.it/spots.json"
    fields = ["spot_datetime", "band", "frequency", "spotted", "spotted_country", "spotted_continent", "spotter", "spotter_country", "spotter_continent", "spotter_comment"]
    old_data = get_data(url)
    print_data(old_data[:3], fields)  # Print the first 3 fields
    latest_datetime = old_data[0]['spot_datetime'] if old_data else None
    while True:
        time.sleep(5)
        new_data = get_data(url)
        if new_data and new_data[0]['spot_datetime'] != latest_datetime:
            latest_index = next((index for index, d in enumerate(new_data) if d['spot_datetime'] == latest_datetime), len(new_data))
            print_data(new_data[:latest_index], fields)
            latest_datetime = new_data[0]['spot_datetime']

if __name__ == "__main__":
    main()
