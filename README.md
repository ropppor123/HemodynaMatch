# HemodynaMatch
A Python-Based Blood Transfusion Compatibility and Inventory Management System.

# File	Responsibility
interface.py	| Entry point, navigation, forms, validation, component IDs and issue controls.
function.py	| Classes, matching rules, expiry calculations, availability checks, issuing and result tables.
storage.py	| JSON reading/writing, storage paths and ID lookup.
requirements.py	| Antibody mapping, ABO compatibility tables, shelf lives and emergency age thresholds.
style.css	| Branding, headings, backgrounds, buttons and input styling.
dataStorage/recipient.json	| Registered recipients.
dataStorage/donor.json	| Donor/component records and remaining units.
dataStorage/requests.json	| Requests, statuses and issued-unit totals.

# Installation and running
Install Python 3 and Streamlit. The other imported modules—`json`, os, datetime and calendar—are part of Python's standard library.

From a terminal in the project folder:
python3 -m pip install streamlit
python3 -m streamlit run interface.py

Open the local URL printed by Streamlit. If your system uses python rather than python3, substitute it in both commands. Run the application through Streamlit rather than executing function.py directly.

The installed Streamlit version must support the APIs used by the source, including st.html, keyed containers and st.button(width="stretch").

The application creates dataStorage automatically. Missing or blank JSON files are treated as empty lists and are populated when records are saved. Existing files must contain a JSON list of dictionaries. Storage paths are relative to storage.py; the CSS path is relative to interface.py.

