import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import tempfile
import os

# ---------- CONFIG ----------
PDF_TEMPLATE = "Form49A.pdf"  # must exist in repo root

st.set_page_config(page_title="PAN Form Filler", layout="centered")

st.title("📄 PAN Form Auto Filler")

# ---------- INPUT FORM ----------
with st.form("name_form"):
    st.subheader("Enter Name Details")

    surname = st.text_input("Surname (Last Name)")
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")

    submitted = st.form_submit_button("Generate PDF")

# ---------- PROCESS ----------
if submitted:

    if not os.path.exists(PDF_TEMPLATE):
        st.error("PDF template not found in repo")
    elif not surname or not first_name:
        st.error("Surname and First Name are required")
    else:
        # Create temp files
        overlay_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        overlay_path = overlay_file.name
        output_path = output_file.name

        # ---------- CREATE OVERLAY ----------
        c = canvas.Canvas(overlay_path, pagesize=A4)
        c.setFont("Helvetica", 10)

        # ⚠️ Adjust coordinates based on your PDF layout
        c.drawString(150, 690, surname)       # Last Name
        c.drawString(300, 690, first_name)    # First Name
        c.drawString(450, 690, middle_name)   # Middle Name

        c.save()

        # ---------- MERGE ----------
        reader = PdfReader(PDF_TEMPLATE)
        overlay_reader = PdfReader(overlay_path)
        writer = PdfWriter()

        for i in range(len(reader.pages)):
            base_page = reader.pages[i]

            if i < len(overlay_reader.pages):
                base_page.merge_page(overlay_reader.pages[i])

            writer.add_page(base_page)

        with open(output_path, "wb") as f:
            writer.write(f)

        # ---------- DOWNLOAD ----------
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Filled PDF",
                data=f,
                file_name="filled_form.pdf",
                mime="application/pdf"
            )

        st.success("PDF generated successfully!")
