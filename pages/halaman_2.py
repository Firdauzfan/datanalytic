import streamlit as st
import pandas as pd
import plotly.express as px
import pages as pg

st.title("Halaman 2")

st.sidebar.header('Dashboard Filters and Features')

st.sidebar.markdown(
    '''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
 '''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose']=loan['purpose'].str.replace("_"," ")

condition=st.selectbox(
    "select loan condition",
    {"Good Loan", "Bad Loan"}
)

with st.container(border=True):
    tab1,tab2= st.tabs(['loan amount distribution','loan amount distribution by purpose'])
    loan_condition = loan[loan['loan_condition'] == condition]
    with tab1:
        lineCount=px.histogram(
        loan_condition,
        x='loan_amount',
        color='term',
        nbins=20,
        template='seaborn',
        labels={
            'loan_amount':'Loan Amount',
            'term':'Loan Term'
        }
    )

        st.plotly_chart(lineCount)

    with tab2:
        lineSum=px.box(
            loan_condition,
            x='purpose',
            y='loan_amount',
            color='term',
            template='seaborn',
            labels={
                'term':'Loan Term',
                'loan_amount':'Loan Amount',
                
            }
        )  

        st.plotly_chart(lineSum)