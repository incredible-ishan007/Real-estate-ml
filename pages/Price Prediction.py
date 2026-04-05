import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gurgaon Real Estate Predictor", page_icon="🏠", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_resource
def load_data():
    with open('datasets/df.pkl','rb') as file:
        df = pickle.load(file)
    with open('datasets/pipeline.pkl','rb') as file:
        pipeline = pickle.load(file)
    return df, pipeline

df, pipeline = load_data()

st.title('🏠 Gurgaon Real Estate Price Predictor')
st.write("Fill in the details below to estimate the property value.")

# --- INPUT SECTION ---
with st.container():
    st.subheader('Property Specifications')
    
    # Organized into 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        property_type = st.selectbox('Property Type', ['flat', 'house'])
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

    with col2:
        bedrooms = float(st.selectbox('Number of Bedroom', sorted(df['bedRoom'].unique().tolist())))
        bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
        balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
        built_up_area = float(st.number_input('Built Up Area (Sq.Ft)', min_value=100.0, step=100.0))

    with col3:
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# --- PREDICTION LOGIC ---
st.markdown("---")
if st.button('Estimate Price'):
    
    # Form data
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # --- DISPLAY RESULTS ---
    st.balloons()
    
    st.markdown(f"""
        <div class="result-card">
            <h2 style='color: #31333F;'>Estimated Price Range</h2>
            <h1 style='color: #ff4b4b;'>₹ {round(low,2)} Cr - ₹ {round(high,2)} Cr</h1>
            <p style='color: #555;'>*Price estimates are based on current market data and model accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Adding Metric visualization
    m1, m2 = st.columns(2)
    m1.metric("Average Price", f"₹ {round(base_price, 2)} Cr")
    m2.metric("Area", f"{built_up_area} Sq.Ft")