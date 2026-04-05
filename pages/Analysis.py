import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Real Estate Analytics", layout="wide")

st.title("🏠 Real Estate Analytics Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv('datasets/fixed_missing_latlong.csv')
    return df

@st.cache_data
def load_wordcloud():
    return pickle.load(open('datasets/word_cloud.pkl','rb'))

new_df = load_data()
feature_text = load_wordcloud()

# ---------------- GROUP DATA ----------------
group_df = new_df.groupby('sector').mean(numeric_only=True)[
    ['price','price_per_sqft','built_up_area','latitude','longitude']
].reset_index()

# ---------------- MAP ----------------
st.header('📍 Sector Price per Sqft Geomap')

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    hover_name="sector",
    text="sector",
    zoom=11,
    color_continuous_scale="Viridis"
)

fig.update_traces(
    textposition="top center",
    marker=dict(size=10, opacity=0.8)
)

fig.update_layout(
    mapbox_style="carto-positron",
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)


st.header('Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")

st.pyplot(fig)

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3, ax = plt.subplots(figsize=(10, 4))

sns.histplot(new_df[new_df['property_type'] == 'house']['price'],
             kde=True, label='house', ax=ax)

sns.histplot(new_df[new_df['property_type'] == 'flat']['price'],
             kde=True, label='flat', ax=ax)

ax.legend()

st.pyplot(fig3)