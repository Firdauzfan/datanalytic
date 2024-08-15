import streamlit as st

import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Loan Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("<h1 style='text-align: center;'>Financial Insights Dashboard: Loan Performance & Trends</h1>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar section
st.sidebar.title("Dashboard Filters and Features")

# List of Features
st.sidebar.header("Features")
st.sidebar.write("""
- **Overview**: Provides a summary of key loan metrics.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
""")


## ----- Import Data ------
loan = pd.read_pickle('data_input/loan_clean')




## ----- OVERVIEW ------

with st.container(border=True):

    # First row of two columns
    col1, col2 = st.columns(2)

    # Metrics for the first row
    col1.metric("Total Loans", f"{loan.shape[0]:,}")
    col1.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}")

    col2.metric("Average Interest Rate", f"{loan['interest_rate'].mean():.0f}%")
    col2.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}")


## ----- TIME_BASED ANALYSIS ------

### -------------- Wrangling And Visualization

# Data wrangling: Aggregate number of loans issued per date

# **1. Loans Issued Over Time**

data_agg = loan.groupby(['issue_date']).count()['id'].reset_index()

loans_inssued = px.line(
    data_agg,
    x='issue_date',
    y='id',
    markers=True,
    title='Number of Loans Issued Over Time',
    labels={
        'issue_date': 'Issue Date',
        'id': 'Number of Loans'
    },
    template="seaborn"
)

# **2. Loan Amount Over Time**
# Data wrangling: Aggregate total loan amount per date
data_amount_agg = loan.groupby(['issue_date'])['loan_amount'].sum().reset_index()

# Create a line chart for the total loan amount over time
loan_amount = px.line(
    data_amount_agg,
    x='issue_date',
    y='loan_amount',
    markers=True,
    title='Total Loan Amount Issued Over Time',
    labels={
        'issue_date': 'Issue Date',
        'loan_amount': 'Total Loan Amount'
    },
    template="seaborn"
)

# **3. Issue Date Analysis**

# Data wrangling: Count the number of loans issued per weekday
weekday_counts = loan['issue_weekday'].value_counts().sort_index()

# Create a bar chart for loan distribution by day of the week
issue_date = px.bar(
    weekday_counts,
    x=weekday_counts.index,
    y=weekday_counts.values,
    labels={
        'issue_weekday': 'Day of the Week',
        'y': 'Number of Loans'
    },
    title='Distribution of Loans by Day of the Week',
    template="seaborn"
)

### ------- Display Dashboard

with st.container(border=True):

    tab1, tab2, tab3 = st.tabs([
        'Loans Issued Over Time',
        'Loan Amount Over Time',
        'Issue Date Analysis'
    ])

    with tab1:
        st.plotly_chart(loans_inssued)

    with tab2:
        st.plotly_chart(loan_amount)

    with tab3:
        st.plotly_chart(issue_date)


## ----- LOAN PERFORMANCE ------
st.subheader('Loan Performance')

### -------------- Wrangling And Visualization

# **1. Loan Condition Analysis**

# # Calculate the distribution of loan conditions
loan_condition_counts = loan['loan_condition'].value_counts()

# Create a pie chart for loan condition analysis
loan_pie = px.pie(
    loan_condition_counts,
    names=loan_condition_counts.index,
    values=loan_condition_counts.values,
    hole=0.4,
    labels={
        'loan_condition': 'Loan Condition',
        'value': 'Number of Loans'
    },
    title='Distribution of Loans by Condition',
    template="seaborn",
)

# **2. Grade Distribution**

# Calculate the distribution of loan grades
grade_counts = loan['grade'].value_counts(sort=False)

# Create a bar chart for grade distribution
grade_bar = px.bar(
    grade_counts,
    x=grade_counts.index,
    y=grade_counts.values,
    labels={
        'grade': 'Grade',
        'y': 'Number of Loans'
    },
    title='Distribution of Loans by Grade',
    template="seaborn",
)


### ------- Display Dashboard

with st.expander("  ", expanded=True):
    performance1, performance2 = st.columns(2)

    with performance1:
        st.plotly_chart(loan_pie)

    with performance2:
        st.plotly_chart(grade_bar)


st.markdown("---")

## ----- FINANCIAL ANALYSIS ------

st.subheader('Financial Analysis')

### ******* SELECT BOX **********
# List unique loan conditions for the selectbox
loan_conditions = loan['loan_condition'].unique()

# Create a selectbox in the sidebar for filtering loan conditions
selected_condition = st.selectbox(
    "Select Loan Condition",
    options=loan_conditions,
    index=0  # Default selected index
)

# Filter data based on selected loan condition
condition = loan[loan['loan_condition'] == selected_condition]

### -------------- Wrangling And Visualization

# **1. Loan Amount Distribution**
loan_amount_hist = px.histogram(
    condition,
    x='loan_amount',
    nbins=30,  # Number of bins in the histogram
    color='term',
    title='Loan Amount Distribution by Condition',
    template='seaborn',
    labels={
        'loan_amount': 'Loan Amount',
        'term': 'Loan Term'
    }
)

# **2. Loan Amount Distribution by Purpose**
loan_amount_box = px.box(
    condition,
    x='purpose',
    y='loan_amount',
    color='term',
    title='Loan Amount Distribution by Purpose',
    template='seaborn',
    labels={
        'loan_amount': 'Loan Amount',
        'term': 'Loan Term',
        'purpose': 'Loan Purpose'
    }
)

### ------- Display Dashboard
with st.container(border=True):

    tab1, tab2 = st.tabs([
        'Loan Amount Distribution',
        'Loan Amount Distribution by Purpose',
    ])

    with tab1:
        st.plotly_chart(loan_amount_hist)

    with tab2:
        st.plotly_chart(loan_amount_box)





# Footer
footer_content = """
---

© 2024 Dwi Gustin Nurdialit
"""
st.markdown(f"<h1 style='text-align: center;'>{footer_content}</h1>", unsafe_allow_html=True)

