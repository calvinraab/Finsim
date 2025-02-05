import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.title("📈 Present Value of Future Investment Calculator")

# Sidebar Inputs
st.sidebar.header("Investment Parameters")

# User Inputs
initial_amount = st.sidebar.number_input("Initial Investment ($)", min_value=0, value=10_000, step=1000)
investment_increase = st.sidebar.number_input("Annual Return Rate (%)", min_value=0.0, max_value=100.0, value=8.0, step=0.1) / 100
yearly_contribution = st.sidebar.number_input("Annual Contribution ($)", min_value=0, value=6_000, step=1000)
contribution_growth = st.sidebar.number_input("Contribution Growth Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
inflation_rate = st.sidebar.number_input("Inflation Rate (%)", min_value=0.0, max_value=100.0, value=3.0, step=0.1) / 100
years = st.sidebar.slider("Number of Years to Project", min_value=1, max_value=100, value=50)
starting_age = st.sidebar.number_input("Starting Age", min_value=18, max_value=200, value=30)
starting_year = st.sidebar.number_input("Starting Year", min_value=1900, max_value=2200, value=2025)

# Initialize dataframe
data = []
total_deposits = initial_amount  
total_interest = 0  
balance = initial_amount  

for year in range(0, years + 1):  
    age = starting_age + year  
    future_year = starting_year + year  

    # Add the yearly contribution
    balance += yearly_contribution
    total_deposits += yearly_contribution  

    # Interest earned
    interest = balance * investment_increase
    balance += interest  
    total_interest += interest  

    # Adjust for inflation
    pv_balance = balance / ((1 + inflation_rate) ** year)
    pv_deposits = total_deposits / ((1 + inflation_rate) ** year)

    # Store data
    data.append([future_year, age, yearly_contribution, interest, total_deposits, total_interest, balance, pv_balance, pv_deposits])

    # Increase yearly contribution for next year
    yearly_contribution *= (1 + contribution_growth)

# Convert to DataFrame
df = pd.DataFrame(data, columns=[
    "Year", "Age", "Deposits", "Interest", "Total Deposits", "Accrued Interest", "Balance", "Balance 2025 Dollars", "Deposits 2025 Dollars"
]).round(2)

# Plot using Plotly
fig = px.line(df, x="Age", y=["Balance", "Balance 2025 Dollars", "Total Deposits", "Deposits 2025 Dollars"],
              labels={"value": "Dollars ($)", "Age": "Age"},
              title="Projected Investment Growth Over Time",
              markers=True)

fig.update_layout(yaxis_title="Value ($)", xaxis_title="Age", template="plotly_dark")

# Display Results
st.plotly_chart(fig)

st.subheader("📊 Detailed Data Table")
st.dataframe(df)

# Option to Download CSV
st.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False),
    file_name="investment_projection.csv",
    mime="text/csv"
)
