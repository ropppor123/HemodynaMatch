import json

recipient_data_storage = "dataStorage/recipient.json"
donor_data_storage = "dataStorage/donor.json"
request_data_storage = "dataStorage/requests.json"

# Get Recipient, Donor, Requests data
def get_recipients():
    try:
        with open(recipient_data_storage, "r", encoding="utf-8") as file:
            content = file.read()

        # A blank file means no recipients yet
        if not content.strip():
            return []

        recipients = json.loads(content)

        if not isinstance(recipients, list):
            raise ValueError("recipient.json must contain a list: [] or [{...}]")

        return recipients

    except FileNotFoundError:
        return []

def get_donors():
    try:
        with open(donor_data_storage, "r", encoding="utf-8") as file:
            content = file.read()

        # A blank file
        if not content.strip():
            return []

        donors = json.loads(content)

        if not isinstance(donors, list):
            raise ValueError("donor.json must contain a list: [] or [{...}]")

        return donors

    except FileNotFoundError:
        return []

def get_requests():
    try:
        with open(request_data_storage, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            return []

        requests = json.loads(content)

        if not isinstance(requests, list):
            raise ValueError("request.json must contain a list")

        return requests

    except FileNotFoundError:
        return []

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
def save_recipient(recipient_data):
    recipients = get_recipients()
    recipients.append(recipient_data)

    with open(recipient_data_storage, "w") as file:
        json.dump(recipients, file, indent = 4)

def save_donor(donor_data):
    donors = get_donors()
    donors.append(donor_data)

    with open(donor_data_storage, "w") as file:
        json.dump(donors, file, indent = 4)

def save_request(request_data):
    requests = get_requests()
    requests.append(request_data)

    # Convert to JSON before opening the file for writing
    content = json.dumps(requests, indent=4)

    with open(request_data_storage, "w", encoding="utf-8") as file:
        file.write(content)

