import json
import os

base_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_folder, "dataStorage")

os.makedirs(data_folder, exist_ok=True)

recipient_data_storage = os.path.join(data_folder, "recipient.json")
donor_data_storage = os.path.join(data_folder, "donor.json")
request_data_storage = os.path.join(data_folder, "requests.json")

# Get Recipient, Donor, Requests data
def read_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            return []

        data = json.loads(content)

        if not isinstance(data, list):
            raise ValueError(f"{filename} must contain a list.")

        for record in data:
            if not isinstance(record, dict):
                raise ValueError(
                    f"{filename} must contain dictionaries inside the list."
                )

        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        raise ValueError(
            f"{filename} contains invalid JSON. Please check the file."
        )

def get_recipients():
    return read_data(recipient_data_storage)


def get_donors():
    return read_data(donor_data_storage)


def get_requests():
    return read_data(request_data_storage)

# Check existing ID
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
def save_data(filename, data):
    # Convert before opening any file for writing.
    content = json.dumps(data, indent=4)

    temporary_file = filename + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        file.write(content)

    # Replace the original only after writing finishes.
    os.replace(temporary_file, filename)


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
    save_data(request_data_storage, requests)