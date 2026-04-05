import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Gurgaon Real Estate Pro",
    page_icon="🏠",
    layout="wide",
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .hero-text {
        text-align: center;
        padding: 40px;
        background: linear-gradient(to right, #4b6cb7, #182848);
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        border-top: 5px solid #ff4b4b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 280px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
    <div class="hero-text">
        <h1>🏙️ Gurgaon Real Estate Intelligence Portal</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>
            Advanced Data Science tools for Price Prediction, Market Analysis, and Property Recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN NAVIGATION CARDS ---
st.write("### 🛠️ Choose a Tool to Get Started")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>📈 Price Predictor</h3>
            <p>Enter property details (Area, BHK, Sector) to get a high-accuracy market value estimate using our trained pipeline.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Predictor →", key="btn_pred"):
        st.info("Select 'Price Predictor' from the sidebar.")

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📊 Market Analytics</h3>
            <p>Explore price trends across sectors with interactive Geo-Maps, Area vs Price plots, and BHK distribution analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Analytics →", key="btn_anal"):
        st.info("Select 'Real Estate Analytics' from the sidebar.")

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>🏢 Recommender</h3>
            <p>Find similar apartments based on luxury features or search for all properties within a specific radius of a landmark.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Recommender →", key="btn_rec"):
        st.info("Select 'Recommend Apartments' from the sidebar.")

with col4:
    st.markdown("""
        <div class="feature-card">
            <h3>💡 Price Insights</h3>
            <p>Dive deep into feature importance. Understand exactly how much 1 extra BHK or a specific sector adds to property value.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Insights →", key="btn_ins"):
        st.info("Select 'Price Insights' from the sidebar.")

st.divider()

# --- PROJECT OVERVIEW ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("About the Project")
    st.write(f"""
    This app is a comprehensive end-to-end data science project focused on the **Gurgaon Real Estate Market**. 
    By leveraging machine learning and data visualization, we aim to provide transparency for buyers and investors.
    
    **Key Features:**
    - **Massive Dataset:** Analyzed **3,500+ flats and houses** across **250+ societies** in Gurgaon.
    - **Data-Driven:** Trained on thousands of property listings scraped from top real estate portals.
    - **Spatial Awareness:** Incorporates location-based distance metrics for better accuracy.
    - **Interactive Insights:** Gain granular understanding of price drivers and location premiums.
    """)

with c2:
    st.subheader("Quick Stats")
    st.success("✅ Model Accuracy: ~88%")
    st.info("📍 250+ Societies & 100+ Sectors")
    st.metric("Total Properties", "3,500+", delta="Live Data")
    st.warning("🔄 Data Updated: 2026")

# --- SIDEBAR ---
st.sidebar.success("Select a tool above to begin.")
st.sidebar.markdown("---")
st.sidebar.caption("Created as part of the DSMP Capstone Project.")