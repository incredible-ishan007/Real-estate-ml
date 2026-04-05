import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Property Recommender", page_icon="🏢", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .stDataFrame { border-radius: 10px; }
    .recommendation-card {
        background-color: #ffffff;
        padding: 15px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
@st.cache_resource
def load_recommender_data():
    location_df = pickle.load(open('datasets/location_distance.pkl','rb'))
    cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
    cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
    cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_recommender_data()

# --- RECOMMENDATION LOGIC ---
def recommend_properties_with_scores(property_name, top_n=5):
    # Weighted Similarity Matrix
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    
    # Get index of the property
    idx = location_df.index.get_loc(property_name)
    
    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    
    # Sort and get top N (excluding itself)
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    
    return pd.DataFrame({
        'PropertyName': location_df.index[top_indices].tolist(),
        'Score': top_scores
    })

# --- UI LAYOUT ---
st.title("🏢 Property Discovery & Recommendations")
st.markdown("Find properties near your favorite locations or discover similar apartments.")

tab1, tab2 = st.tabs(["📍 Search by Radius", "⭐ Similar Properties"])

# --- TAB 1: RADIUS SEARCH ---
with tab1:
    st.subheader("Find Properties Nearby")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_location = st.selectbox('Select Location/Landmark', sorted(location_df.columns.to_list()))
    with col2:
        radius = st.number_input('Radius (Kms)', min_value=0.5, value=5.0, step=0.5)
    
    if st.button('Search Nearby'):
        # Convert radius to meters
        result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()
        
        if result_ser.empty:
            st.warning("No properties found within this radius.")
        else:
            st.success(f"Found {len(result_ser)} properties within {radius} km of {selected_location}")
            
            # Display as a clean list with distance metrics
            for key, value in result_ser.items():
                dist_km = round(value/1000, 2)
                st.markdown(f"""
                <div class="recommendation-card">
                    <strong>{key}</strong><br>
                    <span style='color: #666;'>Distance: {dist_km} kms</span>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 2: CONTENT RECOMMENDATION ---
with tab2:
    st.subheader("Discover Similar Apartments")
    selected_appartment = st.selectbox('Select an Apartment you like', sorted(location_df.index.to_list()))
    
    if st.button('Get Recommendations'):
        rec_df = recommend_properties_with_scores(selected_appartment)
        
        st.write(f"Properties most similar to **{selected_appartment}**:")
        
        for i, row in rec_df.iterrows():
            col_name, col_score = st.columns([3, 2])
            with col_name:
                st.markdown(f"**{i+1}. {row['PropertyName']}**")
            with col_score:
                # Show similarity as a progress bar
                st.progress(min(row['Score'], 1.0))
                st.caption(f"Match Score: {round(row['Score']*100, 1)}%")

st.divider()
st.caption("Note: Similarity is calculated based on facilities, price points, and location proximity.")