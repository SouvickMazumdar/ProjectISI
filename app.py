import streamlit as st
import tofler  # Ensure this is correctly imported
import zauba
import pandas as pd

def company_list(csv_file):
    df=pd.read_csv(csv_file)
    l=[" ".join(i.upper().split('_')) for i in df["Name"].to_list()]
    return l
# #004c4c
# CSS for styling##ADD8E6
st.markdown("""
    <style>
    .main {
    background-color: #004c4c;
    }
     .stSelectbox {
        background-color: #ADD8E6; /* Background color */
        color: white /* Text color */
        border: 1px solid #556b2f; /* Border color */
        border-radius: 5px; /* Border radius */
    }
    .stSpinner{
    color: white;
    }
    .heading {
        background-color: teal; 
        margin-top: 5px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px 10px 0 0;
    }
    .output-box {
        font-size: 20px;
        color: #2e4600; 
        background-color: #c2d9b6; 
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
    div.stButton > button {
        width: 100%;
        height: 60px;
        background-color: teal; 
        color: white;
        font-size: 18px;
        border-radius: 12px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="heading">letsCOMPARE</div>', unsafe_allow_html=True)
file_name="Companies_list.csv"
company_option=company_list(file_name)
col1, col2 = st.columns(2)
# ['ADANI POWER LIMITED', 'ADANI WATER LIMITED', 'ADANI LOGISTICS LIMITED', 'Option Z']
with col1:
    option1 = st.selectbox('Select source of Information:', ['Tofler', 'Zauba Corp'],index=None)

with col2:
    option2 = st.selectbox('Select the company:', company_option,index=None)

if st.button('Lets Compare'):
    with st.spinner("Fetching Data...."):
        if option1 == 'Tofler':
            content, fin_table,cn_image, content_dir, directors = tofler.content(option2)  # Ensure this returns a string or appropriate content
            if content=="":
                st.markdown('<div class="heading">No Data Found</div>', unsafe_allow_html=True)
            else:
                # Overview Section
                st.markdown('<div class="heading">OverView</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{content}</div>', unsafe_allow_html=True)

                # Financial Section
                if fin_table!="":
                    fin_table = pd.DataFrame(fin_table,columns=["Opertating Revenue","Over INR 500 cr"])
                    fin_table.index = range(1, len(fin_table) + 1)
                    st.markdown('<div class="heading">Financial</div>', unsafe_allow_html=True)
                    st.dataframe(fin_table, use_container_width=True)
                # Company Networks 
                if cn_image!="":
                    st.markdown('<div class="heading">Company Networks</div>', unsafe_allow_html=True)
                    st.image(cn_image, caption="Company Networks", use_column_width=True)
                # Directors
                if directors!="":
                    table=pd.DataFrame(directors,columns=["Date","Name","Designation"])
                    table.index = range(1, len(table) + 1)
                    st.markdown('<div class="heading">Directors</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="output-box">{content_dir}</div>', unsafe_allow_html=True)
                    st.dataframe(table,use_container_width=True) 


                
        if option1 == 'Zauba Corp':
            content,basic_table,directors_table,past_directors_table = zauba.content(option2)  # Ensure this returns a string or appropriate content

            if content=="":
                st.markdown('<div class="heading">No Data Found. Try other company</div>', unsafe_allow_html=True)
            else:
                # Overview Section
                st.markdown('<div class="heading">Basic Information</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{content}</div>', unsafe_allow_html=True)

                # Financial Section
                if list(basic_table)!="":
                    st.markdown('<div class="heading">Company Details</div>', unsafe_allow_html=True)
                    st.dataframe(basic_table,use_container_width=True)
                if list(directors_table)!="":
                    st.markdown('<div class="heading">Current Directors Details</div>', unsafe_allow_html=True)
                    st.dataframe(directors_table,use_container_width=True)
                if list(past_directors_table)!="":
                    st.markdown('<div class="heading">Past Director Details</div>', unsafe_allow_html=True)
                    st.dataframe(past_directors_table,use_container_width=True)


