import streamlit as st
from datetime import datetime
import random
import time

# ---------- PAGE CONFIG (FIXED) ----------
st.set_page_config(page_title="PayFlow", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Abhishek",
        "upi": "abhi@okicici",
        "bank": "ICICI Bank",
        "mask": "XXXX 1234"
    }

# ---------- RESPONSIVE CSS ----------
st.markdown("""
<style>

body {background:#f5f7fb;font-family:Inter;}
#MainMenu, footer, header {visibility:hidden;}

.block-container {
    max-width: 1200px;
    padding: 20px;
    margin: auto;
}

/* HEADER */
.header {
    background: linear-gradient(135deg,#1a73e8,#4285f4);
    padding:25px;
    border-radius:20px;
    color:white;
}

/* BALANCE CARD */
.balance {
    background:white;
    padding:20px;
    border-radius:16px;
    margin-top:-40px;
    box-shadow:0 6px 18px rgba(0,0,0,0.1);
}

/* GRID */
.grid {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:20px;
    margin-top:20px;
    text-align:center;
}

.icon {
    width:55px;height:55px;
    border-radius:16px;
    background:#e8f0fe;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:auto;
}

/* CARD */
.card {
    background:white;
    padding:16px;
    border-radius:14px;
    margin-top:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
}

/* SUCCESS */
.success {
    text-align:center;
    background:white;
    padding:25px;
    border-radius:16px;
    box-shadow:0 6px 18px rgba(0,0,0,0.1);
}

/* BUTTON */
.stButton button {
    height:50px;
    border-radius:12px;
    background:#1a73e8;
}

/* -------- RESPONSIVE -------- */

/* Tablet */
@media (max-width: 900px) {
    .grid {
        grid-template-columns: repeat(3,1fr);
    }
}

/* Mobile */
@media (max-width: 600px) {
    .grid {
        grid-template-columns: repeat(2,1fr);
    }

    .header {
        padding:18px;
        border-radius:0 0 20px 20px;
    }

    .balance {
        margin-top:-30px;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home", "💸 Pay", "📊 History", "👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown(f"""
        <div class="header">
            <h3>Hello, {st.session_state.profile['name']}</h3>
            <p>Welcome back</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💸 Quick Actions")
        st.markdown("""
        <div class="grid">
            <div><div class="icon">📷</div>Scan QR</div>
            <div><div class="icon">👤</div>Pay Anyone</div>
            <div><div class="icon">🏦</div>Bank Transfer</div>
            <div><div class="icon">⚡</div>Recharge</div>
            <div><div class="icon">🧾</div>Pay Bills</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🧩 Services")
        st.markdown("""
        <div class="grid">
            <div><div class="icon">🏬</div>Businesses</div>
            <div><div class="icon">🎁</div>Offers</div>
            <div><div class="icon">📊</div>Money</div>
            <div><div class="icon">🏦</div>Balance</div>
            <div><div class="icon">📜</div>History</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Recent Activity")

        if st.session_state.transactions:
            for tx in st.session_state.transactions[:5]:
                st.markdown(f"""
                <div class="card">
                    <b>{tx['to']}</b>
                    <div style="float:right;color:red;">-₹{tx['amt']:,.2f}</div>
                    <div style="font-size:12px;color:gray;">{tx['date']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent transactions yet.")

    with col2:
        st.markdown(f"""
        <div class="balance">
            <div>Available Balance</div>
            <h2>₹{st.session_state.balance:,.2f}</h2>
            <small>{st.session_state.profile['bank']} • {st.session_state.profile['mask']}</small>
        </div>
        """, unsafe_allow_html=True)

# ---------- PAY ----------
with pay:

    st.subheader("Send Money")

    upi = st.text_input("UPI ID / Phone")
    amt = st.number_input("Amount ₹", min_value=1.0)
    note = st.text_input("Note")

    if st.button("Pay Now", use_container_width=True):

        if not upi:
            st.error("Enter UPI ID")
        elif amt > st.session_state.balance:
            st.error("Insufficient balance")
        else:
            with st.spinner("Processing..."):
                time.sleep(1)

            st.session_state.balance -= amt
            txid = f"T{random.randint(100000,999999)}"

            st.session_state.transactions.insert(0,{
                "to": upi,
                "amt": amt,
                "date": datetime.now().strftime("%d %b %I:%M %p"),
                "id": txid
            })

            st.markdown(f"""
            <div class="success">
                <h2>₹{amt:,.2f}</h2>
                <p>Paid to {upi}</p>
                <small>Txn ID: {txid}</small>
            </div>
            """, unsafe_allow_html=True)

# ---------- HISTORY ----------
with history:

    st.subheader("All Transactions")

    if st.session_state.transactions:
        for tx in st.session_state.transactions:
            st.markdown(f"""
            <div class="card">
                {tx['to']}
                <div style="float:right;color:red;">₹{tx['amt']:,.2f}</div>
                <div style="font-size:12px;color:gray;">
                    {tx['date']} • {tx['id']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet.")

# ---------- PROFILE ----------
with profile:

    p = st.session_state.profile

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h3>{p['name']}</h3>
        <p>{p['upi']}</p>
        <p>{p['bank']} • {p['mask']}</p>
    </div>
    """, unsafe_allow_html=True)
