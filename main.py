import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# --- CONFIGURATION & MOCK DATA ---
st.set_page_config(page_title="NMIT Pay", page_icon="💸", layout="centered")

# Initialize Session States
if 'balance' not in st.session_state:
    st.session_state.balance = 50000.00
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'show_balance' not in st.session_state:
    st.session_state.show_balance = False

# --- APP STYLING ---
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #f8f9fa; }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3em; 
        background-color: #6c5ce7; 
        color: white; 
        border: none; 
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #5b4bc4; color: white; box-shadow: 0 4px 12px rgba(108, 92, 231, 0.4); }
    
    /* Cards */
    .balance-card { 
        padding: 25px; 
        background: linear-gradient(135deg, #ffffff 0%, #f1f2f6 100%); 
        border-radius: 20px; 
        box-shadow: 0px 8px 24px rgba(0,0,0,0.08); 
        text-align: center; 
        margin-bottom: 25px;
        border: 1px solid #e2e8f0;
    }
    
    .transaction-card {
        padding: 15px;
        background: white;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #00b894;
    }
    .transaction-card.debit { border-left-color: #d63031; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
# Using tabs to simulate a mobile app bottom/top navigation bar
tab_home, tab_pay, tab_history, tab_profile = st.tabs(["🏠 Home", "💸 Pay", "📜 History", "👤 Profile"])

# --- 1. HOME TAB ---
with tab_home:
    st.title("Hi, NMIT Hacker 👋")
    
    # Balance Card with Show/Hide Toggle
    balance_display = f"₹{st.session_state.balance:,.2f}" if st.session_state.show_balance else "₹ ••••••"
    
    st.markdown(f"""
        <div class="balance-card">
            <h4 style="color: #636e72; margin-bottom: 5px;">Primary Bank Balance</h4>
            <h1 style="color: #2d3436; margin-top: 0;">{balance_display}</h1>
            <p style="color: #a4b0be; font-size: 14px;">State Bank of NMIT - XXXX 1234</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("👁️ Show / Hide Balance"):
        st.session_state.show_balance = not st.session_state.show_balance
        st.rerun()

    st.write("---")
    st.subheader("Insights")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cashback", "₹450", "+₹12")
    col2.metric("Bills Due", "2", "-1")
    col3.metric("Spends (Apr)", "₹4,200")

# --- 2. SEND MONEY TAB ---
with tab_pay:
    st.header("Send Money securely")
    st.caption("Powered by NMIT UPI")
    
    with st.container():
        upi_id = st.text_input("Enter Receiver UPI ID or Phone", placeholder="e.g., satoshi@nmit")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=100.0, format="%.2f")
        note = st.text_input("Add a note", placeholder="Dinner, Rent, etc.")
        
        st.write("---")
        # Simulated UPI PIN Pad
        pin = st.text_input("Enter 4-Digit UPI PIN", type="password", max_chars=4, placeholder="****")
        
        if st.button("Secure Pay"):
            if not upi_id:
                st.error("Please enter a valid UPI ID.")
            elif amount > st.session_state.balance:
                st.error("Transaction Failed: Insufficient Funds!")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("Security Error: Please enter a valid 4-digit PIN.")
            else:
                # Simulate Bank Processing Time
                with st.spinner("Contacting your bank securely..."):
                    time.sleep(1.5)
                
                with st.spinner("Processing payment..."):
                    time.sleep(1)
                
                # Update State
                st.session_state.balance -= amount
                tx_id = f"T{random.randint(1000000000, 9999999999)}"
                new_tx = {
                    "Date": datetime.now().strftime("%b %d, %H:%M"),
                    "ID": tx_id,
                    "To": upi_id,
                    "Note": note if note else "UPI Payment",
                    "Amount": amount
                }
                st.session_state.transactions.insert(0, new_tx)
                
                st.success(f"Payment of ₹{amount:,.2f} to {upi_id} Successful! ✅")
                st.balloons()

# --- 3. TRANSACTION HISTORY TAB ---
with tab_history:
    st.header("Recent Transactions")
    
    if st.session_state.transactions:
        for tx in st.session_state.transactions:
            # Render a custom HTML card for each transaction
            st.markdown(f"""
                <div class="transaction-card debit">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>Paid to {tx['To']}</strong>
                        <strong style="color: #d63031;">- ₹{tx['Amount']:,.2f}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #636e72; font-size: 12px; margin-top: 5px;">
                        <span>{tx['Date']} • {tx['Note']}</span>
                        <span>Txn: {tx['ID']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions found yet. Start sending money!")

# --- 4. PROFILE TAB ---
with tab_profile:
    st.header("My Profile")
    
    col_img, col_info = st.columns([1, 2])
    with col_img:
        # Generate dynamic QR using a free API
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=nmitdev@nmit", caption="Scan to Pay me")
    
    with col_info:
        st.write("### NMIT Developer")
        st.write("**UPI ID:** `nmitdev@nmit`")
        st.write("**Phone:** +91 98765 43210")
        
    st.write("---")
    st.button("⚙️ Settings")
    st.button("❓ Help & Support")
    st.button("🚪 Logout", type="primary")
