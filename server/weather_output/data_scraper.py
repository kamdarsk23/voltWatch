import csv
import requests
from collections import defaultdict
from datetime import datetime


def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


def write_data_to_csv(data, csv_filename, energy):
    if not data:
        print("No data to write.")
        return

    # Extract headers from the first item's keys
    headers = ["datetime", "tempmax", "tempmin", "temp", "cloudcover", "energy"]

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for day, energy_value in zip(data.get("days", []), energy):
            row_data = [day.get(key, "") for key in headers[:-1]]  # Exclude energy column
            row_data.append(energy_value)  # Append energy value to the row
            writer.writerow(row_data)


def process_csv(input_csv):
    # Define defaultdict to store summed values for each date
    summed_values = defaultdict(int)
    date_to_int = defaultdict(int)

    # Read input CSV and process data
    with open(input_csv, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for row in reader:
            date_time_str = row[1]

            if row[5]:  # Check if row[5] (energy column) is not empty
                value = float(row[11])  # Get value from the energy column
                # Parse datetime string to get date
                date_time = datetime.strptime(date_time_str, "%m/%d/%y %H:%M")
                date = date_time.date()
                # Add value to the corresponding date
                summed_values[date] += value
                date_to_int[date] += 1

    # Extract only the cumulative values and return as a list
    for day in summed_values.keys():
        summed_values[day] = int(summed_values[day] / date_to_int[day])
    cumulative_values = list(summed_values.values())
    return cumulative_values


def main():
    # Fetch data from the API
    api_url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/76006/2020-04-01"
               "/2020-10-01?key=J9TYR5T7VQ45C5UG2VJAGSHQ4&include=days&elements=datetime,tempmax,tempmin,temp,"
               "cloudcover")
    data = fetch_data_from_api(api_url)

    if data:
        # Write API data to CSV
        api_csv_filename = "api_data.csv"
        input_file = "data.csv"  # Use the API data CSV as input
        energy = process_csv(input_file)
        write_data_to_csv(data, api_csv_filename, energy)
    else:
        print("No data retrieved from the API.")


if __name__ == "__main__":
    main()
