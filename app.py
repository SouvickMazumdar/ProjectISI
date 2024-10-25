import streamlit as st
import tofler  # Ensure this is correctly imported
import zauba
import pandas as pd
from IPython.display import HTML, display_html
import streamlit.components.v1 as components


def company_list(csv_file):
    df=pd.read_csv(csv_file)
    l=[i.replace(" LTD","").replace(" LTD.","") for i in df["Company Name"].to_list()]
    return l
def path_to_image_html(path):
    return f'<img src="{path}" width="20" height="20">'


def create_financial_table(fin_ar):
    # Create HTML table header
    html = """
    <table border="1" style="width:100%; text-align:center; background-color: white; hieght: 50px">
        <thead">
            <tr>
                <th>Operating Revenue</th>
                <th>Over INR 500 cr</th>
                <th>TOP/DOWN</th>
            </tr>
        </thead>
        <tbody>
    """

    # Add rows to the HTML table
    for row in fin_ar:
        operating_revenue = row[0]
        over_inr_500_cr = row[1]
        up_down_image_base64 = row[2]

        # If the TOP/DOWN column has an image, embed it in the cell
        if up_down_image_base64:
            if over_inr_500_cr[0]=='-':
                up_down_img_tag = f'<img src="data:image/svg;base64,{up_down_image_base64}" width="30"/>'
            else:
                up_down_img_tag = f'<img src="data:image/svg;base64,{up_down_image_base64}" width="30"/>'
        else:
            up_down_img_tag = "N/A"

        html += f"""
        <tr>
            <td>{operating_revenue}</td>
            <td>{over_inr_500_cr}</td>
            <td>{up_down_img_tag}</td>
        </tr>
        """

    html += """
        </tbody>
    </table>
    """
    return html


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
file_name="Company_list.csv"
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
            content, fin_table,key_table, reg_dr, directors, asst_table= tofler.content(option2)  # Ensure this returns a string or appropriate content
            if content=="" and fin_table=="" and key_table=="" and reg_dr=="" and directors=="" and asst_table=="":
                st.markdown('<div class="heading">No Data Found. Try Some other company</div>', unsafe_allow_html=True)
            # Overview Section
            if content!="":
                print(content)
                st.markdown('<div class="heading">OverView</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="output-box">{content}</div>', unsafe_allow_html=True)

            # Financial Section
            if fin_table!="":
                fin_table = pd.DataFrame(fin_table,columns=["","March 2019","March 2020","March 2021","March 2022","March 2023",])
                # del fin_table[fin_table.columns[-1]]
                fin_table.index = range(1, len(fin_table) + 1)

                st.markdown('<div class="heading">Financial Highlights</div>', unsafe_allow_html=True)
                # financial_table_html=create_financial_table(fin_table)
                # components.html(financial_table_html, height=1000)
                st.dataframe(fin_table, use_container_width=True)
            # Company Networks
            if key_table!="":
                table = pd.DataFrame(key_table, columns=["KEY", "VALUE", "INC/DEC"])
                table.index = range(1, len(table) + 1)
                st.markdown('<div class="heading">Key Metrics</div>', unsafe_allow_html=True)
                # st.markdown(f'<div class="output-box">{content_dir}</div>', unsafe_allow_html=True)
                st.dataframe(table, use_container_width=True)
            # Directors
            if directors!="":
                table=pd.DataFrame(directors,columns=["Designation","Name","DIN/PAN","Tenure"])
                table.index = range(1, len(table) + 1)
                st.markdown('<div class="heading">Directors</div>', unsafe_allow_html=True)
                # st.markdown(f'<div class="output-box">{content_dir}</div>', unsafe_allow_html=True)
                st.dataframe(table,use_container_width=True)
            if reg_dr!="":
                table = pd.DataFrame(reg_dr, columns=["TYPE", "Value"])
                table.index = range(1, len(table) + 1)
                st.markdown('<div class="heading">Registration Details</div>', unsafe_allow_html=True)
                # st.markdown(f'<div class="output-box">{content_dir}</div>', unsafe_allow_html=True)
                st.dataframe(table, use_container_width=True)
            if asst_table!="":
                table = pd.DataFrame(asst_table, columns=["Asset Name","No. of Loans","Total Amount"])
                table.index = range(1, len(table) + 1)
                st.markdown('<div class="heading">Charges on Assets</div>', unsafe_allow_html=True)
                # st.markdown(f'<div class="output-box">{content_dir}</div>', unsafe_allow_html=True)
                st.dataframe(table, use_container_width=True)

            # else:
            #     st.markdown('<div class="heading">No Data Found. Try Some other company</div>', unsafe_allow_html=True)


                
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


