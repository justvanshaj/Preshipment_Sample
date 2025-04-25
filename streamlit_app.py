import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Set the page configuration
st.set_page_config(
    page_title="PSS Maker",
    page_icon="favicon.png"
)

# Hide Streamlit's default UI components
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Pre-filled data dictionary
pre_filled_data = {
    "001": {
        "full_name": "Mahendra Tripathi",
        "designation": "Country General Manager & Director",
        "company_name": "Lamberti India Pvt. Ltd.",
        "city_state": "Rajkot, Gujarat",
        "po_id": "LIPL2024250169",
        "custom_message": "Sending you Pre-Shipment sample of Guar Gum Powder Modified."
    },
    "002": {
        "full_name": "Mahendra Tripathi",
        "designation": "Country General Manager & Director",
        "company_name": "Lamberti India Pvt. Ltd.",
        "city_state": "Rajkot, Gujarat",
        "po_id": "LIPL2024250427",
        "custom_message": "Sending you Pre-Shipment sample of FARINA GUAR 200 MESH 5000 T/C."
    }
}

# PDF generator function
def create_pdf(filename, date, salutation1, full_name, designation, company_name, city_state, salutation2, po_id, custom_line, item_details, left_margin):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.set_left_margin(left_margin)
    pdf.ln(50)

    pdf.cell(0, 10, txt="Kindly Att.", ln=False, align='L')
    pdf.cell(0, 10, txt=f"Date: {date}", ln=True, align='R')
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 5, txt=f"{salutation1} {full_name},", ln=True)
    pdf.cell(200, 5, txt=f"({designation})", ln=True)
    pdf.cell(200, 5, txt=company_name + ",", ln=True)
    pdf.cell(200, 5, txt=city_state, ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Dear {salutation2},", ln=True)
    pdf.ln(2)
    pdf.cell(200, 10, txt=custom_line, ln=True)
    pdf.ln(2)
    pdf.cell(200, 10, txt=f"P.O. ID: {po_id}", ln=True)
    pdf.ln(2)

    for item_label, (code, weight) in item_details.items():
        pdf.cell(200, 5, txt=f"{item_label}) {code} - {weight:.2f} MT", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Kindly acknowledge receipt of the same.", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt="Yours Faithfully,", ln=True)
    pdf.ln(15)
    pdf.cell(200, 10, txt="Authorised Signatory", ln=True)
    pdf.cell(200, 10, txt="Aravally Processed Agrotech Pvt Ltd", ln=True)

    pdf.output(filename)

# UI
st.title("PSS PDF MAKER")

with st.form("pdf_form"):
    date = st.date_input("Date", value=datetime.today())
    salutation1 = st.selectbox("Salutation1", ["Mr.", "Mrs."])
    user_code = st.text_input("Enter Code to auto-fill details")

    if user_code in pre_filled_data:
        data = pre_filled_data[user_code]
        full_name = st.text_input("Full Name", value=data["full_name"])
        designation = st.text_input("Designation", value=data["designation"])
        company_name = st.text_input("Company Name", value=data["company_name"])
        city_state = st.text_input("City, State", value=data["city_state"])
        po_id = st.text_input("P.O. ID", value=data["po_id"])
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value=data.get("custom_message", "Sending you Pre-Shipment sample of"))
    else:
        full_name = st.text_input("Full Name")
        designation = st.text_input("Designation")
        company_name = st.text_input("Company Name")
        city_state = st.text_input("City, State")
        po_id = st.text_input("P.O. ID")
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value="Sending you Pre-Shipment sample of")

    salutation2 = st.selectbox("Salutation2", ["Sir", "Ma’am"])
    total_containers = st.number_input("Total Number of Containers", min_value=1, step=1)
    current_container = st.number_input("Current Container Number", min_value=1, step=1)

    num_items = st.selectbox("Number of items", [1, 2, 3, 4, 5, 6])

    item_details = {}
    item_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    for i in range(num_items):
        code = st.text_input(f"Item {item_labels[i]} Code")
        weight = st.number_input(f"Item {item_labels[i]} Weight (MT)", min_value=0.0, step=0.1, value=4.50)
        item_details[item_labels[i]] = (code, weight)

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    date_str = date.strftime("%d/%m/%Y")
    left_margin = 25.0

    # PDF Naming Logic
    suffix = "MOD" if user_code == "001" else "FAR" if user_code == "002" else "GEN"
    po_suffix = po_id[-3:] if len(po_id) >= 3 else "000"
    filename = f"PSS LIPL {suffix} {po_suffix} {int(current_container)} of {int(total_containers)}.pdf"

    create_pdf(filename, date_str, salutation1, full_name, designation, company_name, city_state, salutation2, po_id, custom_line, item_details, left_margin)

    with open(filename, "rb") as f:
        st.download_button("Download PDF", f, file_name=filename)
