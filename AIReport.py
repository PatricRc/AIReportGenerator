import streamlit as st
import pandas as pd
import openai
import io

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

            # Provide download button for the HTML report
            st.markdown("### Download Report")
            html_report = f"<html><body>{template}</body></html>"
            st.download_button(
                label="Download HTML Report",
                data=html_report,
                file_name="report.html",
                mime="text/html"
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

    Please generate a detailed data analytics project template with the following structure:

    # Project Background
    Background about the company, including the industry, active years, business model, and key business metrics. Explain this from the POV of a data analyst who is working at the company.

    Insights and recommendations are provided on the following key areas:
    - **Category 1:** 
    - **Category 2:** 
    - **Category 3:** 
    - **Category 4:** 

    The Python pandas queries used to inspect and clean the data for this analysis can be found here [link].

    Targeted Python pandas queries regarding various business questions can be found here [link].

    An interactive Power BI dashboard used to report and explore sales trends can be found here [link].

    # Data Structure & Initial Checks
    The company’s main database structure as seen below consists of four tables: Table1, Table2, Table3, Table4, with a total row count of X records. A description of each table is as follows:
    - **Table 1:**
    - **Table 2:**
    - **Table 3:**
    - **Table 4:**
    [Entity Relationship Diagram here]

    # Executive Summary
    ## Overview of Findings
    Explain the overarching findings, trends, and themes in 2-3 sentences here. This section should address the question: "If a stakeholder were to take away 3 main insights from your project, what are the most important things they should know?" You can put yourself in the shoes of a specific stakeholder - for example, a marketing manager or finance director - to think creatively about this section.

    [Visualization, including a graph of overall trends or snapshot of a dashboard]

    # Insights Deep Dive
    ### Category 1:
    * **Main insight 1.** Detail about trends and observations.
    * **Main insight 2.** Detail about trends and observations.
    [Visualization specific to category 1]

    ### Category 2:
    * **Main insight 1.** Detail about trends and observations.
    * **Main insight 2.** Detail about trends and observations.
    [Visualization specific to category 2]

    ### Category 3:
    * **Main insight 1.** Detail about trends and observations.
    * **Main insight 2.** Detail about trends and observations.
    [Visualization specific to category 3]

    ### Category 4:
    * **Main insight 1.** Detail about trends and observations.
    * **Main insight 2.** Detail about trends and observations.
    [Visualization specific to category 4]

    # Recommendations
    Based on the insights and findings above, we would recommend the [stakeholder team] to consider the following: 
    * Observation and related recommendation.
    * Observation and related recommendation.

    # Assumptions and Caveats
    * Assumption 1.
    * Assumption 2.

    Return this template as markdown.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating template: {e}"

if __name__ == "__main__":
    main()


