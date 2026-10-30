import streamlit as st # Streamlit as Interface
import storage as s # Import storage.py
import function as f # Import function.py
import requirements as r # Imoport requirements.py

# Setup CSS
st.set_page_config(
    page_title = "Transfusion System",
    layout = "wide")

def load_css():
    with open("style.css", "r", encoding="utf-8") as file:
        st.html(f"<style>{file.read()}</style>")

load_css()

# CSS 
def display_header():
    st.html("""
            <div class="home_header">
                <span class="home_header_name">
                    HemodynaMatch<span style="color: #BA221E;">.</span>
                </span>
                <span class="home_header_myname">
                    |  Panicha Vongthoytong M.D.
                </span>
            </div>
    """)

def display_page_title(title, accent):
    st.html(f"""
        <section class="home_main section_title">
            <h1 style="font-size: clamp(1rem, 3.25vw, 2.75rem); max-width: none; text-align: center;"><span class="section_title_black">{title}</span><em>{accent}.</em></h1>
        </section>
    """)

# ID
def check_recipient_id(id):
    if (len(id) != 7) or (id[0] != "R") or (not id[1:].isdigit()):
        return f"Invalid Recipient ID" 

def check_donor_id(id):
    if (len(id) != 7) or (not id[0] == "D") or (not id[1:].isdigit()):
        return f"Invalid Donor ID" 

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
def change_page(page):
    st.session_state.page = page

# Main Page
def main_page():
    if "page" not in st.session_state:
        st.session_state.page = None

    # Show the same branding above every page.
    display_header()

    if st.session_state.page is None:
        st.html("""
            <section class="home_main">
                <div class="home_eyebrow">Transfusion system simulation</div>

                <h1>
                    Hemodyna<em>Match.</em>
                </h1>

                <p class="home_description">
                    A Python-Based Blood Transfusion Compatibility and Inventory Management System.
                </p>

                <div class="home_shape" aria-hidden="true"></div>
            </section>

            <div class="home_section_label">Choose the page</div> """)

        with st.container(key="home_navigation"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.button(
                    "01   Register Recipient →",
                    key="home_recipient",
                    on_click=change_page,
                    args=("New Recipient Registeration",),
                    width="stretch"
                )
            with col2:
                st.button(
                    "02   Register Donor →",
                    key="home_donor",
                    on_click=change_page,
                    args=("New Donor Registeration",),
                    width="stretch"
                )
            with col3:
                st.button(
                    "03   Request Blood Components →",
                    key="home_request",
                    on_click=change_page,
                    args=("Blood Component Request",),
                    width="stretch"
                )
            with col4:
                st.button(
                    "04   View inventory →",
                    key="home_inventory",
                    on_click=change_page,
                    args=("Inventory",),
                    width="stretch"
                )
    else:
        st.button(
                    "← Back to main page",
                    on_click=change_page,
                    args=(None,)
                )

        if st.session_state.page == "New Recipient Registeration":
            recipient_page()

        elif st.session_state.page == "New Donor Registeration":
            donor_page()

        elif st.session_state.page == "Blood Component Request":
            request_page()

        elif st.session_state.page == "Inventory":
            inventory_page()

    # Full-width footer after the content of every page.
    st.html("""
        <div class="home_footer">
            <span>Educational simulation · Not for clinical use</span>
        </div>
    """)


# Recipient Page
def recipient_page():
    display_page_title("Register ", "Recipient")
    
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
                                "anti-Kpa", "anti-Kpb",
                               "anti-Fya", "anti-Fyb",
                                "anti-Jka", "anti-Jkb"])
    reaction_history = st.selectbox("Previous Transfusion reaction", ["No", "Yes"])

    # Register botton
    if st.button("Register New Recipient", key="submit_recipient"):
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
    
# Donor Page
def donor_page():
    display_page_title("Register ", "Donor")
    
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
                                "anti-Kpa", "anti-Kpb",
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
    
    # Convert selected antibody-style labels into antigen dictionary keys.
    minor_blood = {
        antigen: "Positive" if antibody in minor_blood else "Negative"
        for antibody, antigen in r.ANTIBODY_TO_ANTIGEN.items()}

    # Button
    if st.button("Register New Donor", key="submit_donor"):
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

# Blood component request page
def request_page():
    display_page_title("Blood Component Request Form ", "")

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
    if st.button("Create Request", key="submit_request"):
        error = check_recipient_id(recipient_id)

        if error is not None:
            st.error(error)
        # Recipient who request for the component must be registered first.
        elif not s.recipient_id_exist(recipient_id):
            st.error("Recipient not found. Please register first.")
        # Required date must not proceed request date 
        elif required_date < request_date:
            st.error("Required Date cannot be earlier than Request Date.")
        else:
            request_data = {
                "recipient_id": recipient_id,
                "request_date": request_date.isoformat(),
                "required_date": required_date.isoformat(),
                "component_type": component_type,
                "emergency": emergency,
                "units": units,
                "diagnosis": diagnosis,
                "status": "Pending"}

            # SAVE REQUEST to json file
            s.save_request(request_data)
            st.success("Request saved succesfully.")

            # Call the display
            request = f.Request(**request_data)
            f.display_matching(request)

# Inventory page
def inventory_page():
    display_page_title("Inventory", "")
    f.display_inventory()

if __name__ == "__main__":
    main_page()