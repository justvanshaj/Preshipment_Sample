import streamlit as st
from fpdf import FPDF
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
import os

st.set_page_config(page_title="PSS Maker", page_icon="favicon.png")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

pre_filled_data = {
    "001": {
        "full_name": "Mahendra Tripathi",
        "designation": "Country General Manager & Director",
        "company_name": "Lamberti India Pvt. Ltd.",
        "city_state": "Rajkot, Gujarat",
        "po_id": "LIPL2024250427",
        "custom_message": "Sending you Pre-Shipment sample of Guar Gum Powder Modified.",
        "code_type": "MOD"
    },
    "002": {
        "full_name": "Mahendra Tripathi",
        "designation": "Country General Manager & Director",
        "company_name": "Lamberti India Pvt. Ltd.",
        "city_state": "Rajkot, Gujarat",
        "po_id": "LIPL2024250427",
        "custom_message": "Sending you Pre-Shipment sample of FARINA GUAR 200 MESH 5000 T/C.",
        "code_type": "FAR"
    },
}

def create_pdf(date, sal1, full_name, desig, company, city, sal2, po_id, message, items, margin, letterhead_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_left_margin(margin)

    if os.path.exists(letterhead_path):
        pdf.image(letterhead_path, x=0, y=0, w=210)

    pdf.set_font("Arial", size=10)
    pdf.ln(50)

    pdf.cell(0, 10, txt="Kindly Att.", ln=False, align='L')
    pdf.cell(0, 10, txt=f"Date: {date}", ln=True, align='R')
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 5, txt=f"{sal1} {full_name},", ln=True)
    pdf.cell(200, 5, txt=f"({desig})", ln=True)
    pdf.cell(200, 5, txt=company + ",", ln=True)
    pdf.cell(200, 5, txt=city, ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Dear {sal2},", ln=True)
    pdf.ln(2)
    pdf.cell(200, 10, txt=message, ln=True)
    pdf.ln(2)
    pdf.cell(200, 10, txt=f"P.O. ID: {po_id}", ln=True)
    pdf.ln(2)

    for label, (code, weight) in items.items():
        pdf.cell(200, 5, txt=f"{label}) {code} - {weight} MT", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Kindly acknowledge receipt of the same.", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt="Yours Faithfully,", ln=True)
    pdf.ln(15)
    pdf.cell(200, 10, txt="Authorised Signatory", ln=True)
    pdf.cell(200, 10, txt="Aravally Processed Agrotech Pvt Ltd", ln=True)

    output_path = "generated_letter.pdf"
    pdf.output(output_path)
    return output_path

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
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value=data["custom_message"])
        code_type = data["code_type"]
    else:
        full_name = st.text_input("Full Name")
        designation = st.text_input("Designation")
        company_name = st.text_input("Company Name")
        city_state = st.text_input("City, State")
        po_id = st.text_input("P.O. ID")
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value="Sending you Pre-Shipment sample of")
        code_type = "XXX"

    salutation2 = st.selectbox("Salutation2", ["Sir", "Ma’am"])
    total_containers = st.number_input("Total Containers", min_value=1, value=1)
    current_container = st.number_input("Current Container Number", min_value=1, value=1)
    num_items = st.selectbox("Number of items", [1, 2, 3, 4, 5, 6])

    item_details = {}
    for i in range(num_items):
        label = chr(65 + i)
        code = st.text_input(f"Item {label} Code")
        weight = st.number_input(f"Item {label} Weight (MT)", min_value=0.0, step=0.1, value=4.5)
        item_details[label] = (code, weight)

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    date_str = date.strftime("%d/%m/%Y")
    po_tail = po_id[-3:] if len(po_id) >= 3 else "000"
    file_name = f"PSS LIPL {code_type} {po_tail} {int(current_container)} of {int(total_containers)}.pdf"
    margin = 25.0
    pdf_path = create_pdf(date_str, salutation1, full_name, designation, company_name, city_state, salutation2, po_id, custom_line, item_details, margin, "letterhead.png")

    st.success("PDF generated successfully!")

    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name=file_name)

    # Preview PDF
    st.markdown("### PDF Preview")
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1, fmt='png')
        st.image(images[0], caption="Preview of First Page", use_column_width=True)
    except Exception as e:
        st.warning(f"Could not render PDF preview: {e}")
