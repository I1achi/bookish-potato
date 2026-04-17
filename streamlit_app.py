import streamlit as st
from datetime import date

st.set_page_config(page_title="Form 49A - PAN Application", layout="wide")

st.title("Form 49A - PAN Application Form")

# ---------------------------
# 1. AO CODE
# ---------------------------
st.header("1. AO Code")

col1, col2, col3, col4 = st.columns(4)
with col1:
    area_code = st.text_input("Area Code")
with col2:
    ao_type = st.text_input("AO Type")
with col3:
    range_code = st.text_input("Range Code")
with col4:
    ao_number = st.text_input("AO Number")

# ---------------------------
# 2. FULL NAME
# ---------------------------
st.header("2. Full Name")

col1, col2, col3 = st.columns(3)
with col1:
    last_name = st.text_input("Last Name / Surname")
with col2:
    first_name = st.text_input("First Name")
with col3:
    middle_name = st.text_input("Middle Name")

# ---------------------------
# 3. NAME ON CARD
# ---------------------------
st.header("3. Name to be Printed on Card")

name_on_card = st.text_input("Full Name (as to be printed on PAN Card)")

# ---------------------------
# 4. GENDER + DOB
# ---------------------------
st.header("4. Gender & Date of Birth")

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("Gender", ["Male", "Female", "Other"])
with col2:
    dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1))

# ---------------------------
# 5. FATHER'S NAME
# ---------------------------
st.header("5. Father's Name")

col1, col2, col3 = st.columns(3)
with col1:
    father_last = st.text_input("Father's Last Name")
with col2:
    father_first = st.text_input("Father's First Name")
with col3:
    father_middle = st.text_input("Father's Middle Name")

# ---------------------------
# 6. ADDRESS
# ---------------------------
st.header("6. Address")

address_type = st.radio("Address Type", ["Residence", "Office"])

flat = st.text_input("Flat/Door/Block No.")
premises = st.text_input("Name of Premises/Building")
road = st.text_input("Road/Street/Lane")
area = st.text_input("Area/Locality")

col1, col2, col3 = st.columns(3)
with col1:
    city = st.text_input("Town/City/District")
with col2:
    state = st.text_input("State/UT")
with col3:
    pincode = st.text_input("Pincode")

country = st.text_input("Country", value="India")

# ---------------------------
# 7. CONTACT DETAILS
# ---------------------------
st.header("7. Contact Details")

col1, col2 = st.columns(2)
with col1:
    mobile = st.text_input("Mobile Number")
with col2:
    email = st.text_input("Email ID")

# ---------------------------
# 8. STATUS OF APPLICANT
# ---------------------------
st.header("8. Status of Applicant")

status = st.selectbox(
    "Select Status",
    [
        "Individual",
        "Company",
        "HUF",
        "Firm",
        "AOP",
        "Trust",
        "LLP",
        "Local Authority",
        "Government"
    ]
)

# ---------------------------
# 9. AADHAAR
# ---------------------------
st.header("9. Aadhaar Details")

aadhaar = st.text_input("Aadhaar Number (Optional)")

# ---------------------------
# 10. DECLARATION
# ---------------------------
st.header("10. Declaration")

place = st.text_input("Place")
declaration_date = st.date_input("Date", value=date.today())

agree = st.checkbox("I declare that the information given is true")

# ---------------------------
# SUBMIT BUTTON
# ---------------------------
if st.button("Submit Form"):
    if not agree:
        st.error("You must accept the declaration")
    else:
        data = {
            "AO Code": {
                "Area": area_code,
                "Type": ao_type,
                "Range": range_code,
                "Number": ao_number
            },
            "Name": {
                "Last": last_name,
                "First": first_name,
                "Middle": middle_name
            },
            "Name on Card": name_on_card,
            "Gender": gender,
            "DOB": str(dob),
            "Father Name": {
                "Last": father_last,
                "First": father_first,
                "Middle": father_middle
            },
            "Address": {
                "Type": address_type,
                "Flat": flat,
                "Premises": premises,
                "Road": road,
                "Area": area,
                "City": city,
                "State": state,
                "Pincode": pincode,
                "Country": country
            },
            "Contact": {
                "Mobile": mobile,
                "Email": email
            },
            "Status": status,
            "Aadhaar": aadhaar,
            "Declaration": {
                "Place": place,
                "Date": str(declaration_date)
            }
        }

        st.success("Form Submitted Successfully!")
        st.json(data)
