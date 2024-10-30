import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration - This must be the first Streamlit command
st.set_page_config(page_title="Customer Analysis Dashboard", layout="wide")

file_path = './CUST.csv'
data = pd.read_csv(file_path, engine='python')

# Title of the dashboard
st.markdown("<h1 style='text-align: center;'>Customer Analysis Dashboard</h1>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Select Region", options=data['REGION'].unique(), default=data['REGION'].unique(), help="Filter by region")
selected_marital_status = st.sidebar.multiselect("Select Marital Status", options=data['MARITAL_STATUS'].unique(), default=data['MARITAL_STATUS'].unique(), help="Filter by marital status")
selected_age_range = st.sidebar.slider("Select Age Range", int(data['AGE'].min()), int(data['AGE'].max()), (int(data['AGE'].min()), int(data['AGE'].max())), help="Filter by age range")
selected_salary_range = st.sidebar.slider("Select Salary Range", int(data['SALARY'].min()), int(data['SALARY'].max()), (int(data['SALARY'].min()), int(data['SALARY'].max())), help="Filter by salary range")

# Filter the data based on sidebar inputs
filtered_data = data[
    (data['REGION'].isin(selected_region)) &
    (data['MARITAL_STATUS'].isin(selected_marital_status)) &
    (data['AGE'].between(selected_age_range[0], selected_age_range[1])) &
    (data['SALARY'].between(selected_salary_range[0], selected_salary_range[1]))
]

# Display filtered data (toggleable)
if st.sidebar.checkbox("Show Filtered Data", False):
    st.write(f"Filtered Data for selected filters")
    st.dataframe(filtered_data)

# KPIs (Key Performance Indicators)
st.markdown("<h2 style='text-align: center;'>Key Performance Indicators (KPIs)</h2>", unsafe_allow_html=True)

# Define CSS styles for the KPI cards
kpi_style = """
<style>
.kpi-card {
    background-color: #2E2E2E; /* Dark background */
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1); /* Lighter shadow */
    text-align: center;
    color: #FFFFFF; /* White text */
}
</style>
"""

st.markdown(kpi_style, unsafe_allow_html=True)

# Create KPI columns with styled cards
kpi_col1, kpi_col2, kpi_col3,kpi_col4 = st.columns(4)

with kpi_col1:
    avg_ltv = filtered_data['LTV'].mean()
    st.markdown(f'<div class="kpi-card"><h3>Average LTV</h3><p>${avg_ltv:,.2f}</p></div>', unsafe_allow_html=True)

with kpi_col2:
    purchase_percentage = (filtered_data['BUY_INSURANCE'].value_counts(normalize=True).get('Yes', 0)) * 100
    st.markdown(f'<div class="kpi-card"><h3>Insurance Purchased Percentage</h3><p>{purchase_percentage:.2f}%</p></div>', unsafe_allow_html=True)
with kpi_col4:
    avg_salary = filtered_data['SALARY'].mean()
    st.markdown(f'<div class="kpi-card"><h3>Average Salary</h3><p>${avg_salary:,.2f}</p></div>', unsafe_allow_html=True)


with kpi_col3:
    avg_credit_balance = filtered_data['CREDIT_BALANCE'].mean()
    st.markdown(f'<div class="kpi-card"><h3>Average Credit Balance</h3><p>${avg_credit_balance:,.2f}</p></div>', unsafe_allow_html=True)

# Customer Demographics: House Ownership, Car Ownership & Marital Status in one row
st.markdown("<h2 style='text-align: center;'>Customer Demographics Distribution</h2>", unsafe_allow_html=True)


# Pie Charts in one line with shared legend
pie_col1, pie_col2, pie_col3 = st.columns(3)

# House Ownership Pie Chart
with pie_col1:
    house_ownership_chart = px.pie(
        filtered_data, 
        names='HOUSE_OWNERSHIP', 
        title='House Ownership Distribution',
        labels={'HOUSE_OWNERSHIP': 'House Ownership Status'},
        hole=0.3  # Donut chart style
    )
    st.plotly_chart(house_ownership_chart, use_container_width=True)

# Car Ownership Pie Chart
with pie_col2:
    car_ownership_chart = px.pie(
        filtered_data, 
        names='CAR_OWNERSHIP', 
        title='Car Ownership Distribution',
        labels={'CAR_OWNERSHIP': 'Car Ownership Status'},
        hole=0.3  # Donut chart style
    )
    st.plotly_chart(car_ownership_chart, use_container_width=True)

# Marital Status Pie Chart
with pie_col3:
    marital_status_chart = px.pie(
        filtered_data, 
        names='MARITAL_STATUS', 
        title='Marital Status Distribution',
        labels={'MARITAL_STATUS': 'Marital Status'},
        hole=0.3  # Donut chart style
    )
    st.plotly_chart(marital_status_chart, use_container_width=True)

quantitative_vars = ['CREDIT_BALANCE', 'TIME_AS_CUSTOMER', 'MORTGAGE_AMOUNT', 
                         'BANK_FUNDS', 'N_OF_DEPENDENTS', 'SALARY', 
                         'CREDIT_CARD_LIMITS', 'N_TRANS_WEB_BANK', 
                         'N_TRANS_KIOSK', 'AGE', 'MONEY_MONTHLY_OVERDRAWN', 'T_AMOUNT_AUTOM_PAYMENTS', 'N_TRANS_TELLER', 
                         'CHECKING_AMOUNT', 'N_TRANS_ATM', 'N_MORTGAGES',"LTV"]
qualitative_vars1 = ['SEX','REGION','STATE','HAS_CHILDREN','HOUSE_OWNERSHIP','BUY_INSURANCE']
# Custom Pie Chart: User can select a qualitative variable
# Combine Custom Pie Chart and Histogram in one row
st.markdown("<h2 style='text-align: center;'>Univariate Analysis</h2>", unsafe_allow_html=True)

# Create two columns to display the pie chart and histogram side by side
hist_col, pie_col = st.columns(2)

# Pie Chart for Qualitative Variable
with pie_col:
    st.markdown("#### Qualitative Predictors")
    # Select a Qualitative Variable for Pie Chart
    selected_qual_var = st.selectbox("Select a Qualitative Variable for Pie Chart", qualitative_vars1,index=qualitative_vars1.index('BUY_INSURANCE'))
    
    # Create a pie chart for the selected qualitative variable
    qual_pie_chart = px.pie(
        filtered_data, 
        names=selected_qual_var, 
        title=f'Distribution of {selected_qual_var.replace("_", " ").title()}',
        labels={selected_qual_var: selected_qual_var.replace("_", " ").title()},
        hole=0.3  # Add a hole to make it a donut chart
    )
    # Display the pie chart
    st.plotly_chart(qual_pie_chart, use_container_width=True)

# Histogram for Quantitative Variable
with hist_col:
    st.markdown("#### Quantitative Predictors")
    # Select a Quantitative Variable for Histogram
    selected_quant_var = st.selectbox("Select a Quantitative Variable for Histogram", quantitative_vars, index=quantitative_vars.index('LTV'))
    
    # Create a histogram for the selected quantitative variable
    quant_histogram = px.histogram(
        filtered_data, 
        x=selected_quant_var, 
        nbins=50, 
        title=f'Distribution of {selected_quant_var.replace("_", " ").title()}',
        labels={selected_quant_var: selected_quant_var.replace("_", " ").title()}
    )
    # Display the histogram
    st.plotly_chart(quant_histogram, use_container_width=True)


# Combine Box Plot and Scatter Plot in one row
st.markdown("<h2 style='text-align: center;'>LTV Analysis</h2>", unsafe_allow_html=True)
box_col, scatter_col = st.columns(2)

# Box Plot for LTV with Qualitative Variables
with box_col:
    st.markdown("#### With Qualitative Predictors")
    # Define the qualitative variables
    qualitative_vars = ['SEX','REGION','STATE','HAS_CHILDREN','HOUSE_OWNERSHIP','PROFESSION']
    
    # Select the qualitative variable for the x-axis
    x_axis_box = st.selectbox("Select the Predictor Variable", qualitative_vars)
    
    # Create the box plot using Plotly
    box_custom = px.box(
        filtered_data, 
        x=x_axis_box, 
        y='LTV', 
        title=f'LTV vs {x_axis_box}',
        labels={x_axis_box: x_axis_box.replace("_", " ").title(), 'LTV': 'LTV'},
        hover_data=['CREDIT_BALANCE', 'SALARY']  # Additional data to show on hover
    )
    
    # Display the box plot
    st.plotly_chart(box_custom, use_container_width=True)

# Scatter Plot for LTV with Quantitative Variables
with scatter_col:
    st.markdown("#### With Quantitative Predictors")
    quantitative_vars = ['CREDIT_BALANCE', 'TIME_AS_CUSTOMER', 'MORTGAGE_AMOUNT', 
                         'BANK_FUNDS', 'N_OF_DEPENDENTS', 'SALARY', 
                         'CREDIT_CARD_LIMITS', 'N_TRANS_WEB_BANK', 
                         'N_TRANS_KIOSK', 'AGE', 'MONEY_MONTHLY_OVERDRAWN', 'T_AMOUNT_AUTOM_PAYMENTS', 'N_TRANS_TELLER', 
                         'CHECKING_AMOUNT', 'N_TRANS_ATM', 'N_MORTGAGES',"LTV"]
    
    x_axis = st.selectbox("Select Predictor variable", quantitative_vars, index=quantitative_vars.index('CREDIT_BALANCE'))
    
    scatter_custom = px.scatter(
        filtered_data, 
        x=x_axis, 
        y='LTV',  
        title=f'{x_axis} vs LTV',
        labels={x_axis: x_axis.replace("_", " ").title(), 'LTV': 'LTV'},
        hover_data=['PROFESSION','MARITAL_STATUS']
    )
    
    st.plotly_chart(scatter_custom, use_container_width=True)
st.markdown("<h2 style='text-align: center;'> Insurance Purchase Decision Analysis</h2>", unsafe_allow_html=True)

# Create two columns: one for the Stacked Bar Chart and one for the Box Plot
box_col, bar_col = st.columns(2)

# Stacked Bar Chart for Qualitative Variables with the Binary Response
with bar_col:
    st.markdown("#### With Qualitative Predictors")
    
    # Define the qualitative variables
    qualitative_vars = ['SEX', 'REGION', 'STATE', 'HAS_CHILDREN', 'HOUSE_OWNERSHIP', 'PROFESSION']
    
    # Select the qualitative variable for the x-axis
    x_axis_bar = st.selectbox("Select the Qualitative Predictor Variable", qualitative_vars)
    
    # Calculate the percentage within each category of the qualitative variable
    stacked_data = filtered_data.groupby([x_axis_bar, 'BUY_INSURANCE']).size().reset_index(name='count')
    total_per_category = stacked_data.groupby(x_axis_bar)['count'].transform('sum')
    stacked_data['percentage'] = stacked_data['count'] / total_per_category * 100
    
    # Create the stacked bar chart with 100% bars
    stacked_bar_chart = px.bar(
        stacked_data, 
        x=x_axis_bar, 
        y='percentage', 
        color='BUY_INSURANCE',  # Color by the binary response variable
        barmode='stack',  # Stack bars on top of each other
        title=f'{x_axis_bar} vs BUY INSURANCE',
        labels={x_axis_bar: x_axis_bar.replace("_", " ").title(), 'BUY_INSURANCE': 'Buy Insurance', 'percentage': 'Percentage'},
        hover_data=['count']  # Show raw count on hover
    )
    
    # Update y-axis to show percentage (0-100%) and set the range
    stacked_bar_chart.update_layout(
        yaxis=dict(
            title='Percentage',
            range=[0, 100],  # Set y-axis range from 0 to 100
            tickvals=list(range(0, 101, 10)),  # Set ticks at intervals of 10
            ticktext=[f"{i}%" for i in range(0, 101, 10)]  # Set tick labels as percentages
        )
    )

    # Display the stacked bar chart
    st.plotly_chart(stacked_bar_chart, use_container_width=True)

# Side-by-Side Box Plot for Quantitative Variables with the Binary Response
with box_col:
    st.markdown("#### With Quantitative Predictors")
    
    # Define the quantitative variables
    quantitative_vars = ['CREDIT_BALANCE', 'TIME_AS_CUSTOMER', 'MORTGAGE_AMOUNT', 'BANK_FUNDS', 'SALARY', 'AGE', 'CHECKING_AMOUNT', 'N_MORTGAGES']
    
    # Select the quantitative variable for the x-axis
    x_axis_box = st.selectbox("Select Quantitative Predictor Variable", quantitative_vars,index=quantitative_vars.index('SALARY'))

    # Create the box plot using Plotly, with 'BUY_INSURANCE' as the color to separate box plots and excluding outliers
    box_plot = px.box(
        filtered_data, 
        x='BUY_INSURANCE',  # The binary response variable on x-axis
        y=x_axis_box,  # The quantitative predictor variable
        color='BUY_INSURANCE',  # Color by the binary response
        title=f'{x_axis_box} vs BUY INSURANCE',
        labels={'BUY_INSURANCE': 'Buy Insurance', x_axis_box: x_axis_box.replace("_", " ").title()},
        hover_data=['PROFESSION', 'MARITAL_STATUS'],  # Additional data to show on hover
        points=False  # Disable outliers to remove them from the plot
    )
    
    # Display the box plot
    st.plotly_chart(box_plot, use_container_width=True)
