import streamlit as st
import pandas as pd
from datetime import datetime
import random

# --- CONFIGURATION & MOCK DATA ---
st.set_page_config(page_title="NMIT Pay", page_icon="💸", layout="centered")

if 'balance' not in st.session_state:
    st.session_state.balance = 50000.00
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# --- APP STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #6c5ce7; color: white; border: none; font-weight: bold;}
    .stButton>button:hover { background-color: #5b4bc4; color: white; }
    .balance-card { padding: 20px; background: white; border-radius: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); text-align: center; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("💸 NMIT Pay")
menu = st.sidebar.radio("Navigation", ["Home", "Send Money", "Transaction History", "Profile"])

# --- HOME PAGE ---
if menu == "Home":
    st.title("Welcome back, NMIT Hacker!")
    
    st.markdown(f"""
        <div class="balance-card">
            <h3>Primary Bank Balance</h3>
            <h1 style="color: #2d3436;">₹{st.session_state.balance:,.2f}</h1>
            <p style="color: #636e72;">State Bank of NMIT - XXXX 1234</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rewards", "₹450", "+12")
    col2.metric("Bills Due", "2", "-1")
    col3.metric("Spends (Apr)", "₹4,200")

# --- SEND MONEY ---
elif menu == "Send Money":
    st.header("Transfer Money")
    
    with st.container():
        upi_id = st.text_input("Enter UPI ID (e.g., name@nmit)")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=100.0)
        note = st.text_input("Add a message (Optional)")
        
        if st.button("Proceed to Pay"):
            if "@" not in upi_id:
                st.error("Invalid UPI ID format.")
            elif amount > st.session_state.balance:
                st.error("Insufficient Funds!")
            else:
                # Simulate Transaction logic
                st.session_state.balance -= amount
                tx_id = f"TXN{random.randint(100000, 999999)}"
                new_tx = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Transaction ID": tx_id,
                    "Receiver": upi_id,
                    "Amount": f"-₹{amount}",
                    "Status": "Success"
                }
                st.session_state.transactions.insert(0, new_tx)
                st.success(f"Successfully sent ₹{amount} to {upi_id}!")
                st.balloons()

# --- TRANSACTION HISTORY ---
elif menu == "Transaction History":
    st.header("Recent Transactions")
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        st.table(df)
    else:
        st.info("No transactions found yet.")

# --- PROFILE ---
elif menu == "Profile":
    st.header("Your Profile")
    st.write("**Name:** NMIT Developer")
    st.write("**UPI ID:** nmitdev@nmit")
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=nmitdev@nmit", caption="Your Personal QR")