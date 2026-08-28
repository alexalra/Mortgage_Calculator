import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime, date
import requests
from fpdf import FPDF

# Page setup
st.set_page_config(page_title="Interactive Mortgage Calculator", page_icon="🏠", layout="wide")

# --- 1. DYNAMIC EURIBOR API FETCH ---
@st.cache_data(ttl=86400)  # Cache rate for 24 hours

def fetch_latest_euribor_6m():
    """Fetches the latest 6-month Euribor rate from the European Central Bank API."""
    url = "https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA?lastNObservations=1&detail=dataonly&format=jsondata"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Navigate the nested ECB JSON structure
            series = data['dataSets'][0]['series']
            series_key = list(series.keys())[0]
            obs = series[series_key]['observations']
            latest_obs_key = list(obs.keys())[0]
            rate = float(obs[latest_obs_key][0])
            return round(rate, 3)
    except Exception as e:
        pass
    return 3.0  # Safe modern fallback if API is down

# --- 2. CORE MORTGAGE ENGINE ---
def calculate_mortgage(total_cost, down_payment, euribor_rate, bank_margin, start_date, years):

    loan_amount = total_cost - down_payment
    total_interest_rate = euribor_rate + bank_margin
    total_months = int(years * 12)
    
    # Monthly interest rate
    r = (total_interest_rate / 100) / 12
    
    # Standard Amortization Formula
    if r > 0:
        monthly_payment = loan_amount * (r * (1 + r)**total_months) / ((1 + r)**total_months - 1)
    else:
        monthly_payment = loan_amount / total_months
        
    # Vectorized schedule generation
    dates = pd.date_range(start=start_date, periods=total_months, freq='MS')
    
    balances = []
    interest_payments = []
    principal_payments = []
    
    current_balance = loan_amount
    for _ in range(total_months):
        interest_this_month = current_balance * r
        principal_this_month = monthly_payment - interest_this_month
        
        # Guard against minor floating point errors at the end
        if current_balance < principal_this_month:
            principal_this_month = current_balance
            monthly_payment = interest_this_month + principal_this_month
            
        interest_payments.append(interest_this_month)
        principal_payments.append(principal_this_month)
        current_balance -= principal_this_month
        balances.append(max(0.0, current_balance))
        
    df = pd.DataFrame({
        'Payment Date': dates.strftime('%Y-%m-%d'),
        'Monthly Payment': monthly_payment,
        'Interest Paid': interest_payments,
        'Principal Paid': principal_payments,
        'Remaining Balance': balances
    })
    
    # Cumulative values
    df['Cumulative Interest'] = df['Interest Paid'].cumsum()
    df['Cumulative Principal'] = df['Principal Paid'].cumsum()
    df['Total Paid'] = df['Monthly Payment'].cumsum()
    
    return df, loan_amount, total_interest_rate, monthly_payment

# --- 3. STREAMLIT UI ---
st.title("🏠 Interactive Mortgage Calculator")
st.write("Determine your monthly payment.")

# Sidebar inputs
st.sidebar.header("Mortgage Parameters")
total_cost = st.sidebar.number_input("Property Value (EUR)", min_value=10000.0, value=250000.0, step=5000.0)
down_payment = st.sidebar.number_input("Down Payment (EUR)", min_value=0.0, value=50000.0, step=5000.0)

if down_payment >= total_cost:
    st.sidebar.error("Down payment cannot equal or exceed total property cost!")
    st.stop()

# Auto-fetch Euribor
latest_euribor = fetch_latest_euribor_6m()
st.sidebar.subheader("Interest Details")
euribor_rate = st.sidebar.number_input("6-Month EURIBOR (%)", min_value=0.0, value=latest_euribor, step=0.01)
bank_margin = st.sidebar.number_input("Bank Margin (%)", min_value=0.0, value=1.50, step=0.05)

years = st.sidebar.slider("Term Duration (Years)", min_value=1, max_value=40, value=25)
start_date = st.sidebar.date_input("First Payment Date", value=date.today())

# Calculations Execution
df, loan_amount, total_interest, monthly_payment = calculate_mortgage(
    total_cost, down_payment, euribor_rate, bank_margin, start_date, years
)

# Display Key metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Required Loan Amount", f"{loan_amount:,.2f} €")
m2.metric("Combined Interest Rate", f"{total_interest:.3f} %")
m3.metric("Est. Monthly Payment", f"{monthly_payment:,.2f} €")
m4.metric("Total Interest Cost", f"{df['Cumulative Interest'].iloc[-1]:,.2f} €")

# Layout split: Chart & Table
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Amortization Trajectory")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(pd.to_datetime(df['Payment Date']), df['Cumulative Interest'], label='Total Paid in Interest', color="#e74c3c", linewidth=2)
    ax.plot(pd.to_datetime(df['Payment Date']), df['Cumulative Principal'], label='Total Paid in Principal', color="#2ecc71", linewidth=2)
    ax.set_xlabel("Timeline")
    ax.set_ylabel("EUR")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)
    st.pyplot(fig)

with col2:
    st.subheader("Yearly Schedule Snapshot")
    # Transform to yearly presentation
    df_temp = df.copy()
    df_temp['Year'] = pd.to_datetime(df_temp['Payment Date']).dt.year
    df_yearly = df_temp.groupby('Year').agg({
        'Remaining Balance': 'last',
        'Cumulative Interest': 'last',
        'Cumulative Principal': 'last'
    }).reset_index()
    
    st.dataframe(
        df_yearly.style.format({
            'Remaining Balance': '{:,.2f} €',
            'Cumulative Interest': '{:,.2f} €',
            'Cumulative Principal': '{:,.2f} €'
        }),
        use_container_width=True
    )
