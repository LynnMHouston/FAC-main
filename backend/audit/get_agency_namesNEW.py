from pathlib import Path
import csv
import requests
import json
import os

CSV_URL = "https://sam.gov/api/prod/fileextractservices/v1/api/download/Assistance%20Listings/datagov/AssistanceListings_DataGov_PUBLIC_CURRENT.csv?privacy=Public"

def download_latest_csv(download_path):
    """
    Downloads the latest CSV file from the given URL.
    """
    response = requests.get(CSV_URL, stream=True)
    if response.status_code == 200:
        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded the latest CSV to {download_path}")
    else:
        raise Exception(f"Failed to download CSV. Status code: {response.status_code}")

def get_agency_names(csv_file):
    """
    From a CSV of agency data, return a dictionary with the agency codes as
    keys and the names as values.

    Scrap rows with non-numeric agency nums and rows with empty agency names.
    """
    with open(csv_file, "r", newline="", encoding="Windows-1252") as file:
        reader = csv.DictReader(file)
        
        # Extract 'Program Number' as the key and 'Federal Agency (030)' as the value
        valid_agencies = {
            row["Program Number"]: row["Federal Agency (030)"]
            for row in reader
            if row["Program Number"].replace(".", "").isnumeric() and row["Federal Agency (030)"].strip()
        }
    return valid_agencies

def get_audit_info_lists(name):
    """
    Get lists of internal values and friendly strings for the responses to the
    Audit Information form section.

    Filter out anything with historical_only set to true.

    get_audit_info_lists("gaap_results")
    =>
    [
        {
            "value": "Unmodified opinion",
            "key": "unmodified_opinion",
            "property": "UNMODIFIED_OPINION"
        },
        …
    ]
    """
    jsonfile = Path("./schemas/source/audit/audit-info-values.json")
    jobj = json.loads(jsonfile.read_text(encoding="UTF-8"))

    return [info for info in jobj[name] if not info.get("historical_only") is True]

if __name__ == "__main__":
    # Define the path for the downloaded CSV
    csv_path = "./latest_assistance_listings.csv"

    # Download the latest CSV
    try:
        download_latest_csv(csv_path)
    except Exception as e:
        print(f"Error downloading the CSV: {e}")
        exit(1)

    # Process the downloaded CSV to get agency names
    try:
        agency_names = get_agency_names(csv_path)
        print("Agency Names Dictionary:")
        print(agency_names)
    except Exception as e:
        print(f"Error processing the CSV: {e}")
