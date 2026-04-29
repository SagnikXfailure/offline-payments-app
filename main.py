# SOURCE: Your original code upgraded for UI/UX perfection :contentReference[oaicite:0]{index=0}

import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
import base64

st.set_page_config(page_title="GPay Clone", page_icon="💳", layout="centered")

# ---------- SESSION ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Abhishek",
        "upi_id": "abhi.document-2@okicici",
        "phone": "+91 98765 43210",
        "bank": "ICICI Bank",
        "account_mask": "XXXX 1234",
    }

# ---------- MODERN CSS ----------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 420px;
    padding: 0.5rem 1rem;
}

.stApp {
    background: #f4f7fb;
}

#MainMenu, footer, header {visibility: hidden;}

/* HEADER */
.header {
    background: linear-gradient(180deg,#e8f0fe,#ffffff);
    padding: 18px;
    border-radius: 0 0 25px 25px;
    margin: -1rem -1rem 1rem -1rem;
}

/* SEARCH */
.search {
    background: white;
    padding: 12px 15px;
    border-radius: 30px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-top: 12px;
}

/* GRID */
.grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 16px;
    text-align: center;
}

.grid div {
    font-size: 12px;
    color: #444;
    cursor: pointer;
    transition: 0.2s;
}

.grid div:hover {
    transform: translateY(-4px);
}

/* ICON BOX */
.icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #e8f0fe;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:auto;
    margin-bottom:6px;
}

/* CARD */
.card {
    background:white;
    padding:16px;
    border-radius:14px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
    margin-bottom:10px;
}

/* SUCCESS */
.success-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align:center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

.amount {
    font-size:28px;
    font-weight:600;
    color:#1a73e8;
}

/* BUTTON */
.stButton button {
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
    background: #1a73e8;
}

</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "💸 Pay", "📜 History", "👤 Profile"])

# ---------- HOME ----------
with tab1:

    st.markdown("""
    <div class="header">
        <div style="font-size:13px;">10:08 📶 🔋</div>

        <div class="search">🔍 Pay friends & merchants</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="grid">
        <div><div class="icon">📱</div>Scan</div>
        <div><div class="icon">👤</div>Contact</div>
        <div><div class="icon">📲</div>Phone</div>
        <div><div class="icon">🏦</div>Bank</div>
        <div><div class="icon">@</div>UPI ID</div>
        <div><div class="icon">🔄</div>Self</div>
        <div><div class="icon">🧾</div>Bills</div>
        <div><div class="icon">⚡</div>Recharge</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- PAY ----------
with tab2:

    st.subheader("Send Money")

    upi = st.text_input("UPI ID / Phone")
    amt = st.number_input("Amount ₹", min_value=1.0, step=10.0)
    note = st.text_input("Note")

    if st.button("Pay Now", use_container_width=True):

        if not upi:
            st.error("Enter UPI ID")
        elif amt > st.session_state.balance:
            st.error("Insufficient balance")
        else:
            with st.spinner("Processing..."):
                time.sleep(1.2)

            st.session_state.balance -= amt
            txid = f"T{random.randint(100000,999999)}"

            st.session_state.transactions.insert(0,{
                "to": upi,
                "amt": amt,
                "date": datetime.now().strftime("%d %b %I:%M %p"),
                "id": txid
            })

            st.markdown(f"""
            <div class="success-card">
                <div class="amount">₹{amt:,.2f}</div>
                <p>Paid to {upi}</p>
                <p style="font-size:12px;color:gray;">TXN ID: {txid}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- HISTORY ----------
with tab3:

    st.subheader("Transactions")
    st.write(f"Balance: ₹{st.session_state.balance:,.2f}")

    for tx in st.session_state.transactions:
        st.markdown(f"""
        <div class="card">
            <b>{tx['to']}</b>
            <div style="float:right;color:red;">-₹{tx['amt']:,.2f}</div>
            <div style="font-size:12px;color:gray;">
                {tx['date']} • {tx['id']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- PROFILE ----------
with tab4:

    p = st.session_state.profile

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h3>{p['bank']}</h3>
        <p>{p['account_mask']}</p>
        <div class="amount">₹{st.session_state.balance:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write(f"Name: {p['name']}")
    st.write(f"UPI: {p['upi_id']}")
    st.write(f"Phone: {p['phone']}")
