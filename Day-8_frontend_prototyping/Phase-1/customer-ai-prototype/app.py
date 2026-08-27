import requests
import streamlit as st


# ==========================================
# Configuration
# ==========================================

API_BASE_URL = "http://127.0.0.1:8000"


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Customer AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# Header
# ==========================================

st.title("🤖 Customer AI Assistant")

st.write(
    "Retrieve customer information and generate "
    "a simple operational summary."
)


# ==========================================
# User Input
# ==========================================

customer_id = st.number_input(
    "Customer ID",
    min_value=1,
    value=101,
    step=1
)

question = st.text_input(
    "Ask a question",
    placeholder="What is the current status of this customer?"
)


# ==========================================
# API + AI Interaction
# ==========================================

if st.button("Ask AI"):

    # -----------------------------
    # Input validation
    # -----------------------------

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    # -----------------------------
    # Call Mock Customer API
    # -----------------------------

    try:

        with st.spinner("Retrieving customer information..."):

            response = requests.get(
                f"{API_BASE_URL}/customers/{customer_id}",
                timeout=5
            )

        # -----------------------------
        # Customer not found
        # -----------------------------

        if response.status_code == 404:

            st.error(
                f"Customer {customer_id} was not found."
            )

            st.stop()

        # -----------------------------
        # Other HTTP errors
        # -----------------------------

        response.raise_for_status()

        # -----------------------------
        # Parse JSON
        # -----------------------------

        customer = response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to the Customer API."
        )

        st.info(
            "Make sure the FastAPI mock server is running "
            "on port 8000."
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error(
            "The Customer API request timed out."
        )

        st.stop()

    except requests.exceptions.RequestException as error:

        st.error(
            f"Customer API request failed: {error}"
        )

        st.stop()

    # ==========================================
    # Customer Information
    # ==========================================

    st.subheader("Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Customer ID",
            customer["customer_id"]
        )

    with col2:

        st.metric(
            "Status",
            customer["status"].upper()
        )

    st.write(
        f"**Name:** {customer['name']}"
    )

    st.write(
        f"**Segment:** {customer['segment']}"
    )

    st.write(
        f"**Region:** {customer['region']}"
    )

    # ==========================================
    # AI Response
    # ==========================================

    st.subheader("AI Response")

    if customer["status"].lower() == "active":

        answer = (
            f"{customer['name']} is currently active. "
            f"The customer belongs to the "
            f"{customer['segment']} segment and is located "
            f"in the {customer['region']} region."
        )

    else:

        answer = (
            f"{customer['name']} is currently inactive. "
            "Further investigation may be required."
        )

    st.info(answer)