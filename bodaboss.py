import streamlit as st
import pandas as pd 
import numpy as np 
import os 
import plotly.express as px
import colorsys
import warnings 
warnings.filterwarnings('ignore')

# Setting the page layout 
st.set_page_config(page_title = "Boda Boss Motorcycle Spares", page_icon = ":runner", layout = 'wide')

# Page title
# st.title(":bar_chart: Boda Boss Motorcylce Spares")

# Styling the title
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Fjalla+One&display=swap" rel="stylesheet">

<style>
        .fancy-font{
            font-family: "Anton", sans-serif;
            font-size: 4rem;
            # font-weight: 4000;
            font-style: normal;
            color: #FF5800;
            
            }
            
</style>
<div class = "fancy-font"> Boda Boss Motorcycle Spares</div>
            
""", unsafe_allow_html = True
)
upload_button = st.sidebar.file_uploader(":file_uploader: Upload a file", type = (["xls","txt","csv","xlsx"]))

# condition for if a user uploads a file
if upload_button is not None: 
    filename = upload_button.name
    st.write(filename)
    df = pd.read_csv(upload_button, encoding = "ISO-8859-1")
else:
    default_file = ""
    if os.path.exists(default_file):
        df = pd.read_csv(default_file, encoding = "ISO-8859-1")
    else:
        st.error("Please upload a file or ensure {default_file} exists")
        st.stop()


# Detecting Categorical Variables
categorical_cols = [col for col in df.columns if df[col].unique() < 20 and df[col].dtype == "object"]

# Variable to hold filtered selection 
filtered_selection = {}

# Date pickers

# Define the layout with 3 columns
col1, col2, col3 = st.columns([1, 3.5, 1])


# Column 1 → right border only
with col1:
    st.write(f"Everything comes here")
    st.markdown("""
        <div style='
            border-right: 3px solid red;
            height: 100vh;
            padding: 10px;
            box-sizing: border-box;
        '>
            🟥 Column 1
        </div>
    """, unsafe_allow_html=True)

# Column 2 → right border only
with col2:
    st.write(f"Everything comes here")
    st.markdown("""
        <div style='
            border-right: 3px solid blue;
            height: 100vh;
            padding: 10px;
            box-sizing: border-box;
        '>
            🟩 Column 2 (Main Content)
        </div>
    """, unsafe_allow_html=True)

    with st.expander("Raw Unfiltered Data: {filename}")
        st.write(df)
    

# Column 3 → no borders
with col3:
    st.write(f"Everything comes here")
    st.markdown("""
        <div style='
            height: 100vh;
            padding: 10px;
            box-sizing: border-box;
        '>
            🟦 Column 3
        </div>
    """, unsafe_allow_html=True)
    

