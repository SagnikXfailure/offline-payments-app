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

if "action" not in st.session_state:
    st.session_state.action = None

# ---------- CSS ----------
st.markdown("""
<style>
body {background:#0b1220;font-family:Inter;}
#MainMenu, footer, header {visibility:hidden;}

.block-container {max-width:1200px;padding:20px;margin:auto;}

.header {
    background: linear-gradient(135deg,#1a73e8,#4285f4);
    padding:25px;border-radius:20px;color:white;
}

.balance {
    background:white;padding:22px;border-radius:16px;
    color:#202124;
}

.balance h2 {color:#1a73e8;}

.grid {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:20px;margin-top:20px;text-align:center;
}

/* BUTTONS styled as tiles */
.stButton button {
    background: transparent;
    border: none;
    color: white;
    font-size: 14px;
    padding: 10px;
    cursor: pointer;
}

/* icon block */
.stButton button::first-line {
    display: block;
    font-size: 24px;
    background: #e8f0fe;
    color: black;
    border-radius: 16px;
    width: 55px;
    height: 55px;
    line-height: 55px;
    margin: auto;
    margin-bottom: 6px;
}

.card {
    background:white;padding:16px;border-radius:14px;
    margin-top:12px;color:#202124;
}

.title {font-weight:600;}
.subtitle {font-size:12px;color:#5f6368;}
.amount {float:right;color:#ea4335;}
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

        c1, c2, c3, c4, c5 = st.columns(5)

        def action_btn(col, icon, label, key, action):
            with col:
                if st.button(f"{icon}\n{label}", key=key):
                    st.session_state.action = action

        action_btn(c1, "📷", "Scan QR", "scan", "scan")
        action_btn(c2, "👤", "Pay Anyone", "pay", "pay")
        action_btn(c3, "🏦", "Bank Transfer", "bank", "bank")
        action_btn(c4, "⚡", "Recharge", "recharge", "recharge")
        action_btn(c5, "🧾", "Pay Bills", "bills", "bills")

        # ---------- ACTION RESPONSE ----------
        if st.session_state.action:
            st.markdown("### ⚡ Action")

            if st.session_state.action == "scan":
                st.info("📷 QR Scanner coming soon")

            elif st.session_state.action == "pay":
                st.info("👤 Go to Pay tab to send money")

            elif st.session_state.action == "bank":
                st.info("🏦 Bank Transfer coming soon")

            elif st.session_state.action == "recharge":
                st.info("⚡ Recharge coming soon")

            elif st.session_state.action == "bills":
                st.info("🧾 Bill payment coming soon")

        # ---------- RECENT ----------
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

    if st.button("Pay Now"):

        if not upi:
            st.error("Enter UPI ID")
        elif amt > st.session_state.balance:
            st.error("Insufficient balance")
        else:
            st.session_state.balance -= amt
            txid = f"T{random.randint(100000,999999)}"

            st.session_state.transactions.insert(0,{
                "to": upi,
                "amt": amt,
                "date": datetime.now().strftime("%d %b %I:%M %p"),
                "id": txid
            })

            st.success(f"Paid ₹{amt} to {upi}")

# ---------- HISTORY ----------
with history:

    st.subheader("All Transactions")

    for tx in st.session_state.transactions:
        st.markdown(f"""
        <div class="card">
            <span class="title">{tx['to']}</span>
            <span class="amount">₹{tx['amt']:,.2f}</span>
            <div class="subtitle">{tx['date']} • {tx['id']}</div>
        </div>
        """, unsafe_allow_html=True)

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
