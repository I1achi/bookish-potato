import streamlit as st

# Page config
st.set_page_config(page_title="Simple Form", layout="centered")

st.title("Simple Name Input Form")

# Form
with st.form("name_form"):
    surname = st.text_input("Surname")
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")

    submitted = st.form_submit_button("Submit")

# Output
if submitted:
    st.write("### Entered Data:")
    st.write(f"Surname: {surname}")
    st.write(f"First Name: {first_name}")
    st.write(f"Middle Name: {middle_name}")
