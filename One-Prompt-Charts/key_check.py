import databutton as db
import streamlit as st
import openai
from openai import OpenAI


def is_valid_openai_key(api_key: str) -> bool:
    """
    Validates whether the provided OpenAI API key is valid.

    Parameters:
    - api_key (str): The OpenAI API key to validate.

    Returns:
    - bool: True if the API key is valid, False otherwise.
    """
    try:
        Client = OpenAI(api_key=db.secrets.get("OPENAI_API_KEY"))
        # Attempting to list models; will throw an exception if the key is invalid.
        if Client.models.list():
            return True
    except:
        return False


def key_check():
    """
    Checks the OpenAI API key, either from the Databutton secrets store or from user input.
    If the key is valid, it continues the app flow; otherwise, it stops the app and provides feedback.
    """
    try:
        # Attempting to get the OpenAI API key from the Databutton secrets store.
        openai.api_key = db.secrets.get(name="OPENAI_API_KEY")

        # Check if the connection is established and models are available.
        if not openai.Model.list():
            st.write("Not connected to OpenAI.")
            st.stop()

    except Exception as e:
        # Display information about needing an OpenAI API key.
        mtinfo = st.empty()
        mtinfo.info(
            """
            Hi there! Welcome to the "One-Prompt Charts" app template. 📊
            
            This app allows you to upload your data and get visual insights with just a single prompt. However, to power the magic behind the scenes, I need your OpenAI API key. 
            
            If you don't have a key, you can sign up and create one [here](https://platform.openai.com/account/api-keys).
            
            Don't worry, your key will be securely stored in the Databutton secrets store, which you can find in the left-side menu under "Configure". If you prefer to add it manually, ensure to assign the name as `OPENAI_API_KEY` for your secret.
            
            Once set up, simply upload your data, prompt about it, and see it visualized! ✨

            """,
            icon="🤖",
        )

        # Accept user input for the API key.
        mt = st.empty()
        user_provided_key = mt.text_input(
            "Type your OpenAI API key here to continue:", type="password"
        )

        # Check the format of the provided API key.
        if user_provided_key.startswith("sk-"):
            with st.status("Connecting to OpenAI.", expanded=True) as status:
                # Validate the provided API key.
                if is_valid_openai_key(user_provided_key):
                    status.write("Adding OpenAI API key...")
                    db.secrets.put(name="OPENAI_API_KEY", value=user_provided_key)
                    status.update(
                        label="Added OpenAI API key to Databutton secrets securely. Chatbot is enabled for you.",
                        state="complete",
                    )
                    status.write("Added and cleaning onboarding UI...")
                    # Clean the screen
                    mt.empty()
                    mtinfo.empty()
                else:
                    st.error(
                        "Error: Invalid OpenAI API Key. You can find your API key at [this link](https://platform.openai.com/account/api-keys).",
                    )
                    st.stop()
        else:
            st.warning("Please ensure a correct API key.")
            st.stop()
