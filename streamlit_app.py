import streamlit as st
from datetime import date
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
import os

st.set_page_config(page_title="Form 49A Auto Fill", layout="wide")

st.title("Form 49A - PAN Application Auto Fill")

# ---------------------------
# INPUT FORM
# ---------------------------

st.header("Applicant Details")

col1, col2, col3 = st.columns(3)
with col1:
    first_name = st.text_input("First Name")
with col2:
    middle_name = st.text_input("Middle Name")
with col3:
    last_name = st.text_input("Last Name")

name_on_card = st.text_input("Name on PAN Card")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
with col2:
    dob = st.date_input("Date of Birth")

st.header("Father's Details")

col1, col2, col3 = st.columns(3)
with col1:
    father_first = st.text_input("Father First Name")
with col2:
    father_middle = st.text_input("Father Middle Name")
with col3:
    father_last = st.text_input("Father Last Name")

st.header("Address")

flat = st.text_input("Flat / Building")
road = st.text_input("Road / Street")
city = st.text_input("City")

col1, col2, col3 = st.columns(3)
with col1:
    state = st.text_input("State")
with col2:
    pincode = st.text_input("Pincode")
with col3:
    country = st.text_input("Country", value="India")

st.header("Contact")

col1, col2 = st.columns(2)
with col1:
    mobile = st.text_input("Mobile")
with col2:
    email = st.text_input("Email")

aadhaar = st.text_input("Aadhaar Number")

st.header("Declaration")

place = st.text_input("Place")
declaration_date = st.date_input("Date", value=date.today())

agree = st.checkbox("I confirm all details are correct")

# ---------------------------
# PDF OVERLAY FUNCTION
# ---------------------------

def create_overlay(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # ⚠️ Adjust coordinates based on your PDF

    # Name
    can.drawString(100, 700, data["first_name"])
    can.drawString(250, 700, data["middle_name"])
    can.drawString(400, 700, data["last_name"])

    # Name on Card
    can.drawString(100, 660, data["name_on_card"])

    # Gender + DOB
    can.drawString(100, 620, data["gender"])
    can.drawString(200, 620, data["dob"])

    # Father's Name
    can.drawString(100, 580, data["father_first"])
    can.drawString(250, 580, data["father_middle"])
    can.drawString(400, 580, data["father_last"])

    # Address
    can.drawString(100, 520, data["flat"])
    can.drawString(100, 500, data["road"])
    can.drawString(100, 480, data["city"])

    # Contact
    can.drawString(100, 440, data["mobile"])
    can.drawString(300, 440, data["email"])

    # Aadhaar
    can.drawString(100, 400, data["aadhaar"])

    # Declaration
    can.drawString(100, 350, data["place"])
    can.drawString(300, 350, data["date"])

    can.save()
    packet.seek(0)

    return PdfReader(packet)

# ---------------------------
# MERGE FUNCTION
# ---------------------------

def fill_pdf(input_pdf, output_pdf, data):
    existing_pdf = PdfReader(open(input_pdf, "rb"))
    overlay_pdf = create_overlay(data)

    writer = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]

        if i < len(overlay_pdf.pages):
            page.merge_page(overlay_pdf.pages[i])

        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

# ---------------------------
# SUBMIT ACTION
# ---------------------------

if st.button("Generate Filled PDF"):

    if not agree:
        st.error("Please confirm declaration")
    else:
        data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "name_on_card": name_on_card,
            "gender": gender,
            "dob": str(dob),
            "father_first": father_first,
            "father_middle": father_middle,
            "father_last": father_last,
            "flat": flat,
            "road": road,
            "city": city,
            "mobile": mobile,
            "email": email,
            "aadhaar": aadhaar,
            "place": place,
            "date": str(declaration_date)
        }

        input_pdf_path = "Form49A.pdf"
        output_pdf_path = "filled_Form49A.pdf"

        if not os.path.exists(input_pdf_path):
            st.error("Form49A.pdf not found in project folder")
        else:
            fill_pdf(input_pdf_path, output_pdf_path, data)

            with open(output_pdf_path, "rb") as f:
                st.success("PDF Generated Successfully!")
                st.download_button(
                    "Download Filled Form",
                    f,
                    file_name="Form49A_filled.pdf"
                )
