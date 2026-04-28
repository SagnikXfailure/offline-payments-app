import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
import re

st.set_page_config(page_title="NMIT Pay", page_icon="💸", layout="centered")

# ---------- SESSION STATE ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.00

if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {
            "Date": datetime.now().strftime("%b %d, %Y %I:%M %p"),
            "ID": f"T{random.randint(1000000000, 9999999999)}",
            "Type": "Credit",
            "Party": "Welcome Bonus",
            "Note": "Cashback Reward",
            "Amount": 500.00,
            "Status": "Success",
        }
    ]

if "show_balance" not in st.session_state:
    st.session_state.show_balance = False

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "NMIT Developer",
        "upi_id": "nmitdev@nmit",
        "phone": "+91 98765 43210",
        "bank": "State Bank of NMIT",
        "account_mask": "XXXX 1234",
    }

if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

if "favorites" not in st.session_state:
    st.session_state.favorites = ["satoshi@nmit", "alice@ybl", "9876543210"]

# ---------- HELPERS ----------
def validate_upi(value: str) -> bool:
    if not value:
        return False
    upi_pattern = r"^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$"
    phone_pattern = r"^\d{10}$"
    return bool(re.match(upi_pattern, value) or re.match(phone_pattern, value))

def create_txn_id():
    return f"T{random.randint(1000000000, 9999999999)}"

def add_transaction(tx_type, party, note, amount, status="Success"):
    txn = {
        "Date": datetime.now().strftime("%b %d, %Y %I:%M %p"),
        "ID": create_txn_id(),
        "Type": tx_type,
        "Party": party,
        "Note": note,
        "Amount": amount,
        "Status": status,
    }
    st.session_state.transactions.insert(0, txn)
    return txn

def get_total_spends():
    return sum(
        tx["Amount"]
        for tx in st.session_state.transactions
        if tx["Type"] == "Debit" and tx["Status"] == "Success"
    )

def get_total_cashback():
    return 450

# ---------- STYLING ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f7f9fc 0%, #eef2f7 100%);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .title-block {
        padding: 0.25rem 0 1rem 0;
    }

    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.22);
        margin-bottom: 18px;
    }

    .glass-card {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
        margin-bottom: 16px;
    }

    .txn-credit, .txn-debit {
        padding: 14px 16px;
        border-radius: 16px;
        margin-bottom: 10px;
        background: white;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    }

    .txn-credit {
        border-left: 5px solid #16a34a;
    }

    .txn-debit {
        border-left: 5px solid #dc2626;
    }

    .small-muted {
        color: #64748b;
        font-size: 0.9rem;
    }

    .success-pill, .danger-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
    }

    .success-pill {
        background: #dcfce7;
        color: #166534;
    }

    .danger-pill {
        background: #fee2e2;
        color: #991b1b;
    }

    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 3.1em;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        font-weight: 600;
        transition: 0.25s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(99, 102, 241, 0.35);
        color: white;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 4px;
    }

    .receipt-box {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 16px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title-block">', unsafe_allow_html=True)
st.title("💸 NMIT Pay")
st.caption("Fast, secure, student-friendly digital payments")
st.markdown("</div>", unsafe_allow_html=True)

tab_home, tab_pay, tab_history, tab_profile = st.tabs(
    ["🏠 Home", "💸 Pay", "📜 History", "👤 Profile"]
)

# ---------- HOME ----------
with tab_home:
    profile = st.session_state.profile
    balance_display = (
        f"₹{st.session_state.balance:,.2f}"
        if st.session_state.show_balance
        else "₹ ••••••"
    )

    st.markdown(f"""
    <div class="hero-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:14px; opacity:0.8;">Welcome back</div>
                <div style="font-size:28px; font-weight:700;">{profile['name']} 👋</div>
            </div>
            <div style="font-size:13px; opacity:0.85; text-align:right;">
                <div>{profile['bank']}</div>
                <div>{profile['account_mask']}</div>
            </div>
        </div>
        <div style="margin-top:22px; font-size:14px; opacity:0.82;">Available Balance</div>
        <div style="font-size:34px; font-weight:800; margin-top:6px;">{balance_display}</div>
        <div style="margin-top:8px; font-size:13px; opacity:0.75;">UPI ID: {profile['upi_id']}</div>
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        if st.button("👁 Toggle Balance"):
            st.session_state.show_balance = not st.session_state.show_balance
            st.rerun()
    with colB:
        st.button("🔒 Security Shield")

    st.markdown("### Insights")
    c1, c2, c3 = st.columns(3)
    c1.metric("Cashback", f"₹{get_total_cashback():,.0f}", "+₹12")
    c2.metric("Transactions", len(st.session_state.transactions))
    c3.metric("Spent", f"₹{get_total_spends():,.0f}")

    st.markdown("### Quick Pay")
    fav_cols = st.columns(len(st.session_state.favorites))
    for i, fav in enumerate(st.session_state.favorites):
        fav_cols[i].button(f"Pay\n{fav}", key=f"fav_{i}")

# ---------- PAY ----------
with tab_pay:
    st.subheader("Send Money")
    st.caption("Protected with UPI PIN verification")

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        upi_id = st.text_input(
            "Receiver UPI ID or 10-digit phone number",
            placeholder="e.g. satoshi@nmit or 9876543210"
        )
        amount = st.number_input(
            "Amount (₹)",
            min_value=1.0,
            step=50.0,
            format="%.2f"
        )
        note = st.text_input(
            "Add note",
            placeholder="Mess bill, rent, snacks..."
        )
        pin = st.text_input(
            "Enter 4-digit UPI PIN",
            type="password",
            max_chars=4,
            placeholder="****"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if amount:
            st.info(f"You are about to pay ₹{amount:,.2f}")

        if st.button("✅ Secure Pay"):
            if not validate_upi(upi_id):
                st.error("Enter a valid UPI ID or 10-digit phone number.")
            elif amount <= 0:
                st.error("Amount must be greater than ₹0.")
            elif amount > st.session_state.balance:
                st.error("Insufficient balance for this transaction.")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("Enter a valid 4-digit UPI PIN.")
            else:
                with st.spinner("Authenticating securely..."):
                    time.sleep(1)

                with st.spinner("Processing payment..."):
                    time.sleep(1.2)

                st.session_state.balance -= amount
                txn = add_transaction(
                    tx_type="Debit",
                    party=upi_id,
                    note=note if note else "UPI Payment",
                    amount=amount,
                    status="Success",
                )
                st.session_state.last_receipt = txn

                st.success(f"₹{amount:,.2f} sent successfully to {upi_id}")
                st.balloons()

    if st.session_state.last_receipt:
        tx = st.session_state.last_receipt
        st.markdown("### Last Receipt")
        st.markdown(f"""
        <div class="receipt-box">
            <p><strong>Transaction ID:</strong> {tx['ID']}</p>
            <p><strong>Paid To:</strong> {tx['Party']}</p>
            <p><strong>Amount:</strong> ₹{tx['Amount']:,.2f}</p>
            <p><strong>Date:</strong> {tx['Date']}</p>
            <p><strong>Note:</strong> {tx['Note']}</p>
            <p><strong>Status:</strong> Success ✅</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- HISTORY ----------
with tab_history:
    st.subheader("Transaction History")

    if st.session_state.transactions:
        txn_type_filter = st.selectbox("Filter", ["All", "Debit", "Credit"])

        filtered = st.session_state.transactions
        if txn_type_filter != "All":
            filtered = [tx for tx in filtered if tx["Type"] == txn_type_filter]

        for tx in filtered:
            klass = "txn-debit" if tx["Type"] == "Debit" else "txn-credit"
            amount_prefix = "-" if tx["Type"] == "Debit" else "+"
            amount_color = "#dc2626" if tx["Type"] == "Debit" else "#16a34a"
            status_class = "success-pill" if tx["Status"] == "Success" else "danger-pill"

            st.markdown(f"""
            <div class="{klass}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700;">{tx['Type']} • {tx['Party']}</div>
                        <div class="small-muted">{tx['Date']} • {tx['Note']}</div>
                        <div class="{status_class}" style="margin-top:8px;">{tx['Status']}</div>
                    </div>
                    <div style="font-weight:800; color:{amount_color};">
                        {amount_prefix} ₹{tx['Amount']:,.2f}
                    </div>
                </div>
                <div class="small-muted" style="margin-top:10px;">Txn ID: {tx['ID']}</div>
            </div>
            """, unsafe_allow_html=True)

        df = pd.DataFrame(st.session_state.transactions)
        with st.expander("View structured data"):
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No transactions yet. Your recent payments will appear here.")

# ---------- PROFILE ----------
with tab_profile:
    profile = st.session_state.profile

    left, right = st.columns([1, 2])

    with left:
        st.image(
            f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={profile['upi_id']}",
            caption="Scan to pay"
        )

    with right:
        st.markdown(f"### {profile['name']}")
        st.write(f"**UPI ID:** `{profile['upi_id']}`")
        st.write(f"**Phone:** {profile['phone']}")
        st.write(f"**Bank:** {profile['bank']}")
        st.write(f"**A/C:** {profile['account_mask']}")

    st.write("---")
    st.button("⚙️ Settings")
    st.button("🛡 Privacy & Security")
    st.button("❓ Help & Support")
    st.button("🚪 Logout", type="primary")
