import streamlit as st
import pandas as pd
import plotly.express as px
import pages as pg

st.set_page_config(
    page_title='Demo Dashboard',
    page_icon="😉" #window dan titik
)

st.title("Financial Insights Dashboard: Finance & Trends")

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

col1,col2= st.columns(2)

with st.container(border=True):
    with col1:
        st.metric('Total Loans', f"{loan['id'].count():,.0f}".replace(',','.'))
        st.metric('Total Loan  Amount', f"${loan['loan_amount'].sum():,.0f}")
    with col2:
        st.metric('Average Interest Rate', f"{loan['interest_rate'].mean():,.0f}")
        st.metric('Average Loan Amount', f"{loan['loan_amount'].mean():,.0f}")

with st.container(border=True):
    tab1,tab2,tab3= st.tabs(['loans issued over time','loan amount over time','issue date analysis'])
    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        lineCount=px.line(
        loan_date_count.sort_index(),
        markers=True,
        labels={
            'issue_date':'Issue Date',
            'value':'Count Loan Amount',
            'variable':'Loan Amount'
            
            }
        ).update_layout(showlegend=False)

        st.plotly_chart(lineCount)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        lineSum=px.line(
        loan_date_sum.sort_index(),
        markers=True,
        labels={
            'issue_date':'Issue Date',
            'value':'Sum Loan Amount',
            'variable':'Loan Amount'     
            }
        ).update_layout(showlegend=False)   

        st.plotly_chart(lineSum)



    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        lineDayCount=px.bar(
        loan_day_count,
        category_orders={
            'issue_weekday':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        },
        labels={
            'issue_weekday':'Issue Weekday',
            'value':'Count Loan Amount',
            'variable':'Loan Amount'
            
        },
        template='seaborn'
        ).update_layout(showlegend=False)  

        st.plotly_chart(lineDayCount)


with st.expander("click here to expand visualization"):
    col3,col4=st.columns(2)
    with col3:
        pie=px.pie(
        loan,
        names='loan_condition',
        hole=0.4,
        title='Distribution of Conditions',
        )
        
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar=px.bar(
        grade,
        title='Distribution of Loans by Grade',
        labels={
            'value':'Numbers of Loans'
        }
        ).update_layout(showlegend=False)

        st.plotly_chart(bar)

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