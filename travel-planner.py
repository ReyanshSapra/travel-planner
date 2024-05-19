import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, timedelta


def generate_pdf(itinerary_df, trip_title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 10, txt=trip_title, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    
    for index, row in itinerary_df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Date']} - {row['Plan']}", ln=True)
    
    pdf_file = f"{trip_title}.pdf"
    pdf.output(pdf_file)
    return pdf_file


st.title("Travel Itinerary Planner")

trip_title = st.text_input("Enter Trip Title", "My Trip")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if start_date and end_date and start_date <= end_date:
    num_days = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    
    plans = []
    for date in dates:
        plan = st.text_area(f"Plan for {date.strftime('%Y-%m-%d')}", height=100)
        plans.append(plan)
    
    itinerary_df = pd.DataFrame({
        "Date": [date.strftime('%Y-%m-%d') for date in dates],
        "Plan": plans
    })
    
    st.write("Your Itinerary:")
    st.dataframe(itinerary_df)
    
    if st.button("Generate PDF"):
        pdf_file = generate_pdf(itinerary_df, trip_title)
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="Download Itinerary as PDF",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )
else:
    st.warning("Please ensure the end date is after the start date.")
