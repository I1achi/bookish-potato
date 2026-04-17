import streamlit as st
from datetime import datetime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
import os

st.set_page_config(page_title="Form 49A Auto Fill", layout="wide")

st.title("Form 49A - PAN Application")

# ---------------------------
# INPUTS (NO CHECKBOX / NO DEFAULT DATE)
# ---------------------------

st.header("Applicant Name")

col1, col2, col3 = st.columns(3)
with col1:
    first_name = st.text_input("First Name").upper()
with col2:
    middle_name = st.text_input("Middle Name").upper()
with col3:
    last_name = st.text_input("Last Name").upper()

name_on_card = st.text_input("Name on PAN Card").upper()

st.header("Gender & DOB")

gender = st.text_input("Gender (M/F/O)").upper()

dob_input = st.text_input("Date of Birth (DD/MM/YYYY)")
dob = dob_input if dob_input else ""

st.header("Father Name")

col1, col2, col3 = st.columns(3)
with col1:
    father_first = st.text_input("Father First Name").upper()
with col2:
    father_middle = st.text_input("Father Middle Name").upper()
with col3:
    father_last = st.text_input("Father Last Name").upper()

st.header("Address")

flat = st.text_input("Flat / Building").upper()
road = st.text_input("Road").upper()
city = st.text_input("City").upper()

st.header("Contact")

mobile = st.text_input("Mobile")
email = st.text_input("Email").upper()

aadhaar = st.text_input("Aadhaar Number")

st.header("Declaration")

place = st.text_input("Place").upper()
date_input = st.text_input("Date (DD/MM/YYYY)")
decl_date = date_input if date_input else ""

# ---------------------------
# HELPER: DRAW BOX TEXT
# ---------------------------

def draw_boxes(can, text, x, y, box_width=12, gap=2):
    """
    Draw each character in separate box spacing
    """
    for i, char in enumerate(text):
        can.drawString(x + i * (box_width + gap), y, char)

# ---------------------------
# PDF OVERLAY
# ---------------------------

def create_overlay(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.setFont("Helvetica", 9.5)

    # ⚠️ Adjust coordinates EXACTLY as per PDF

    # First Name (boxes)
    draw_boxes(can, data["first_name"], 195, 589)

    # Middle Name
    draw_boxes(can, data["middle_name"], 195, 574)

    # Last Name
    draw_boxes(can, data["last_name"], 195, 604)

    # Name on Card
    draw_boxes(can, data["name_on_card"], 100, 630)

    # Gender
    draw_boxes(can, data["gender"], 100, 600)

    # DOB
    draw_boxes(can, data["dob"], 200, 600)

    # Father Name
    draw_boxes(can, data["father_first"], 100, 570)
    draw_boxes(can, data["father_middle"], 100, 550)
    draw_boxes(can, data["father_last"], 100, 530)

    # Address
    draw_boxes(can, data["flat"], 100, 500)
    draw_boxes(can, data["road"], 100, 480)
    draw_boxes(can, data["city"], 100, 460)

    # Contact
    draw_boxes(can, data["mobile"], 100, 430)
    draw_boxes(can, data["email"], 100, 410)

    # Aadhaar
    draw_boxes(can, data["aadhaar"], 100, 380)

    # Declaration
    draw_boxes(can, data["place"], 100, 350)
    draw_boxes(can, data["date"], 300, 350)

    can.save()
    packet.seek(0)

    return PdfReader(packet)

# ---------------------------
# MERGE PDF
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
# SUBMIT
# ---------------------------

if st.button("Generate PDF"):

    data = {
        "first_name": first_name.replace(" ", ""),
        "middle_name": middle_name.replace(" ", ""),
        "last_name": last_name.replace(" ", ""),
        "name_on_card": name_on_card.replace(" ", ""),
        "gender": gender,
        "dob": dob.replace("/", ""),
        "father_first": father_first.replace(" ", ""),
        "father_middle": father_middle.replace(" ", ""),
        "father_last": father_last.replace(" ", ""),
        "flat": flat.replace(" ", ""),
        "road": road.replace(" ", ""),
        "city": city.replace(" ", ""),
        "mobile": mobile,
        "email": email.replace(" ", ""),
        "aadhaar": aadhaar,
        "place": place.replace(" ", ""),
        "date": decl_date.replace("/", "")
    }

    input_pdf = "Form49A.pdf"
    output_pdf = "filled_Form49A.pdf"

    if not os.path.exists(input_pdf):
        st.error("Form49A.pdf not found")
    else:
        fill_pdf(input_pdf, output_pdf, data)

        with open(output_pdf, "rb") as f:
            st.success("PDF Generated")
            st.download_button("Download", f, "Form49A_filled.pdf")
