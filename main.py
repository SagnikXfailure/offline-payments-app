import streamlit as st
from datetime import datetime
import random
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="PayFlow", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Sagnik",
        "upi": "Sagnik@oksbi",
        "bank": "SBI Bank",
        "mask": "XXXX 1234"
    }

if "popup" not in st.session_state:
    st.session_state.popup = None

if "qr_result" not in st.session_state:
    st.session_state.qr_result = ""

# ---------- QR VALIDATION ----------
def validate_qr(data):
    if not data:
        return "invalid"
    if data.startswith("upi://"):
        return "upi"
    if data.startswith("http"):
        return "suspicious"
    return "invalid"

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
    background:white;padding:22px;border-radius:16px;color:#202124;
}

.balance h2 {color:#1a73e8;}

.card {
    background:white;padding:16px;border-radius:14px;margin-top:12px;color:#202124;
}

.popup {
    background:white;
    padding:20px;
    border-radius:16px;
    margin-top:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home", "💸 Pay", "📊 History", "👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2.2, 1])

    with col1:
        st.markdown(f"""
        <div class="header">
            <h3>Hello, {st.session_state.profile['name']}</h3>
            <p>Welcome back</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💸 Quick Actions")

        c1, c2, c3, c4, c5 = st.columns(5)

        if c1.button("📷\nScan QR"):
            st.session_state.popup = "scan"

        if c2.button("👤\nPay Anyone"):
            st.session_state.popup = "pay"

        if c3.button("🏦\nBank Transfer"):
            st.session_state.popup = "bank"

        if c4.button("⚡\nRecharge"):
            st.session_state.popup = "recharge"

        if c5.button("🧾\nPay Bills"):
            st.session_state.popup = "bills"

        # ---------- POPUPS ----------
        if st.session_state.popup:

            st.markdown('<div class="popup">', unsafe_allow_html=True)

            if st.button("❌ Close"):
                st.session_state.popup = None
                st.rerun()

            # ---------- SCANNER ----------
            if st.session_state.popup == "scan":

                st.subheader("QR Scanner")

                components.html("""
                <div style="position:relative; width:100%;">

                    <div id="reader" style="width:100%;"></div>

                    <div style="
                        position:absolute;
                        top:0;
                        left:0;
                        width:100%;
                        height:2px;
                        background:#00ffcc;
                        animation:scan 2s infinite;
                    "></div>

                </div>

                <script src="https://unpkg.com/html5-qrcode"></script>

                <script>
                function sendToStreamlit(data){
                    const textarea = window.parent.document.querySelector('textarea');
                    if(textarea){
                        textarea.value = data;
                        textarea.dispatchEvent(new Event('input',{bubbles:true}));
                    }
                }

                function onScanSuccess(decodedText) {
                    sendToStreamlit(decodedText);
                    scanner.clear();
                }

                let scanner = new Html5QrcodeScanner(
                    "reader",
                    { fps: 10, qrbox: 250 },
                    false
                );

                scanner.render(onScanSuccess);

                const style = document.createElement('style');
                style.innerHTML = `
                @keyframes scan {
                    0% { top:0; }
                    100% { top:100%; }
                }`;
                document.head.appendChild(style);

                </script>
                """, height=420)

                qr_data = st.text_area("QR Result")

                if qr_data:

                    st.session_state.qr_result = qr_data
                    result = validate_qr(qr_data)

                    if result == "upi":
                        st.success("✅ UPI QR Detected")
                    elif result == "suspicious":
                        st.warning("⚠️ Suspicious QR (URL detected)")
                    else:
                        st.error("❌ Invalid QR")

                    # Auto close + redirect
                    st.session_state.popup = "pay"
                    st.rerun()

            # ---------- PAY ----------
            elif st.session_state.popup == "pay":

                st.subheader("Pay Anyone")

                upi = st.text_input("UPI ID", value=st.session_state.qr_result)
                amt = st.number_input("Amount ₹", min_value=1.0)

                if st.button("Send"):

                    if amt > st.session_state.balance:
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

                        st.success("Payment Successful")

            # ---------- RECHARGE ----------
            elif st.session_state.popup == "recharge":

                st.subheader("Recharge")

                num = st.text_input("Mobile")
                amt = st.number_input("Amount", min_value=10.0)

                if st.button("Recharge"):

                    if amt > st.session_state.balance:
                        st.error("Insufficient balance")
                    else:
                        st.session_state.balance -= amt
                        st.success("Recharge Done")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- RECENT ----------
        st.markdown("### 📊 Recent Activity")

        for tx in st.session_state.transactions[:5]:
            st.markdown(f"""
            <div class="card">
                <b>{tx['to']}</b>
                <span style="float:right;color:red;">₹{tx['amt']:,.2f}</span>
                <div style="font-size:12px;color:gray;">{tx['date']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="balance">
            <div>Available Balance</div>
            <h2>₹{st.session_state.balance:,.2f}</h2>
            <small>{st.session_state.profile['bank']} • {st.session_state.profile['mask']}</small>
        </div>
        """, unsafe_allow_html=True)

# ---------- HISTORY ----------
with history:
    st.subheader("All Transactions")

    for tx in st.session_state.transactions:
        st.markdown(f"""
        <div class="card">
            <b>{tx['to']}</b>
            <span style="float:right;color:red;">₹{tx['amt']:,.2f}</span>
            <div style="font-size:12px;color:gray;">
                {tx['date']} • {tx['id']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- PROFILE ----------
with profile:
    p = st.session_state.profile

    st.markdown(f"""
    <div class="card">
        <h3>{p['name']}</h3>
        <p>{p['upi']}</p>
        <p>{p['bank']} • {p['mask']}</p>
    </div>
    """, unsafe_allow_html=True)
