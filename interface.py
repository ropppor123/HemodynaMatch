import streamlit as st # Streamlit as Interface
import storage as s # Import storage.py
import function as f # Import function.py

# ID
def check_recipient_id(id):
    if (len(id) != 7) or (id[0] != "R") or (not id[1:].isdigit()):
        return f"Invalid Recipient ID\n" f"ID must follow R000000 format"

def check_donor_id(id):
    if (len(id) != 7) or (not id[0] == "D") or (not id[1:].isdigit()):
        return f"Invalid Donor ID\n" f"ID must follow D000000 format"

def generate_component_id(component_type:str) -> str:
    # Component letter code
    if component_type == "Packed Red Cell":
        letter_code = "PRC"
    elif component_type == "Red Cell Leucocyte Depleted":
        letter_code = "RLD"
    elif component_type == "Washed Red Cell Leucocyte Depleted":
        letter_code = "WRD"
    elif component_type == "Apheresis Platelets":
        letter_code = "APL"
    elif component_type == "Pooled Platelets":
        letter_code = "PPL"
    elif component_type == "Fresh Frozen Plasma":
        letter_code = "FFP"    
    elif component_type == "Cryodepleted Plasma":
        letter_code = "CRP" 
    elif component_type == "Cryoprecipitate":
        letter_code = "CPP"
    else:
        raise ValueError("Unknown component type")
    
    # 6 digits code
    if "component_counter" not in st.session_state:
        st.session_state.component_counter = 0 #start with 0
    if st.session_state.component_counter >= 999999:
        raise ValueError("Component ID limit reached")
    st.session_state.component_counter +=1 # add by one

    component_id = f"{letter_code}{st.session_state.component_counter:06d}"
    #:06d Format the integer as six digits, adding leading zeros

    return component_id

# ALL PAGES
def main_page():
    # Main page set up
    if "page" not in st.session_state:
        st.session_state.page = None
    
    # Main page, showing title and page choices
    if st.session_state.page is None:
        st.title("Transfusion System Simulation")
        choice = st.selectbox("Choose a page",
                            [   
                                "Main Page",
                                "New Recipient Registeration",
                                "New Donor Registeration",
                                "Blood Component Request",
                                "Inventory"
                            ])
        # Choose a page = on the same main page
        # Not choose a page >> leads to specific choosen page
        if choice != "Main Page":
            st.session_state.page = choice
            st.rerun()
    # New Recipient Registeration
    elif st.session_state.page == "New Recipient Registeration":
        if st.button("Back to main page"):
            st.session_state.page = None
            st.rerun()
        recipient_page()
    # New Donor Registeration
    elif st.session_state.page == "New Donor Registeration":
        if st.button("Back to main page"):
            st.session_state.page = None
            st.rerun()
        donor_page()
    # Blood Component Request
    elif st.session_state.page == "Blood Component Request":
        if st.button("Back to main page"):
            st.session_state.page = None
            st.rerun()
        request_page()
    # Inventory
    elif st.session_state.page == "Inventory":
        if st.button("Back to main page"):
            st.session_state.page = None
            st.rerun()
        inventory_page()

def recipient_page():
    st.title("New Recipient Registeration")
    
    # Recipient details 
    id = st.text_input("Recipient ID Example R000000  (R + 6 digits)")
    name = st.text_input("First name and Last name")
    age = st.number_input("Age", min_value = 0, max_value = 120, step = 1)
    gender = st.selectbox("Gender", ["Female", "Male"])
    underlying_disease = st.text_input("Underlying Disease")
    major_blood = st.selectbox("ABO and Rh Blood Group", 
                                ["O-","O+","A-","A+", "B-","B+","AB-", "AB+"])
    minor_blood = st.multiselect ("Minor Blood Group or Antibodies - if none, leave this blank",
                                ["anti-K", "anti-k",
                                "anti-kpa", "anti-kpb",
                               "anti-Fya", "anti-Fyb",
                                "anti-Jka", "anti-Jkb"])
    reaction_history = st.selectbox("Previous Transfusion reaction", ["No", "Yes"])

    # Register botton
    if st.button("Register New recipient"):
        error = check_recipient_id(id)
        if error is not None:
            st.error(error)
        elif s.recipient_id_exist(id):
            st.error("Recipient ID already exists.")
        else:
            recipient_data = {"id":id,
                              "name":name, 
                              "age":age,
                              "gender": gender,
                              "underlying_disease": underlying_disease,
                              "major_blood": major_blood,
                              "minor_blood": minor_blood,
                              "reaction_history": reaction_history}

            # SAVE RECIPIENT to json file
            s.save_recipient(recipient_data)
            st.success("New recipient registered successfully") 
    

def donor_page():
    st.title("New Donor Registeration")
    
    # Donor details
    id = st.text_input("Donor ID Example D000000  (D + 6 digits)")
    name = st.text_input("First name and Last name")
    age = st.number_input("Age", min_value = 0, max_value = 120, step = 1)
    gender = st.selectbox("Gender", ["Female", "Male"])
    underlying_disease = st.text_input("Underlying Disease")
    major_blood = st.selectbox("ABO and Rh Blood Group", 
                                ["O-","O+","A-","A+", "B-","B+","AB-", "AB+"])
    minor_blood = st.multiselect ("Minor Blood Group and Antibodies - if none, leave this blank",
                                ["anti-K", "anti-k",
                                "anti-kpa", "anti-kpb",
                                "anti-Fya", "anti-Fyb",
                                "anti-Jka", "anti-Jkb"])
    
    # COMPONENET DETAILS
    component_type = st.selectbox("Blood Component Type", ["Packed Red Cell",
                                                           "Red Cell Leucocyte Depleted",
                                                           "Washed Red Cell Leucocyte Depleted",
                                                           "Apheresis Platelets",
                                                           "Pooled Platelets",
                                                           "Fresh Frozen Plasma",
                                                           "Cryodepleted Plasma",
                                                           "Cryoprecipitate"])
    component_id = generate_component_id(component_type)
    units = st.number_input("Number of Units", min_value =1, step = 1)    
    collection_date = st.date_input("Collection Date")
    
    # Convert selected antigens into a dictionary
    minor_blood = {
        antigen: "Positive" if antigen in minor_blood else "Negative"
        for antigen in ["anti-K", "anti-k", "anti-Kpa", "anti-Kpb", "anti-Fya", "anti-Fyb", "anti-Jka", "anti-Jkb"]}
    
    # Button
    if st.button("Register New Donor"):
        error = check_donor_id(id)
        if error is not None:
            st.error(error)
        elif s.donor_id_exist(id):
            st.error("Donor ID already exists.")
        else:
            donor_data = {"id":id,
                              "name":name, 
                              "age":age,
                              "gender": gender,
                              "underlying_disease": underlying_disease,
                              "major_blood": major_blood,
                              "minor_blood": minor_blood,
                              "component_id": component_id,
                              "component_type": component_type,
                              "units":units,
                              "collection_date": collection_date.isoformat()}

            # SAVE RECIPIENT to json file
            s.save_donor(donor_data)
            st.success("New Donor registered successfully") 


def request_page():
    st.title("Blood Component Request Form")

    recipient_id = st.text_input("Recipient ID (Example: R000000)")
    request_date = st.date_input("Request Date")
    required_date = st.date_input("Required Date")
    emergency = st.selectbox("Urgency", ["Immediate - Now", "Urgent - within 10 minutes", "Emergency within - 30-40 minutes", "Non-emergency"])
    component_type = st.selectbox("Blood Component Type",
        ["Packed Red Cell",
         "Red Cell Leucocyte Depleted",
         "Washed Red Cell Leucocyte Depleted",
         "Apheresis Platelets",
         "Pooled Platelets",
         "Fresh Frozen Plasma",
         "Cryodepleted Plasma",
         "Cryoprecipitate"])
    units = st.number_input(
        "Number of Units Requested",
        min_value=1,
        step=1)
    diagnosis = st.text_input("Diagnosis")
    
    # Button
    if st.button("Create Request"):
        error = check_recipient_id(recipient_id)


        if error is not None:
            st.error(error)
        elif not s.recipient_id_exist(recipient_id):
            st.error("Recipient not found. Please register first.")
        else:
            request_data = {
                "recipient_id": recipient_id,
                "request_date": request_date.isoformat(),
                "required_date": required_date.isoformat(),
                "component_type": component_type,
                "emergency": emergency,
                "units": units,
                "diagnosis": diagnosis,
                "status": "Pending"
            }

            # SAVE REQUEST to json file
            s.save_request(request_data)
            st.success("Request created for this session.")

            # Call the display
            request = f.Request(**request_data)
            f.display_matching(request)


def inventory_page():
    st.title("Inventory")
    f.display_inventory()

if __name__ == "__main__":
    main_page()