import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Function to create PDF with the updated document format
def create_pdf(date, salutation1, full_name, designation, company_name, city_state, salutation2, po_id, custom_line, item_details):
    pdf = FPDF()
    pdf.add_page()

    # Setting font
    pdf.set_font("Arial", size=10)

    # Adding top gap
    pdf.ln(50)  # Adjust the value as needed to match your desired gap

    # Adding "Kindly Att." on the left and Date on the right on the same line
    pdf.cell(0, 10, txt="Kindly Att.", ln=False, align='L')
    pdf.cell(0, 10, txt=f"Date: {date}", ln=True, align='R')
    
    # Adding the rest of the content
    pdf.ln(10)  # Line break after the first line
    
    # Bold Full Name and City State
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
    
    # List items with alphanumeric codes and weights
    for item_label, (code, weight) in item_details.items():
        pdf.cell(200, 5, txt=f"{item_label}) {code} - {weight} MT", ln=True)
    pdf.ln(5)
    
    pdf.cell(200, 10, txt="Kindly acknowledge receipt of the same.", ln=True)
    pdf.ln(2)
    
    # Bold Authorized Signatory and Company Name
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(200, 10, txt="Yours Faithfully,", ln=True)
    pdf.ln(15)
    pdf.cell(200, 10, txt="Authorised Signatory", ln=True)
    pdf.cell(200, 10, txt="Aravally Processed Agrotech Pvt Ltd", ln=True)
    
    # Saving the PDF
    pdf_output = "generated_letter.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Streamlit App
st.title("Generate a Custom PDF Letter")

# Form to collect data
with st.form("pdf_form"):
    date = st.date_input("Date", value=datetime.today())
    salutation1 = st.selectbox("Salutation1", ["Sir", "Ma’am", "Mr.", "Mrs."])  # Added Mr./Mrs. options
    full_name = st.text_input("Full Name")
    designation = st.text_input("Designation")
    company_name = st.text_input("Company Name")
    city_state = st.text_input("City, State")
    salutation2 = st.selectbox("Salutation2", ["Sir", "Ma’am"])
    po_id = st.text_input("P.O. ID")
    
    # Custom line input for "Pre-Shipment sample..." with default text
    custom_line = st.text_input("Custom line for Pre-Shipment sample", value="Sending you Pre-Shipment sample of")

    # Select number of items to display
    num_items = st.selectbox("Number of items to include", [1, 2, 3, 4, 5, 6])

    # Conditional item inputs
    item_details = {}
    if num_items >= 1:
        item_a_code = st.text_input("Item A Code")
        item_a_weight = st.number_input("Item A Weight (MT)", min_value=0.0, step=0.1)
        item_details["A"] = (item_a_code, item_a_weight)
    if num_items >= 2:
        item_b_code = st.text_input("Item B Code")
        item_b_weight = st.number_input("Item B Weight (MT)", min_value=0.0, step=0.1)
        item_details["B"] = (item_b_code, item_b_weight)
    if num_items >= 3:
        item_c_code = st.text_input("Item C Code")
        item_c_weight = st.number_input("Item C Weight (MT)", min_value=0.0, step=0.1)
        item_details["C"] = (item_c_code, item_c_weight)
    if num_items >= 4:
        item_d_code = st.text_input("Item D Code")
        item_d_weight = st.number_input("Item D Weight (MT)", min_value=0.0, step=0.1)
        item_details["D"] = (item_d_code, item_d_weight)
    if num_items >= 5:
        item_e_code = st.text_input("Item E Code")
        item_e_weight = st.number_input("Item E Weight (MT)", min_value=0.0, step=0.1)
        item_details["E"] = (item_e_code, item_e_weight)
    if num_items == 6:
        item_f_code = st.text_input("Item F Code")
        item_f_weight = st.number_input("Item F Weight (MT)", min_value=0.0, step=0.1)
        item_details["F"] = (item_f_code, item_f_weight)
    
    # Submit button
    submitted = st.form_submit_button("Generate PDF")

if submitted:
    # Convert date to string format
    date_str = date.strftime("%d/%m/%Y")
    
    # Create PDF
    pdf_path = create_pdf(date_str, salutation1, full_name, designation, company_name, city_state, salutation2, po_id, custom_line, item_details)
    
    # Display the link to download the PDF
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="generated_letter.pdf")
