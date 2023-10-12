# Import necessary modules
import databutton as db
import streamlit as st

# Import custom utility functions
from utils import get_data
from app_brain import handle_openai_query

# This function checks for API keys and completely optional as usage
# and is not necessary when defining an Input box or using secrets
from key_check import key_check

# Suppress deprecation warnings related to Pyplot's global use
st.set_option("deprecation.showPyplotGlobalUse", False)


# Cache the header of the app to prevent re-rendering on each load
@st.cache_resource
def display_app_header():
    """Display the header of the Streamlit app."""
    st.title("1️⃣ One-Prompt Charts 📊 ")
    st.markdown("***Prompt about your data, and see it visualized** ✨ This app runs on the power of your prompting. As here in Databutton HQ, we envision, '**Prompting is the new programming.**'*")


# Display the header of the app
display_app_header()

with st.expander("App Overview", expanded=False):
    st.markdown(
        """

    You will find each functions either in the library or in the main script. Feel free to modu
    - **App Header:** The function `display_app_header` defines the title and a brief description of the app, setting the context for the user. This function is displayed at the top of the app when called on line 24.
       
    - **API Key Check:** The `key_check` function is invoked to ensure the necessary API keys are present before proceeding. This might be for authentication or to access certain services.
    
    - **Data Upload and Display:** The app provides the user with an option to upload data using the `get_data` function (line 47). Once the data is uploaded, it's optionally displayed in an expandable section for the user to review.
    
    - **OpenAI Query Handling:** If the uploaded data is not empty, the `handle_openai_query` function is called (line 64) to process the user's prompt regarding the data and visualize it accordingly. If the uploaded data is empty, a warning is displayed to the user.  
    
    """
    )

# Check for the necessary API keys
key_check()

options = st.radio(
    "Data Usage", options=["Upload file", "Use Data in Storage"], horizontal=True
)
if options == "Upload file":
    # Get data uploaded by the user
    df = get_data()
else:
    df = db.storage.dataframes.get(key="spectra-csv")


# If data is uploaded successfully
if df is not None:
    # Create an expander to optionally display the uploaded data
    with st.expander("Show data"):
        st.write(df)

    # Extract column names for further processing
    column_names = ", ".join(df.columns)

    # Check if the uploaded DataFrame is not empty
    if not df.empty:
        # Handle the OpenAI query and display results
        handle_openai_query(df, column_names)
    else:
        # Display a warning if the uploaded data is empty
        st.warning("The given data is empty.")
