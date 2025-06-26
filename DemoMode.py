# Streamlit SKU Matcher with GPT and Tokens (Demo Mode)

import streamlit as st
import openai
import os

# --- MODE TOGGLE ---
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# --- SESSION STATE ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "sku" not in st.session_state:
    st.session_state.sku = ""

# --- BASIC PASSWORD PROTECTION ---
def login():
    password = st.text_input("Enter Password", type="password")
    if password != os.getenv("APP_PASSWORD"):
        st.warning("Incorrect password.")
        st.stop()

login()

# --- API KEY SETUP ---
if not DEMO_MODE:
    openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("AI-Powered SKU Matcher (Demo Mode Enabled)" if DEMO_MODE else "AI-Powered SKU Matcher")

# --- INPUT ---
sku = st.text_input("Enter Competitor SKU:", value=st.session_state.sku)
submit = st.button("Find Equivalent")

# --- GPT PROMPT FUNCTIONS ---
def get_competitor_product_info(sku):
    if DEMO_MODE:
        return f"""
        - Brand: Whirlpool  
        - Product type: Dishwasher  
        - Dimensions: 24\"W x 34\"H  
        - Key features: Stainless steel tub, Quiet operation  
        - Full list price: $699  
        - SKU: WDT730HAMZ  
        - Link: https://example.com/competitor-product  
        - Image: https://example.com/images/competitor.jpg
        """
    # GPT logic here...


def get_ge_match(product_summary):
    if DEMO_MODE:
        return f"GE Model: GDT630PYRFS  \nWhy it's the best match: Closest feature alignment and GE family match (GE, GE Profile, Cafe, Monogram, Haier, Hotpoint)  \nSKU: GDT630PYRFS  \nLink: https://www.geappliances.com/appliance/GDT630PYRFS  \nImage: https://example.com/images/ge.jpg"
    # GPT logic here...


def generate_comparison_table(competitor_info, ge_match, features):
    if DEMO_MODE:
        feature_rows = "\n".join([
            f"| {feature}         | ✅ Yes                | ✅ Yes              |" for feature in features
        ])
        return f"""
        | Feature             | Competitor Product     | GE Product           |
        |---------------------|------------------------|----------------------|
        | Brand               | Whirlpool              | GE                   |
        | SKU                 | WDT730HAMZ             | GDT630PYRFS          |
        | Price               | $699                   | $699                 |
        | Size                | 24\" x 34\"            | 24\" x 34\"          |
        | Configuration       | Front control          | Front control        |
        {feature_rows}
        | Product Link        | [Link](https://example.com/competitor-product) | [Link](https://www.geappliances.com/appliance/GDT630PYRFS) |
        | What Doesn't Match  | None (very close match) | None (very close match) |
        """
    # GPT logic here...

# --- MAIN LOGIC ---
specific_features = []

if submit and sku:
    st.session_state.sku = sku
    st.session_state.submitted = True

if st.session_state.submitted:
    with st.spinner("Retrieving competitor product info..."):
        competitor_info = get_competitor_product_info(st.session_state.sku)
        st.subheader("Competitor Product Info")
        st.markdown(competitor_info)

    with st.spinner("Finding best GE match..."):
        ge_match = get_ge_match(competitor_info)
        st.subheader("Recommended Equivalent")
        st.markdown(ge_match)

    # --- Extract demo image links ---
    if DEMO_MODE:
        st.image([
            "https://example.com/images/competitor.jpg",
            "https://example.com/images/ge.jpg"
        ], width=300, caption=["Competitor Product", "GE Product"])

    feature_options = [
        "ADA compliance", "Stainless steel tub", "WiFi connectivity",
        "Energy Star rated", "Top control panel", "Child lock",
        "Third rack", "SmartDry", "Quiet operation", "Steam clean"
    ]
    specific_features = st.multiselect("Select features to compare:", feature_options)

    if specific_features:
        with st.spinner("Generating comparison table..."):
            feature_check = generate_comparison_table(competitor_info, ge_match, specific_features)
            st.subheader("Feature Comparison Table")
            st.markdown(feature_check, unsafe_allow_html=True)
