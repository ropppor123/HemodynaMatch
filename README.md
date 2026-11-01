# HemodynaMatch

**A Python-based blood transfusion compatibility and inventory management simulation.**

HemodynaMatch allows users to register recipients and donors, request blood components, find candidate components using predefined rules according to the Australian Red Cross Lifeblood guidelines, issue selected units and search inventory. It uses Streamlit for the interface, HTML/CSS for styling and JSON files for persistent storage.

## Project files
| File | Responsibility |
| --- | --- |
| `interface.py` | Entry point, navigation, forms, validation, component IDs and issue controls. |
| `function.py` | Classes, matching rules, expiry calculations, availability checks, issuing and result tables. |
| `storage.py` | JSON reading/writing, storage paths and ID lookup. |
| `requirements.py` | Antibody mapping, ABO compatibility tables, shelf lives and emergency age thresholds. |
| `style.css` | Branding, headings, backgrounds, buttons and input styling. |
| `dataStorage/recipient.json` | Registered recipients. |
| `dataStorage/donor.json` | Donor/component records and remaining units. |
| `dataStorage/requests.json` | Requests, statuses and issued-unit totals. |
`requirements.py` is a Python rules module, **not** a pip dependency file. The supplied source files do not include a `requirements.txt` dependency manifest.

## Installation and running
Install Python 3 and Streamlit. The other imported modules—`json`, `os`, `datetime` and `calendar`—are part of Python's standard library.

From a terminal in the project folder:
```bash
python3 -m pip install streamlit
python3 -m streamlit run interface.py
```

Open the local URL printed by Streamlit. If your system uses `python` rather than `python3`, substitute it in both commands. Run the application through Streamlit rather than executing `function.py` directly.

The installed Streamlit version must support the APIs used by the source, including `st.html`, keyed containers and `st.button(width="stretch")`.

The application creates `dataStorage` automatically. Missing or blank JSON files are treated as empty lists and are populated when records are saved. Existing files must contain a JSON list of dictionaries. Storage paths are relative to `storage.py`; the CSS path is relative to `interface.py`.

## How to use

### 1. Register a recipient

Select **Register Recipient** from the home page.
| Field | Expected input |
| --- | --- |
| Recipient ID | Uppercase R followed by six digits, such as `R000001`. |
| Name | First and last name; whitespace-only input is rejected. |
| Age | Integer from 0 to 120. |
| Gender | Female or Male. |
| Underlying disease | Existing conditions, separate from the request diagnosis. |
| ABO and Rh group | `O-`, `O+`, `A-`, `A+`, `B-`, `B+`, `AB-` or `AB+`. |
| Minor Blood Group or Antibodies | Zero or more supported antibody labels (including anti-K,anti-k,anti-Kpa,anti-Kpb,anti-Fya,anti-Fyb,anti-Jka,anti-Jkb |
| Previous Transfusion reaction | No or Yes. |

Click **Register New Recipient**. Duplicate recipient IDs are rejected. The latest supplied code does not collect an IAT result. Underlying disease and reaction history are stored but do not influence matching.

### 2. Register a donor and component stock

Select **Register Donor**. Enter a donor ID such as `D000001`, personal details, blood group, minor-group selections, component type, positive integer quantity and collection date.

Click **Register New Donor**. After validation, the program generates the next component ID from the largest saved numeric suffix for that component prefix.

| Component | Prefix | Example |
| --- | --- | --- |
| Packed Red Cell | PRC | PRC000001 |
| Red Cell Leucocyte Depleted | RLD | RLD000001 |
| Washed Red Cell Leucocyte Depleted | WRD | WRD000001 |
| Apheresis Platelets | APL | APL000001 |
| Pooled Platelets | PPL | PPL000001 |
| Fresh Frozen Plasma | FFP | FFP000001 |
| Cryodepleted Plasma | CRP | CRP000001 |
| Cryoprecipitate | CPP | CPP000001 |

The six-digit suffix has a maximum of 999999. Each component ID identifies an inventory record that may contain multiple units, rather than each individual unit.

The current form rejects duplicate donor IDs, so it cannot register repeat donations under the same donor ID. Donor age accepts 0–120 for simulation input; this is not a donor-eligibility assessment.

### 3. Create a component request

Select **Request Blood Components** and enter:

1. A registered recipient ID.
2. Request date and required date.
3. Urgency level.
4. Component type and number of units.
5. Diagnosis associated with the request.

The required date cannot precede the request date. Click **Create Request** to save the request and display candidates.

Results include the recipient, requested quantity, total candidate stock, stock-sufficiency message, and candidate component IDs, donor IDs, types, ABO/Rh groups, quantities and expiry dates.

### 4. Issue selected components

Select a component ID below the matching results, choose the units to issue and click **Confirm Issue**.

In the uploaded version, the quantity is editable from 1 to the smaller of the request's remaining quantity and the selected component's available stock. The backend rechecks matching, expiry and stock before deducting units.

| Request status | Meaning |
| --- | --- |
| Pending | Newly saved request awaiting issue. |
| Partially issued | Some requested units have been issued. |
| Issued | The issued total equals the requested total. |

For example, a request of 3 units can be completed by issuing 1 unit from one component and 2 from another. Each issue requires separate confirmation. The program does not automatically split requests across donors.

The active request's list index is kept in `st.session_state.current_request` so the controls remain available after widget reruns. Editing the form does not edit the saved request; click **Create Request** to create a new request. Older requests are stored, but there is no request-history selector for reopening them in a new session.

### 5. View and search inventory

Select **View inventory**.

- With no donor ID entered, the table uses the selected component type.
- Entering a donor ID searches across all component types and takes priority over the dropdown.
- Search ignores letter case and surrounding spaces: `d000003` matches `D000003`.
- Search requires the full donor ID; it is not a partial-text search.

The table displays component ID, donor ID, component type, ABO/Rh group, positive antigen labels, units, expiry date and status. Status is checked in this order: **Expired**, **Out of stock**, **Not yet collected**, otherwise **Available**.

Inventory status uses today's date. Request matching uses the request's required date.

## Matching rules implemented

The following rules describe the code's simulation behaviour, not a comprehensive clinical protocol.

### ABO compatibility

| Recipient ABO | Allowed red-cell donor ABO | Allowed plasma/cryoprecipitate donor ABO | Allowed platelet donor ABO |
| --- | --- | --- | --- |
| O | O | O, A, B, AB | O |
| A | A, O | A, AB | A |
| B | B, O | B, AB | B |
| AB | AB, A, B, O | AB | AB |

Cryodepleted Plasma follows the plasma table. Platelets use an ABO-identical-only simplification.

### Rh compatibility

Under standard matching, red cells and platelets pass when the recipient is Rh-positive or the donor is Rh-negative. Plasma and cryoprecipitate bypass Rh checking. Immediate and urgent red-cell requests use the specific policies below.

### Minor-group convention

The supported labels are `anti-K`, `anti-k`, `anti-Kpa`, `anti-Kpb`, `anti-Fya`, `anti-Fyb`, `anti-Jka` and `anti-Jkb`.

Recipient selections are stored as an antibody list. The donor form uses the same labels as a simplified simulation input: selected labels are stored as Positive for the corresponding antigen key, and unselected labels as Negative. There is no unknown state.

For example, selecting donor `anti-K` produces `"K": "Positive"`. This is an explicit simulation convention, not a medical inference of antigen status from an antibody result.

For red-cell components, a donor is rejected if a recipient antibody maps to an antigen marked Positive in the donor record. This check runs for all red-cell urgency policies. Other component types bypass it.

### Urgency
| Form option | Implemented red-cell selection |
| --- | --- |
| Immediate - Now | O-negative for females aged 50 or younger and males aged 18 or younger; otherwise O-positive only. |
| Urgent - within 10 minutes | Exactly the recipient's recorded ABO and Rh group. |
| Emergency within - 30-40 minutes | Standard ABO/Rh rules and recorded minor-group checks. |
| Non-emergency | Standard ABO/Rh rules and recorded minor-group checks. |
Non-red-cell components use standard matching regardless of urgency. The internal policy label `crossmatch_required` does not mean a laboratory crossmatch is performed. The time labels select policies; they are not timers.

### Shelf life and availability
| Component | Configured shelf life |
| --- | --- |
| Packed Red Cell | 42 days |
| Red Cell Leucocyte Depleted | 42 days |
| Washed Red Cell Leucocyte Depleted | 28 days |
| Apheresis Platelets | 7 days |
| Pooled Platelets | 7 days |
| Fresh Frozen Plasma | 12 calendar months |
| Cryodepleted Plasma | 12 calendar months |
| Cryoprecipitate | 12 calendar months |

The expiry function adds days or calendar months to the collection date. For calendar-month calculations, the day is limited to the last valid day of the target month.

A candidate must satisfy all three conditions:
- Collection date is on or before the required date.
- Required date is on or before the calculated expiry date.
- Available units are greater than zero.

Candidates are sorted by earliest expiry, but the user chooses which record to issue. Processing, thawing, storage temperature and time-of-day expiry are not modelled.

## Code organisation 
The main processing sequence is:

1. `get_recipient_for_request()` finds the registered recipient.
2. `find_matching_component()` filters by component type.
3. `find_matching_donors()` applies urgency and blood-group rules.
4. `check_availability()` checks dates and stock.
5. `display_matching()` displays the candidates.
6. `issue_component()` rechecks and updates the selected stock and saved request.

## Data storage
Dates are saved as `YYYY-MM-DD` strings using `.isoformat()` because JSON cannot directly store Python date objects.
Example request record:

```json
{
  "recipient_id": "R000001",
  "request_date": "2026-11-01",
  "required_date": "2026-11-01",
  "component_type": "Packed Red Cell",
  "emergency": "Non-emergency",
  "units": 2,
  "diagnosis": "Example simulation diagnosis",
  "status": "Pending"
}
```

The Request constructor defaults `issued_units` to zero if the field is absent. Issuing adds or updates it in the saved record. The program stores the issued total but does not keep a separate per-request history of issued component IDs.`
save_data()` writes a temporary file and replaces the original for recipient/donor registration. The uploaded `save_request()` and `issue_component()` functions write directly to their destination files. Updating donor stock and request status requires two separate file writes, not a transaction.


