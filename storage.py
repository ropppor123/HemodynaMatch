import json
import os

# Locate the folder containing this Python file.
base_folder = os.path.dirname(os.path.abspath(__file__))

# Build the storage folder path and create it if it does not exist.
data_folder = os.path.join(base_folder, "dataStorage")
os.makedirs(data_folder, exist_ok=True)

recipient_data_storage = os.path.join(data_folder, "recipient.json")
donor_data_storage = os.path.join(data_folder, "donor.json")
request_data_storage = os.path.join(data_folder, "requests.json")

# Read Recipient, Donor, Requests data
def read_data(filename:str) -> list[dict]:
    """Read record dictionaries; return an empty list for a missing or blank file."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip(): # Treat empty or whitespace-only files as having no records.
            return []

        data = json.loads(content)

        # Validate the outer list and each record inside it.
        if not isinstance(data, list):
            raise ValueError(f"{filename} must contain a list.")

        for record in data:
            if not isinstance(record, dict):
                raise ValueError(f"{filename} must contain dictionaries inside the list.")
        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        raise ValueError(f"{filename} contains invalid JSON. Please check the file.")


def get_recipients()->list[dict]:
    return read_data(recipient_data_storage)


def get_donors()->list[dict]:
    return read_data(donor_data_storage)


def get_requests()->list[dict]:
    return read_data(request_data_storage)

# Check existing ID of Recipinent and Donor
def recipient_id_exist(recipient_id):
    recipients = get_recipients()

    for new_recipient in recipients:
        if new_recipient["id"] == recipient_id:
            return True
    
    return False

def donor_id_exist(donor_id):
    donors = get_donors()

    for new_donor in donors:
        if new_donor["id"] == donor_id:
            return True
    
    return False


# Save Recipient, Donor , Request data
def save_data(filename: str, data: list[dict]) -> None:
    """Save a list of records to a JSON file."""
    # Convert the data before opening the file.
    content = json.dumps(data, indent=4)

    # Write the JSON data to the file.
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def save_recipient(recipient_data):
    recipients = get_recipients()
    recipients.append(recipient_data)
    save_data(recipient_data_storage, recipients)


def save_donor(donor_data):
    donors = get_donors()
    donors.append(donor_data)
    save_data(donor_data_storage, donors)


def save_request(request_data):
    requests = get_requests()
    requests.append(request_data)

    content = json.dumps(requests, indent=4)

    with open(request_data_storage, "w", encoding="utf-8") as file:
        file.write(content)

    return len(requests) - 1
