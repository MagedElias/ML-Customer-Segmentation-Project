import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation AI",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN BACKGROUND
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(99, 102, 241, 0.12),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(6, 182, 212, 0.10),
                transparent 25%
            ),
            #080d1c;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 45px;
        padding-bottom: 60px;
    }


    /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #f8fafc !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    .stCaption {
        color: #64748b !important;
    }

    label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    input {
        background-color: #111827 !important;
        color: #f8fafc !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;
        height: 58px;

        border: none;
        border-radius: 14px;

        background: linear-gradient(
            90deg,
            #6366f1,
            #06b6d4
        );

        color: white;

        font-size: 17px;
        font-weight: 700;

        transition: all 0.2s ease;

        box-shadow:
            0 10px 30px rgba(99, 102, 241, 0.20);
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 15px 40px rgba(99, 102, 241, 0.35);
    }


    /* ========================================================
       METRIC
       ======================================================== */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #111827,
            #0f172a
        );

        border: 1px solid #26344d;

        border-radius: 20px;

        padding: 25px;

        text-align: center;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.20);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #818cf8 !important;
        font-size: 30px !important;
        font-weight: 800 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {
        color: #475569;
        text-align: center;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.title("👥 Customer Segmentation AI")

st.write(
    "Discover customer segments using their annual income "
    "and spending behavior."
)

st.divider()


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.header("💼 Customer Profile")

st.caption(
    "Enter the customer's financial and spending information."
)


col1, col2 = st.columns(2)


with col1:

    annual_income = st.number_input(
        "Annual Income (k$)",
        min_value=0.0,
        max_value=500.0,
        value=50.0,
        step=1.0
    )


with col2:

    spending_score = st.number_input(
        "Spending Score (1-100)",
        min_value=1.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PREDICTION
# ============================================================

if st.button("🔍 Identify Customer Segment"):

    # --------------------------------------------------------
    # Prepare customer data
    # --------------------------------------------------------

    data = {
        "annual_income": annual_income,
        "spending_score": spending_score
    }


    try:

        # ----------------------------------------------------
        # Send request to FastAPI
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Analyzing customer profile..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=data,
                timeout=10
            )


        # ----------------------------------------------------
        # Successful prediction
        # ----------------------------------------------------

        if response.status_code == 200:

            result = response.json()

            segment = result["customer_segment"]

            description = result["description"]


            # ------------------------------------------------
            # Result
            # ------------------------------------------------

            st.divider()

            st.header("🎯 Customer Segment")

            result_col1, result_col2, result_col3 = st.columns(
                [1, 2, 1]
            )

            with result_col2:

                st.metric(
                    label="Identified Segment",
                    value=segment
                )


            st.info(
                f"💡 {description}"
            )


            # ------------------------------------------------
            # Customer profile summary
            # ------------------------------------------------

            st.subheader("📊 Customer Profile")

            profile_col1, profile_col2 = st.columns(2)

            with profile_col1:

                st.metric(
                    "Annual Income",
                    f"${annual_income:.0f}k"
                )

            with profile_col2:

                st.metric(
                    "Spending Score",
                    f"{spending_score:.0f}/100"
                )


        # ----------------------------------------------------
        # API error
        # ----------------------------------------------------

        else:

            st.error(
                f"❌ API Error: {response.status_code}"
            )


    # --------------------------------------------------------
    # Connection error
    # --------------------------------------------------------

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI.\n\n"
            "Make sure the FastAPI server is running "
            "on http://127.0.0.1:8000."
        )


    # --------------------------------------------------------
    # Timeout
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The prediction request timed out."
        )


    # --------------------------------------------------------
    # Other errors
    # --------------------------------------------------------

    except Exception as e:

        st.error(
            f"❌ Something went wrong: {e}"
        )


# ============================================================
# INFORMATION
# ============================================================

st.divider()

st.header("💡 How It Works")

st.write(
    "The application uses a trained K-Means clustering model "
    "to identify customer groups based on annual income "
    "and spending score."
)

info1, info2, info3 = st.columns(3)

with info1:

    st.info(
        "**High Income + High Spending**\n\n"
        "Potential premium customers."
    )

with info2:

    st.info(
        "**Low Income + High Spending**\n\n"
        "Customers with strong spending behavior."
    )

with info3:

    st.info(
        "**High Income + Low Spending**\n\n"
        "Potential customers for targeted offers."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer-text">'
    'Customer Segmentation AI • K-Means • FastAPI • Streamlit'
    '</div>',
    unsafe_allow_html=True
)