import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os

# -------- CONFIG --------
PDF_TEMPLATE = "Form49A.pdf"  # must exist in repo root

st.set_page_config(page_title="PDF Editor", layout="centered")
st.title("PDF Name Editor")

# -------- FORM --------
with st.form("name_form"):
    surname = st.text_input("Surname")
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")

    submitted = st.form_submit_button("Generate PDF")

# -------- PROCESS --------
if submitted:

    if not os.path.exists(PDF_TEMPLATE):
        st.error("PDF file not found in repository")
    elif not surname or not first_name:
        st.error("Surname and First Name are required")
    else:
        # Temporary files
        overlay_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name

        # -------- CREATE OVERLAY --------
        c = canvas.Canvas(overlay_path, pagesize=A4)
        c.setFont("Helvetica", 10)

        # ⚠️ Adjust these coordinates for your PDF
        c.drawString(150, 690, surname)
        c.drawString(300, 690, first_name)
        c.drawString(450, 690, middle_name)

        c.save()

        # -------- MERGE WITH ORIGINAL PDF --------
        reader = PdfReader(PDF_TEMPLATE)
        overlay = PdfReader(overlay_path)
        writer = PdfWriter()

        for i in range(len(reader.pages)):
            page = reader.pages[i]

            if i < len(overlay.pages):
                page.merge_page(overlay.pages[i])

            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        # -------- DOWNLOAD --------
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Edited PDF",
                data=f,
                file_name="edited_form.pdf",
                mime="application/pdf"
            )

        st.success("PDF generated successfully!")
