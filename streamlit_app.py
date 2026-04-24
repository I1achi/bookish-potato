import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
import io
import os

DEBUG_BOXES = True

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Form 49A Auto Fill", layout="wide")
st.title("Form 49A - PAN Application")

# ---------------------------
# FORM CONFIG (EDIT HERE ONLY)
# ---------------------------
FORM_CONFIG = {
    "name_section": {
        "first_name": (195, 589),
        "middle_name": (195, 574),
        "last_name": (195, 604),
        "name_on_card": (100, 630)
    },
    "personal_section": {
        "gender": (100, 600),
        "dob": (200, 600)
    },
    "father_section": {
        "father_first": (100, 570),
        "father_middle": (100, 550),
        "father_last": (100, 530)
    },
    "address_section": {
        "flat": (100, 500),
        "road": (100, 480),
        "city": (100, 460)
    },
    "contact_section": {
        "mobile": (100, 430),
        "email": (100, 410)
    },
    "aadhaar_section": {
        "aadhaar": (100, 380)
    },
    "declaration_section": {
        "place": (100, 350),
        "date": (300, 350)
    }
}

# ---------------------------
# INPUT UI
# ---------------------------

st.header("Applicant Name")
c1, c2, c3 = st.columns(3)
first_name = c1.text_input("First Name")
middle_name = c2.text_input("Middle Name")
last_name = c3.text_input("Last Name")

name_on_card = st.text_input("Name on PAN Card")

st.header("Personal")
gender = st.text_input("Gender (M/F/O)")
dob = st.text_input("DOB (DD/MM/YYYY)")

st.header("Father Name")
c1, c2, c3 = st.columns(3)
father_first = c1.text_input("Father First Name")
father_middle = c2.text_input("Father Middle Name")
father_last = c3.text_input("Father Last Name")

st.header("Address")
flat = st.text_input("Flat / Building")
road = st.text_input("Road")
city = st.text_input("City")

st.header("Contact")
mobile = st.text_input("Mobile")
email = st.text_input("Email")
aadhaar = st.text_input("Aadhaar")

st.header("Declaration")
place = st.text_input("Place")
decl_date = st.text_input("Date (DD/MM/YYYY)")

# ---------------------------
# DATA CLEANING
# ---------------------------
def clean_data(raw):
    return {
        k: str(v).upper().replace(" ", "").replace("/", "")
        for k, v in raw.items()
    }

# ---------------------------
# DRAW FUNCTION (BOX TEXT)
# ---------------------------
from reportlab.pdfbase import pdfmetrics

def draw_boxes(can, text, x, y, step=13.7, box_height=14):
    font_name = "Helvetica"
    font_size = 9.5

    for i, char in enumerate(text):
        box_x = x + i * step
        box_y = y

        # 🟦 DRAW BOX OUTLINE (DEBUG)
        if DEBUG_BOXES:
            can.setStrokeColorRGB(1, 0, 0)  # red border
            can.rect(box_x, box_y, step, box_height, stroke=1, fill=0)

        # Character width
        char_width = pdfmetrics.stringWidth(char, font_name, font_size)

        # Center alignment
        x_pos = box_x + (step - char_width) / 2 + 0.5
        y_pos = box_y + 2

        # Text color
        can.setFillColor(colors.darkblue)

        can.drawString(x_pos, y_pos, char)
        
# ---------------------------
# SECTION RENDERER
# ---------------------------
def render_section(can, section_config, data):
    for field, (x, y) in section_config.items():
        value = data.get(field, "")
        draw_boxes(can, value, x, y)

# ---------------------------
# CREATE OVERLAY
# ---------------------------
def create_overlay(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)

    # Font + Color
    can.setFont("Helvetica", 9.5)
    can.setFillColor(colors.darkblue)

    # Render all sections
    for section in FORM_CONFIG.values():
        render_section(can, section, data)

    can.save()
    packet.seek(0)
    return PdfReader(packet)

# ---------------------------
# MERGE PDF
# ---------------------------
def fill_pdf(input_pdf, output_pdf, data):
    base_pdf = PdfReader(open(input_pdf, "rb"))
    overlay = create_overlay(data)

    writer = PdfWriter()

    for i in range(len(base_pdf.pages)):
        page = base_pdf.pages[i]
        if i < len(overlay.pages):
            page.merge_page(overlay.pages[i])
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

# ---------------------------
# SUBMIT
# ---------------------------
if st.button("Generate PDF"):

    raw_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "name_on_card": name_on_card,
        "gender": gender,
        "dob": dob,
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
        "date": decl_date
    }

    data = clean_data(raw_data)

    input_pdf = "Form49A.pdf"
    output_pdf = "filled_Form49A.pdf"

    if not os.path.exists(input_pdf):
        st.error("Form49A.pdf not found")
    else:
        fill_pdf(input_pdf, output_pdf, data)

        with open(output_pdf, "rb") as f:
            st.success("PDF Generated Successfully")
            st.download_button("Download PDF", f, "Form49A_filled.pdf")
