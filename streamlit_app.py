import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Page config
st.set_page_config(page_title="PSS Maker", page_icon="favicon.png")

# Hide default UI
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Pre-filled data
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
        "po_id": "LIPL2024250169",
        "custom_message": "Sending you Pre-Shipment sample of FARINA GUAR 200 MESH 5000 T/C."
    }
}

# PDF creation function
def create_pdf(date, salutation1, full_name, designation, company_name, city_state,
               salutation2, po_id, custom_line, item_details, left_margin,
               code, container_number, total_containers):
    pdf = FPDF()
    pdf.add_page()

    try:
        pdf.image("letterhead.png", x=0, y=0, w=210)  # full A4 width
    except RuntimeError:
        pass

    pdf.set_font("Arial", size=10)
    pdf.set_left_margin(left_margin)
    pdf.ln(60)

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

    for label, (code_text, weight) in item_details.items():
        pdf.cell(200, 5, txt=f"{label}) {code_text} - {weight} MT", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Kindly acknowledge receipt of the same.", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt="Yours Faithfully,", ln=True)
    pdf.ln(15)
    pdf.cell(200, 10, txt="Authorised Signatory", ln=True)
    pdf.cell(200, 10, txt="Aravally Processed Agrotech Pvt Ltd", ln=True)

    po_suffix = po_id[-3:]
    material = "MOD" if code == "001" else "FAR" if code == "002" else "UNK"
    file_name = f"PSS LIPL {material} {po_suffix} {container_number} of {total_containers}.pdf"

    pdf.output(file_name)
    return file_name

# App interface
st.title("PSS PDF MAKER")

with st.form("pdf_form"):
    date = st.date_input("Date", value=datetime.today())
    salutation1 = st.selectbox("Salutation1", ["Mr.", "Mrs."])
    user_code = st.text_input("Enter Code to auto-fill details")

    if user_code in pre_filled_data:
        full_name = st.text_input("Full Name", value=pre_filled_data[user_code]["full_name"])
        designation = st.text_input("Designation", value=pre_filled_data[user_code]["designation"])
        company_name = st.text_input("Company Name", value=pre_filled_data[user_code]["company_name"])
        city_state = st.text_input("City, State", value=pre_filled_data[user_code]["city_state"])
        po_id = st.text_input("P.O. ID", value=pre_filled_data[user_code]["po_id"])
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value=pre_filled_data[user_code]["custom_message"])
    else:
        full_name = st.text_input("Full Name")
        designation = st.text_input("Designation")
        company_name = st.text_input("Company Name")
        city_state = st.text_input("City, State")
        po_id = st.text_input("P.O. ID")
        custom_line = st.text_input("Pre-Shipment Sample Properties:", value="Sending you Pre-Shipment sample of")

    salutation2 = st.selectbox("Salutation2", ["Sir", "Ma’am"])
    num_items = st.selectbox("Number of items to include", [1, 2, 3, 4, 5, 6])

    item_details = {}
    for i in range(1, num_items + 1):
        label = chr(64 + i)  # A, B, C...
        code_input = st.text_input(f"Item {label} Code")
        weight_input = st.number_input(f"Item {label} Weight (MT)", min_value=0.0, step=0.1, value=4.5)
        item_details[label] = (code_input, weight_input)

    container_number = st.text_input("Current Container Number")
    total_containers = st.text_input("Total Containers")

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    date_str = date.strftime("%d/%m/%Y")
    left_margin = 25.0
    pdf_path = create_pdf(
        date_str, salutation1, full_name, designation, company_name,
        city_state, salutation2, po_id, custom_line, item_details, left_margin,
        user_code, container_number, total_containers
    )

    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name=pdf_path)
