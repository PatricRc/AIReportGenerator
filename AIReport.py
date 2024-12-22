import streamlit as st
import pandas as pd
import openai
import io
from fpdf import FPDF

def main():
    st.title("AI-Powered Data Analytics Template Generator")

    # Input for OpenAI API Key
    st.markdown("### Enter your OpenAI API Key")
    openai_api_key = st.text_input("API Key", type="password")

    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")
        return

    # Set the OpenAI API key dynamically
    openai.api_key = openai_api_key

    # Upload File Section
    st.markdown("### Upload Your Dataset")
    uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file:
        df = load_data(uploaded_file)

        st.markdown("#### Data Preview")
        st.write(df.head())

        st.markdown("### Dataset Information")
        st.write(f"Number of rows: {df.shape[0]}")
        st.write(f"Number of columns: {df.shape[1]}")

        if st.button("Generate Report with AI"):
            template = generate_template(df, openai_api_key)
            st.markdown(template, unsafe_allow_html=True)

            # Provide download button for the PDF report
            st.markdown("### Download Report")
            pdf_report = generate_pdf(template)
            st.download_button(
                label="Download PDF Report",
                data=pdf_report,
                file_name="report.pdf",
                mime="application/pdf"
            )

def load_data(uploaded_file):
    """Load CSV or XLSX data into a pandas DataFrame."""
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

def generate_template(df, api_key):
    """Generate the project template based on the uploaded data."""
    openai.api_key = api_key

    prompt = f"""
    I have a dataset with the following columns:
    {', '.join(df.columns)}.

    Here are the first few rows of the dataset:
    {df.head(500).to_string(index=False)}

    Please generate a detailed and well-formatted data analytics project report with the following structure:

    # Project Background
    Provide a detailed background about the company, its industry, business model, and any key metrics related to the project. Include specifics that are relevant to the dataset provided.

    # Insights and Recommendations
    Provide insights derived from the dataset in the following categories:
    - **Category 1:** Explain the trends or findings for this category.
    - **Category 2:** Highlight demographic-related insights or trends.
    - **Category 3:** Focus on operational or process-related insights.
    - **Category 4:** Summarize recovery patterns or efficiency insights.

    Include actionable recommendations for each category that stakeholders can consider.

    # Data Structure and Initial Analysis
    Describe the structure of the data, including a summary of the number of records, data types, and any preprocessing steps performed.

    # Executive Summary
    Provide a concise summary of the project findings, key takeaways, and how they address the company’s goals or challenges. Include up to 3 key insights that would be most impactful to stakeholders.

    Return the report in a well-formatted markdown format, making it easy to read and include headings, subheadings, and bullet points.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data analytics assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating template: {e}"

def generate_pdf(template):
    """Generate a PDF from the markdown template."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in template.splitlines():
        # Encode to latin-1 or replace unsupported characters
        sanitized_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, sanitized_line)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output, dest='S')
    pdf_output.seek(0)
    return pdf_output.read()

if __name__ == "__main__":
    main()

