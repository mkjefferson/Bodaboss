import streamlit as st
import pandas as pd 
import numpy as np 
from datetime import timedelta
from datetime import date
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
# Score Card Design
st.markdown("""
<style>
.metric-box{
        background-color: ;
        padding: 0.0rem;
        margin: 0.1rem;
        border-radius: 0.5rem;
        box-shadow: 0px 2px 6px rgba(0,0,0,5);
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        
}
.metric-box h2{
        margin: -1rem;
        padding-top: 0 rem;
            
}     
.metric-box h5{
    margin: 0rem;

}      

</style>
""", unsafe_allow_html = True)



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
        st.error(f"Please upload a file or ensure {default_file} exists")
        st.stop()


# Detecting Categorical Variables
categorical_cols = [col for col in df.select_dtypes(include=["object", "category"]).columns if 20 <= df[col].nunique(dropna = True) <= 52 ]
# Variable to hold filtered selection 
filtered_selection = {}

    # Date pickers
filtered_df = df.copy()
date_col = None
for col in df.columns:
    if df[col].dtype in ['object', 'datetime64[ns]']:
        try:
            converted = pd.to_datetime(df[col], errors = 'coerce', infer_datetime_format = True)
            # Require at lead 50% of the values to be valid dates
            if converted.notna().mean() > 0.5:
                df[col] = converted
                date_col = col
                break
        except Exception as e:
            continue
# Fall back to Year column if no proper date time is found
if date_col is None and 'Year' in df.columns:
    try:
        df['Year'] = pd.to_datetime(df['Year'], format = '%Y', errors = 'coerce')
        if df['Year'].notna().sum() > 0:
            date_col = 'Year'
            df = df.dropna(subset = ['Year'])
            # st.markdown("***Fallback to 'Year' column for date filtering")
    except Exception as e:
        pass
col1, col2, col3 = st.columns(3)
with col1: 
    if date_col:
        # st.markdown(f"**Date Column Detected: ** `{date_col}`")
        # Drop the rows where date parsing failed 
        df = df.dropna(subset = [date_col])

        # Get the actual min and max date
        startDate = df[date_col].min().date()
        endDate = df[date_col].max().date()

        # Displaying the date pickers with the data's date range
        date1 = st.date_input('Start Date', startDate, min_value = startDate, max_value = endDate)
        date2 = st.date_input('End Date', endDate, min_value = startDate, max_value = endDate)

        # Filter the dataframe based on the selected date 
        mask = (df[date_col].dt.date >= date1) & (df[date_col].dt.date <= date2)
        filtered_df = df.loc[mask]
    else:
        st.warning("No Valid date in the file date detected")    

with col2:
    for col in categorical_cols:
        filtered_selection[col] = st.multiselect(
        f"Select: {col}",
        options = filtered_df[col].unique()
        )

    for col, selection in filtered_selection.items():
        if selection:
            filtered_df = filtered_df[filtered_df[col].isin(selection)]
with col3:
    categorical_cols2 = [col for col in df.select_dtypes(include=["object", "category"]).columns if df[col].nunique(dropna = True) <= 2]
    for col in categorical_cols2:
        filtered_selection[col] = st.multiselect(
            f"Select {col}",
            options = filtered_df[col].unique()
        )
    for col, selection in filtered_selection.items():
        if selection: 
            filtered_df = filtered_df[filtered_df[col].isin(selection)]

total_sales = filtered_df['SALES'].sum() if 'SALES' in filtered_df.columns else 0
cog = filtered_df['COG'].sum() if 'COG' in filtered_df.columns else 0
profits = total_sales - cog
total_qty = filtered_df['QTY'].sum() if 'QTY' in filtered_df.columns else 0
roi =  (profits/cog)*100    
colA1, colB1, colC1, colD1, colE1 = st.columns(5)
with colA1:
        st.markdown(f"""
        <div class = "metric-box">
            <h4>Sales</h4>
            <h2>Ksh. {total_sales:,.2f}</h2>
            <p></p> 
        </div>
        """, unsafe_allow_html = True)

with colB1:
    st.markdown(f"""
    <div class = "metric-box">
        <h4>COG</h4>
        <h2>{cog:,.2f}</h2>
        <p></p>
    </div>
    """, unsafe_allow_html = True)
with colC1:
    st.markdown(f"""
    <div class = "metric-box">
        <h4>Profits</h4>
        <h2>Ksh. {profits:,.2f}</h2>
        <p></p>
    </div>
    
    """, unsafe_allow_html = True)

with colD1:
    st.markdown(f"""
    <div class = "metric-box">
        <h4>QTY</h4>
        <h2>{total_qty}</h2>
        <p></p>
    </div> 
    """, unsafe_allow_html = True)

with colE1:
    st.markdown(f"""
    <div class = "metric-box">
        <h4>ROI</h4>
        <h2>{roi:,.2f}%</h2>
        <p></p>
    </div>
    
    """, unsafe_allow_html = True)

colAA, colAB, colAC = st.columns(3)

st.markdown("""
<style>
  .infographics-box{
        background-color:;
        padding: 12rem;
        margin: 1rem; 
        box-shadow: 0px 2px 6px rgba(0,0,0,5);
        border-radius: 12px;     
            
    }          
           
</style>
""", unsafe_allow_html = True)
st.markdown("""
<style>
  .calender{
        background-color:;
        padding: 12rem;
        margin: 1rem; 
        box-shadow: 0px 2px 6px rgba(0,0,0,5);
        border-radius: 12px;
        display: flex; 
        flex-direction: column;
        align-items: center;     
            
    }
    .calendar-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2e4d;
        margin-bottom: 1rem;
    }
    [data-testid="stDateInput"] {
        width: 100%;
        text-align: center;
    }         
           
</style>
""", unsafe_allow_html = True)
st.markdown("""
<style>
  .line-graph{
        background-color:;
        padding: 12rem;
        margin: 1rem; 
        box-shadow: 0px 2px 6px rgba(0,0,0,5);
        border-radius: 12px;     
            
    }          
           
</style>
""", unsafe_allow_html = True)

colBB, colCC, colDD = st.columns([1, 2, 1])
with colBB:
    st.markdown('<div class = "calender">', unsafe_allow_html = True)
    # selected_date = st.date_input("Pick a date", value = date.today(), key = "calendar_input")
    st.markdown('</div', unsafe_allow_html = True)
with colCC:
    st.markdown("""
    <div class = "line-graph">
    
                
    </div>
    
    """, unsafe_allow_html = True)
with colDD: 
    st.markdown("""
    <div class = "infographics-box">
    
                
    </div>
    
    """, unsafe_allow_html = True)
colBBB, colCCC, colDDD, colEEE = st.columns(4)

with colBBB:
    st.markdown("""
    <div class = "infographics-box">
    
                
                
    </div>
    """, unsafe_allow_html = True)
with colCCC:
        st.markdown("""
    <div class = "infographics-box">
    
                
                
    </div>
    """, unsafe_allow_html = True)
with colDDD:
         st.markdown("""
    <div class = "infographics-box">
    
                
                
    </div>
    """, unsafe_allow_html = True)
with colEEE:
         st.markdown("""
    <div class = "infographics-box">
    
                
                
    </div>
    """, unsafe_allow_html = True)
with st.expander(f"Raw Unfiltered Data: {filename}."):
        st.write(df) 
with st.expander(f"Filtered Data "):
        st.write(filtered_df) 
 