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

# ---------- VALIDATION ----------
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

.card {
    background:white;padding:16px;border-radius:14px;margin-top:12px;color:#202124;
}

.popup {
    background:white;
    padding:20px;
    border-radius:16px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home","💸 Pay","📊 History","👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2.2,1])

    with col1:
        st.markdown(f"""
        <div class="header">
            <h3>Hello, {st.session_state.profile['name']}</h3>
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

        # ---------- POPUP ----------
        if st.session_state.popup:

            st.markdown("<div class='popup'>", unsafe_allow_html=True)

            if st.button("❌ Close"):
                st.session_state.popup = None
                st.rerun()

            # ---------- FIXED SCANNER ----------
            if st.session_state.popup == "scan":

                st.subheader("QR Scanner")

                components.html("""
                <div style="position:relative;width:100%;height:420px;background:black;border-radius:16px;overflow:hidden;">
                    
                    <div id="reader" style="width:100%;height:100%;"></div>

                    <div style="
                        position:absolute;
                        top:50%;
                        left:50%;
                        transform:translate(-50%,-50%);
                        width:240px;
                        height:240px;
                        border:2px solid #00ffcc;
                        border-radius:16px;
                    ">
                        <div style="
                            position:absolute;
                            width:100%;
                            height:2px;
                            background:#00ffcc;
                            animation:scan 2s linear infinite;
                        "></div>
                    </div>

                </div>

                <script src="https://unpkg.com/html5-qrcode"></script>

                <script>
                function send(data){
                    const ta = window.parent.document.querySelector("textarea");
                    if(ta){
                        ta.value = data;
                        ta.dispatchEvent(new Event("input",{bubbles:true}));
                    }
                }

                const qr = new Html5Qrcode("reader");

                Html5Qrcode.getCameras().then(devices => {
                    if(devices.length){
                        qr.start(
                            devices[0].id,
                            { fps: 10, qrbox: 240 },
                            (decodedText)=>{
                                send(decodedText);
                                qr.stop();
                            }
                        );
                    }
                });

                const style = document.createElement("style");
                style.innerHTML = `
                @keyframes scan {
                    0% { top:0 }
                    100% { top:100% }
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
                        st.warning("⚠️ Suspicious QR")
                    else:
                        st.error("❌ Invalid QR")

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

            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="balance">
            <h2>₹{st.session_state.balance:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
