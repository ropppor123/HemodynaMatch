import storage as s 
import requirements as r
from datetime import date, timedelta
import calendar
import streamlit as st

class Recipient:
    def __init__(self, 
                 id: str, 
                 name: str, 
                 age: int, 
                 gender: str,
                 underlying_disease: str,
                 major_blood: str,
                 minor_blood: list,
                 reaction_history: str):
    
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.underlying_disease = underlying_disease
        self.major_blood = major_blood
        self.minor_blood = minor_blood
        self.reaction_history = reaction_history

class Donor:
    def __init__(self, 
                 id: str, 
                 name: str, 
                 age: int, 
                 gender: str,
                 underlying_disease: str,
                 major_blood: str,
                 minor_blood: dict,
                 component_id: str,
                 component_type:str,
                 units: int,
                 collection_date:str):
    
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.underlying_disease = underlying_disease
        self.major_blood = major_blood
        self.minor_blood = minor_blood
        self.component_id = component_id
        self.component_type = component_type
        self.units = units
        self.collection_date = collection_date

    def matches_component_type(self, component_type):
        return self.component_type == component_type

class Request:
    def __init__(self, 
                 recipient_id,
                 request_date, 
                 required_date, 
                 component_type, 
                 emergency, 
                 units, 
                 diagnosis, 
                 status):
        
        self.recipient_id = recipient_id
        self.request_date = request_date
        self.required_date = required_date
        self.component_type = component_type
        self.emergency = emergency
        self.units = units
        self.diagnosis = diagnosis
        self.status = status


# STEP 1: Create recipient, donor and request object from recipinet.json via get_recipinets()
def get_recipient_objects():
    return [Recipient(**data) for data in s.get_recipients()]

def get_donor_objects():
    return [Donor(**data) for data in s.get_donors()]

def get_request_objects():
    return [Request(**data) for data in s.get_requests()]


# STEP 2: Filter data
# 2.1 Use the current request's recipient_id to find this particular recipient in recipient.json
def get_recipient_for_request(request):
    for recipient in get_recipient_objects():
        if recipient.id == request.recipient_id:
            return recipient
    raise ValueError("Recipient not found")

# 2.2: Filter donor by requested component
def find_matching_component(request):
    recipient = get_recipient_for_request(request) # object
    donors = get_donor_objects() 

    matching_donors_by_component = []
    
    for donor in donors:
        if donor.matches_component_type(request.component_type):
            matching_donors_by_component.append(donor)
    
    return recipient, matching_donors_by_component
    # recipient as an object, matching_donors_by_component as a list


# STEP 3 : Check compatibility according to the requirements in requirements.py
# 3.1: Check ABO major_group compatibility
def check_abo(recipient, donor):
    # "AB+" becomes "AB"; "O-" becomes "O"
    recipient_abo = recipient.major_blood[:-1]
    donor_abo = donor.major_blood[:-1]

    # Red cell component
    if donor.component_type in [
        "Packed Red Cell",
        "Red Cell Leucocyte Depleted",
        "Washed Red Cell Leucocyte Depleted"
    ]:
        return donor_abo in r.RED_CELL_ABO[recipient_abo]
    # Plasma and Cryoprecipitate components
    elif donor.component_type in [
        "Fresh Frozen Plasma",
        "Cryodepleted Plasma",
        "Cryoprecipitate"
    ]:
        return donor_abo in r.PLASMA_ABO[recipient_abo]
    # Platelet components
    elif donor.component_type in [
        "Apheresis Platelets",
        "Pooled Platelets"
    ]:
        # Simplified policy: only select ABO-identical platelets! >> No additional function for platelet
        return donor_abo == recipient_abo

    raise ValueError("Unknown component type")

# 3.2: Check Rh major_group compatibility
def check_rh(recipient, donor):
    recipient_rh = recipient.major_blood[-1]
    donor_rh = donor.major_blood[-1]

    if donor.component_type in [
        "Fresh Frozen Plasma",
        "Cryodepleted Plasma",
        "Cryoprecipitate"
    ]:
        return True
    elif donor.component_type in [
        "Packed Red Cell",
        "Red Cell Leucocyte Depleted",
        "Washed Red Cell Leucocyte Depleted",
        "Apheresis Platelets",
        "Pooled Platelets"
    ]:
        return recipient_rh == "+" or donor_rh == "-"

    raise ValueError(f"Unknown component type: {donor.component_type}")

# 3.3: Check minor group compatibility
def check_minor_blood(recipient, donor):
    for antibody in recipient.minor_blood:
        antigen = r.ANTIBODY_TO_ANTIGEN[antibody]

        if donor.minor_blood[antigen] == "Positive":
            return False
    return True


# STEP 4: Check emergency
def check_emergency(request, recipient):
    red_cell_types = [
        "Packed Red Cell",
        "Red Cell Leucocyte Depleted",
        "Washed Red Cell Leucocyte Depleted"]

    if request.component_type not in red_cell_types:
        return "standard_component_matching"

    if request.emergency == "Immediate - Now":
        age_limit = r.EMERGENCY_O_NEGATIVE_MAX_AGE.get(
            recipient.gender)

        if age_limit is None:
            raise ValueError("Emergency Rh selection requires review")

        if recipient.age <= age_limit:
            return "emergency_O_negative"

        return "emergency_O_positive"

    elif request.emergency == "Urgent - within 10 minutes":
        return "confirmed_group_specific"

    elif request.emergency in [
        "Emergency within - 30-40 minutes",
        "Non-emergency"]:
        return "crossmatch_required"

    raise ValueError(f"Unknown urgency: {request.emergency}")

# STEP 5: Find matching
def find_matching_donors(request):
    recipient, component_matches = find_matching_component(request)
    
    policy = check_emergency(request,recipient)
    matching_donors = []

    red_cell_types = [
        "Packed Red Cell",
        "Red Cell Leucocyte Depleted",
        "Washed Red Cell Leucocyte Depleted"]

    for donor in component_matches:
        if policy == "emergency_O_negative":
            if donor.major_blood != "O-":
                continue
        elif policy == "emergency_O_positive":
            if donor.major_blood != "O+":
                continue
        elif policy == "confirmed_group_specific":
            # Match the recipient's recorded ABO and Rh exactly.
            if donor.major_blood != recipient.major_blood:
                continue
        else:
            # Standard matching for other requests.
            if not check_abo(recipient, donor):
                continue

            if not check_rh(recipient, donor):
                continue
        
        # Check recorded antibodies for all red-cell candidates.
        if donor.component_type in red_cell_types:
            if not check_minor_blood(recipient, donor):
                continue
        matching_donors.append(donor)
    return recipient, matching_donors


# STEP 6: Check availability
# 6.1 Calculate expiry date
def calculate_expiry(donor):
    collection_date = date.fromisoformat(donor.collection_date)
    shelf_life = r.SHELF_LIFE[donor.component_type]

    if "days" in shelf_life:
        return collection_date + timedelta(days=shelf_life["days"])

    if "months" in shelf_life:
        total_months = (
            collection_date.year * 12
            + collection_date.month - 1
            + shelf_life["months"]
        )

        year, month_index = divmod(total_months, 12)
        month = month_index + 1

        last_day = calendar.monthrange(year, month)[1]
        day = min(collection_date.day, last_day)

        return date(year, month, day)

    raise ValueError("Shelf life must specify days or months")

# 6.2 Check expiry date
def check_expiry(donor, request):
    required_date = date.fromisoformat(request.required_date)
    return required_date > calculate_expiry(donor)

# 6.3 Check total units across available donor records
def check_units(available_donors, request):
    total_units = sum(donor.units for donor in available_donors)
    return total_units >= request.units

# 6.4 Combine availability checks
def check_availability(request):
    if request.units <= 0:
        raise ValueError("Requested units must be greater than zero")

    recipient, matching_donors = find_matching_donors(request)
    required_date = date.fromisoformat(request.required_date)

    available_donors = []

    for donor in matching_donors:
        collection_date = date.fromisoformat(donor.collection_date)

        if collection_date > required_date:
            continue

        if check_expiry(donor, request):
            continue

        if donor.units <= 0:
            continue

        available_donors.append(donor)

    # Components expiring soonest appear first
    available_donors.sort(key=calculate_expiry)

    enough_units = check_units(available_donors, request)

    return recipient, available_donors, enough_units


# DISPLAYS
def display_matching(request):
    recipient, available_donors, enough_units = check_availability(request)

    st.subheader("Matching Results")
    st.write(f"Recipient: {recipient.id} — {recipient.name}")

    total_units = sum(donor.units for donor in available_donors)

    if not available_donors:
        st.error("No matching candidates available.")
        return
    if enough_units:
        st.success("Matching candidates found with sufficient stock.")
    else:
        st.warning("Review required: matching candidates have insufficient stock.")

    st.write(
        f"Requested: {request.units} units | Available: {total_units} units")

    rows = []

    for donor in available_donors:
        rows.append({
            "Component ID": donor.component_id,
            "Donor ID": donor.id,
            "Component Type": donor.component_type,
            "ABO Rh": donor.major_blood,
            "Available Units": donor.units,
            "Expiry Date": calculate_expiry(donor)
        })

    st.dataframe(rows)
    st.caption("Candidate screening results; not final transfusion approval.")

# Display inventory 
def display_inventory():
    donors = get_donor_objects()

    if not donors:
        st.info("No components in inventory.")
        return

    component_types = sorted({
        donor.component_type for donor in donors})

    selected_type = st.selectbox(
        "Choose blood component type",
        component_types)

    # Search donor ID
    search_donor_id = st.text_input(
        "Search by Donor ID",
        placeholder="Example: D000001"
    ).strip().upper()

    today = date.today()
    rows = []

    for donor in donors:
        if search_donor_id:
            if donor.id.strip().upper() != search_donor_id:
                continue
        elif donor.component_type != selected_type:
            continue

        expiry_date = calculate_expiry(donor)

        positive_antigens = [
            antigen
            for antigen, result in donor.minor_blood.items()
            if result == "Positive"]
        
        if today > expiry_date:
            status = "Expired"
        elif donor.units <= 0:
            status = "Out of stock"
        elif date.fromisoformat(donor.collection_date) > today:
            status = "Not yet collected"
        else:
            status = "Available"

        rows.append({"Component ID": donor.component_id,
                    "Donor ID": donor.id,
                    "Component Type": donor.component_type,
                    "ABO Rh": donor.major_blood,
                    "Positive Antigens": ", ".join(positive_antigens) or "None",
                    "Units": donor.units,
                    "Expiry Date": expiry_date,
                    "Status": status})

    if rows:
        st.dataframe(rows, hide_index=True)
    elif search_donor_id:
        st.info("No inventory records found for this donor ID.")
    else:
        st.info("No records found for the selected component type.")
