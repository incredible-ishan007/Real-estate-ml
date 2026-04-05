import streamlit as st
import numpy as np
import pickle
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Real Estate Insights", layout="wide")
st.title("🏠 Property Feature Impact Analysis")

# --- LOAD ASSETS ---
@st.cache_resource
def load_assets():
    path = "datasets"
    with open(os.path.join(path, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(path, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(path, 'features.pkl'), 'rb') as f:
        feature_names = pickle.load(f)
    return model, scaler, feature_names

try:
    lr, scaler, feature_names = load_assets()
except Exception as e:
    st.error(f"Error: Could not load files from 'datasets' folder. {e}")
    st.stop()

# --- STRICT CATEGORIZATION ---
# 1. These are exactly the columns you mentioned
main_features_list = [
    'property_type',
    'bedRoom',
    'bathroom',
    'built_up_area',
    'servant room',
    'furnishing_type',
    'luxury_category',
    'agePossession_old',
    'agePossession_under construction',
    'agePossession_new'
]

# Ensure we only show ones that exist in your model
available_main = [f for f in main_features_list if f in feature_names]

# 2. Everything else goes to Sectors
sector_features = [f for f in feature_names if f not in available_main and f != 'const']

# --- UI INPUTS ---
st.sidebar.header("Pricing Context")
base_price_cr = st.sidebar.number_input("Base Price of Property (Cr)", min_value=0.1, value=2.0, step=0.1)

category = st.radio("Select Category", ["Property Details", "Sectors/Location"], horizontal=True)

if category == "Property Details":
    selected_feature = st.selectbox("Select Feature (Impact of +1 Unit)", available_main)
else:
    selected_feature = st.selectbox("Select Sector (Impact of Location)", sector_features)

# --- MATH (Locked to 1 Unit) ---
feature_idx = feature_names.index(selected_feature)
std_coef = lr.coef_[feature_idx]
original_std = scaler.scale_[feature_idx] 

# Unstandardize & Un-log
actual_log_coef = std_coef / original_std
percentage_increase = np.expm1(actual_log_coef) 
impact_in_lakhs = (base_price_cr * percentage_increase) * 100

# --- RESULTS ---
st.divider()
res_color = "green" if impact_in_lakhs >= 0 else "red"
sign = "+" if impact_in_lakhs >= 0 else ""

label = "Location Premium" if category == "Sectors/Location" else "Impact of +1 Unit"
st.markdown(f"### {label}: <span style='color:{res_color}'>{sign}{impact_in_lakhs:.2f} Lakhs</span>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("New Valuation", f"{base_price_cr + (impact_in_lakhs/100):.2f} Cr")
col2.metric("Price Change (%)", f"{percentage_increase * 100:.2f}%")
col3.metric("Base Price", f"{base_price_cr} Cr")

with st.expander("Technical Summary"):
    st.write(f"Feature: **{selected_feature}**")
    st.write(f"Standardized Weight: `{std_coef:.4f}`")
    st.write(f"Actual Multiplier: `{percentage_increase + 1:.4f}x`")