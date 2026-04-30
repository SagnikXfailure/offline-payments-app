import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(page_title="NMIT Pay", page_icon="💸", layout="centered", initial_sidebar_state="collapsed")

# ---------- SESSION STATE INIT ----------
if "balance" not in st.session_state:
    st.session_state.balance = 54320.50
if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"Date": datetime.now().strftime("%b %d, %I:%M %p"), "ID": f"T{random.randint(100000000, 999999999)}", "Type": "Credit", "Party": "Welcome Bonus", "Amount": 500.00, "Status": "Success"},
    ]
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "NMIT Hacker",
        "upi_id": "nmithacker@oknmit",
        "phone": "+91 98765 43210",
        "bank": "State Bank of NMIT",
        "account_mask": "XXXX 1234",
    }
if "show_balance" not in st.session_state:
    st.session_state.show_balance = False

# ---------- CUSTOM CSS (THE MOBILE WRAPPER) ----------
st.markdown("""
<style>
    /* Hide default Streamlit top menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clamp the app width to simulate a mobile phone screen */
    .block-container {
        max-width: 420px !important;
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        margin: auto;
        background-color: #f8f9fa;
        min-height: 100vh;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.05);
    }

    /* Google Pay Style Top Banner */
    .gpay-header {
        background: linear-gradient(135deg, #1a73e8, #4285f4);
        padding: 20px;
        border-radius: 20px;
        color: white;
        text-align: left;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(26, 115, 232, 0.3);
    }
    .gpay-header h3 { margin: 0; padding: 0; font-size: 22px; font-weight: 600; color: white; }
    .gpay-header p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; color: white; }
    
    /* Quick Action Buttons Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: auto;
        padding: 10px 5px;
        background-color: white;
        color: #3c4043;
        border: 1px solid #e8eaed;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #f1f3f4;
        border-color: #dadce0;
        color: #1a73e8;
    }

    /* Card Panels */
    .gpay-card {
        background: white;
        border-radius: 16px;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        border: 1px solid #f1f3f4;
    }
    .gpay-card h4 { margin-top: 0; color: #202124; font-size: 16px;}
    
    /* Avatar Grid */
    .avatar-row {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
    }
    .avatar-item {
        text-align: center;
        font-size: 12px;
        color: #3c4043;
    }
    .avatar-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #e8f0fe;
        color: #1a73e8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 5px;
        margin: 0 auto 5px auto;
    }

    /* History List */
    .history-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #f1f3f4;
    }
    .history-row:last-child { border-bottom: none; }
    .h-left { display: flex; flex-direction: column; }
    .h-name { font-weight: 600; color: #202124; font-size: 15px; }
    .h-date { font-size: 12px; color: #5f6368; margin-top: 2px; }
    .h-amt-out { font-weight: 600; font-size: 15px; color: #d93025; }
    .h-amt-in { font-weight: 600; font-size: 15px; color: #1e8e3e; }
    
    /* Input Fields */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
tab_home, tab_pay, tab_history, tab_profile = st.tabs(["🏠 Home", "💸 Pay", "📜 History", "👤 Profile"])

# ==========================================
# 1. HOME TAB (The Visual Dashboard)
# ==========================================
with tab_home:
    profile = st.session_state.profile
    
    # Top Banner
    st.markdown(f"""
    <div class="gpay-header">
        <p>Good evening,</p>
        <h3>{profile['name']}</h3>
        <p style="margin-top:10px;">UPI ID: {profile['upi_id']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Actions Grid
    st.markdown("<b>Explore</b>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("📷\nScan QR")
    with c2: st.button("👤\nContacts")
    with c3: st.button("🏦\nBank Tx")
    with c4: st.button("📱\nSelf Tx")

    # People / Contacts Section
    st.markdown("""
    <div class="gpay-card">
        <h4>People</h4>
        <div class="avatar-row">
            <div class="avatar-item"><div class="avatar-circle">A</div>Alice</div>
            <div class="avatar-item"><div class="avatar-circle">B</div>Bob</div>
            <div class="avatar-item"><div class="avatar-circle" style="background:#fce8e6; color:#d93025;">C</div>Charlie</div>
            <div class="avatar-item"><div class="avatar-circle" style="background:#e6f4ea; color:#1e8e3e;">D</div>Dipa</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Balance Check
    st.markdown('<div class="gpay-card">', unsafe_allow_html=True)
    colA, colB = st.columns([3, 1])
    with colA:
        if st.session_state.show_balance:
            st.markdown(f"<h3 style='margin:0; color:#1a73e8;'>₹{st.session_state.balance:,.2f}</h3>", unsafe_allow_html=True)
            st.caption(f"{profile['bank']} • {profile['account_mask']}")
        else:
            st.markdown("<h3 style='margin:0; color:#5f6368;'>₹ ••••••</h3>", unsafe_allow_html=True)
            st.caption("Tap to view balance")
            
    with colB:
        if st.button("👁️" if not st.session_state.show_balance else "🙈"):
            st.session_state.show_balance = not st.session_state.show_balance
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 2. PAY TAB (Transaction Logic)
# ==========================================
with tab_pay:
    st.markdown("### Secure Payment")
    st.caption("Powered by UPI")
    
    with st.container():
        upi_id = st.text_input("Receiver UPI ID or Phone", placeholder="e.g. name@bank")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=50.0, format="%.2f")
        note = st.text_input("What's this for?", placeholder="Add a note")
        pin = st.text_input("4-Digit UPI PIN", type="password", max_chars=4, placeholder="****")

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ Confirm Payment", use_container_width=True, type="primary"):
            if not upi_id:
                st.error("Enter a valid receiver.")
            elif amount > st.session_state.balance:
                st.error("Insufficient balance in your linked bank account.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("Invalid UPI PIN.")
            else:
                # Process Transaction
                st.session_state.balance -= amount
                tx_id = f"T{random.randint(100000000, 999999999)}"
                new_tx = {
                    "Date": datetime.now().strftime("%b %d, %I:%M %p"),
                    "ID": tx_id,
                    "Type": "Debit",
                    "Party": upi_id,
                    "Amount": amount,
                    "Status": "Success",
                    "Note": note
                }
                st.session_state.transactions.insert(0, new_tx)
                st.success(f"Payment of ₹{amount:,.2f} successful!")
                st.balloons()


# ==========================================
# 3. HISTORY TAB (Transaction Log)
# ==========================================
with tab_history:
    st.markdown("### Recent Activity")
    
    if st.session_state.transactions:
        html_content = '<div class="gpay-card">'
        for tx in st.session_state.transactions:
            amt_class = "h-amt-out" if tx["Type"] == "Debit" else "h-amt-in"
            amt_prefix = "-" if tx["Type"] == "Debit" else "+"
            
            html_content += f"""
            <div class="history-row">
                <div class="h-left">
                    <span class="h-name">{tx['Party']}</span>
                    <span class="h-date">{tx['Date']} • {tx.get('Note', 'UPI Transfer')}</span>
                </div>
                <div class="{amt_class}">{amt_prefix}₹{tx['Amount']:,.2f}</div>
            </div>
            """
        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.info("No recent transactions.")


# ==========================================
# 4. PROFILE TAB (Account Details)
# ==========================================
with tab_profile:
    p = st.session_state.profile
    st.markdown(f"""
    <div class="gpay-card" style="text-align: center;">
        <div style="width: 80px; height: 80px; background-color: #1a73e8; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; margin: 0 auto 15px auto;">
            {p['name'][0]}
        </div>
        <h3 style="margin:0; color:#202124;">{p['name']}</h3>
        <p style="color:#5f6368; margin-top:5px;">{p['phone']}</p>
        <p style="color:#1a73e8; font-weight:500;">{p['upi_id']}</p>
    </div>
    
    <div class="gpay-card">
        <h4 style="margin-bottom: 10px;">Payment Methods</h4>
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f3f4; padding-bottom:10px;">
            <div>
                <b>{p['bank']}</b><br>
                <span style="color:#5f6368; font-size:14px;">Primary • {p['account_mask']}</span>
            </div>
            <span style="color:#1e8e3e; font-weight:bold;">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛡️ Privacy & Security", use_container_width=True):
        st.toast("Security settings clicked!")
    if st.button("🚪 Logout", use_container_width=True):
        st.warning("Logout triggered.")
