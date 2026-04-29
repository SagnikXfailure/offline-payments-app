import streamlit as st
from datetime import datetime
import random
import time

# ---------- PAGE CONFIG ----------
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

# ---------- CSS (FULL FIX) ----------
st.markdown("""
<style>

body {background:#0b1220;font-family:Inter;}
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
    padding:22px;
    border-radius:16px;
    box-shadow:0 6px 18px rgba(0,0,0,0.1);
    color:#202124;
}

.balance h2 {
    color:#1a73e8;
    margin:10px 0;
}

.balance small {
    color:#5f6368;
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

/* CARD FIX (IMPORTANT) */
.card {
    background:white;
    padding:16px;
    border-radius:14px;
    margin-top:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
    color:#202124;
}

/* TEXT FIX */
.title {
    font-weight:600;
    color:#202124;
}

.subtitle {
    font-size:12px;
    color:#5f6368;
}

.amount {
    float:right;
    color:#ea4335;
    font-weight:600;
}

/* SUCCESS */
.success {
    text-align:center;
    background:white;
    padding:25px;
    border-radius:16px;
    color:#202124;
}

/* BUTTON */
.stButton button {
    height:50px;
    border-radius:12px;
    background:#1a73e8;
}

/* RESPONSIVE */
@media (max-width: 900px) {
    .grid {grid-template-columns: repeat(3,1fr);}
}

@media (max-width: 600px) {
    .grid {grid-template-columns: repeat(2,1fr);}
}

</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home", "💸 Pay", "📊 History", "👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2.2, 1], gap="large")

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

        st.markdown("### 📊 Recent Activity")

        if st.session_state.transactions:
            for tx in st.session_state.transactions[:5]:
                st.markdown(f"""
                <div class="card">
                    <span class="title">{tx['to']}</span>
                    <span class="amount">-₹{tx['amt']:,.2f}</span>
                    <div class="subtitle">{tx['date']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent transactions yet.")

    with col2:
        st.markdown(f"""
        <div class="balance">
            <div class="subtitle">Available Balance</div>
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
                <span class="title">{tx['to']}</span>
                <span class="amount">₹{tx['amt']:,.2f}</span>
                <div class="subtitle">{tx['date']} • {tx['id']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet.")

# ---------- PROFILE ----------
with profile:

    p = st.session_state.profile

    st.markdown(f"""
    <div class="card">
        <h3 class="title">{p['name']}</h3>
        <p class="subtitle">{p['upi']}</p>
        <p class="subtitle">{p['bank']} • {p['mask']}</p>
    </div>
    """, unsafe_allow_html=True)
