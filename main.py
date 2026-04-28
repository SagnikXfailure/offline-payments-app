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
        dis
