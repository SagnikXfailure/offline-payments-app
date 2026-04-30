import streamlit as st
from datetime import datetime
import random
import streamlit.components.v1 as components

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="PayFlow Dashboard", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

# ---------- SESSION INITIALIZATION ----------
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

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Defaults */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Dashboard Cards & Layout */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .dashboard-header h2 { margin: 0; font-weight: 700; color: white;}
    .dashboard-header p { margin: 5px 0 0 0; color: #94a3b8; font-size: 1.1rem;}

    .balance-card {
        background: white;
        padding: 30px;
        border-radius: 16px;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    .balance-card h4 { margin: 0; color: #64748b; font-size: 1rem; font-weight: 500;}
    .balance-card h1 { color: #0f172a; font-size: 2.5rem; margin: 10px 0;}
    .balance-card .bank-info { color: #10b981; font-weight: 600; background: #d1fae5; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;}

    .action-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    /* Transaction Items */
    .txn-item {
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #f1f5f9;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .txn-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-color: #e2e8f0;
    }
    .txn-left { display: flex; flex-direction: column; }
    .txn-title { font-weight: 600; color: #0f172a; font-size: 1.05rem; }
    .txn-date { font-size: 0.85rem; color: #64748b; margin-top: 4px; }
    .txn-amount { font-weight: 700; color: #ef4444; font-size: 1.1rem; }
    .txn-amount.credit { color: #10b981; }

    /* Popups / Modals */
    .popup-container {
        background: #ffffff;
        padding: 25px;
        border-radius: 16px;
        margin-top: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------- NAVIGATION (SIDEBAR) ----------
with st.sidebar:
    st.markdown("<h2>💳 PayFlow</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: 0; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    nav_selection = st.radio(
        "Menu",
        ["🏠 Dashboard", "💸 Send Money", "📊 Transaction History", "👤 My Profile"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Secure Portal • V 2.1.0")

# ==========================================
# 1. DASHBOARD (HOME)
# ==========================================
if nav_selection == "🏠 Dashboard":

    col1, col2 = st.columns([2.5, 1.2])

    with col1:
        # Header Greeting
        st.markdown(f"""
        <div class="dashboard-header">
            <h2>Welcome back, {st.session_state.profile['name']}</h2>
            <p>Here is what's happening with your account today.</p>
        </div>
        """, unsafe_allow_html=True)

        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        c1, c2, c3, c4, c5 = st.columns(5)

        if c1.button("📷\nScan", use_container_width=True):
            st.session_state.popup = "scan"
        if c2.button("👤\nPay", use_container_width=True):
            st.session_state.popup = "pay"
        if c3.button("🏦\nBank", use_container_width=True):
            st.session_state.popup = "bank"
        if c4.button("📱\nRecharge", use_container_width=True):
            st.session_state.popup = "recharge"
        if c5.button("🧾\nBills", use_container_width=True):
            st.session_state.popup = "bills"

        # ---------- DYNAMIC INLINE POPUPS ----------
        if st.session_state.popup:
            st.markdown('<div class="popup-container">', unsafe_allow_html=True)
            
            close_col, title_col = st.columns([1, 10])
            with close_col:
                if st.button("✖", key="close_popup"):
                    st.session_state.popup = None
                    st.rerun()

            # SCANNER POPUP
            if st.session_state.popup == "scan":
                st.subheader("Scan QR Code")
                components.html("""
                <div style="position:relative; width:100%; max-width: 400px; margin: auto;">
                    <div id="reader" style="width:100%; border-radius: 12px; overflow: hidden;"></div>
                    <div style="position:absolute; top:0; left:0; width:100%; height:2px; background:#10b981; animation:scan 2s infinite;"></div>
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
                let scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 }, false);
                scanner.render(onScanSuccess);
                const style = document.createElement('style');
                style.innerHTML = `@keyframes scan { 0% { top:0; } 100% { top:100%; } }`;
                document.head.appendChild(style);
                </script>
                """, height=350)

                qr_data = st.text_area("Scanned Result (Or type manually)", placeholder="upi://pay?pa=...")
                
                if qr_data:
                    st.session_state.qr_result = qr_data
                    result = validate_qr(qr_data)
                    if result == "upi":
                        st.success("✅ Valid UPI detected.")
                    elif result == "suspicious":
                        st.warning("⚠️ External URL detected. Proceed with caution.")
                    else:
                        st.error("❌ Invalid format.")
                    
                    if st.button("Proceed to Pay"):
                        st.session_state.popup = "pay"
                        st.rerun()

            # PAY POPUP
            elif st.session_state.popup == "pay":
                st.subheader("Send Money")
                upi = st.text_input("UPI ID or Contact", value=st.session_state.qr_result)
                amt = st.number_input("Amount (₹)", min_value=1.0, step=100.0)
                
                if st.button("Confirm Payment", type="primary"):
                    if amt > st.session_state.balance:
                        st.error("Transaction Failed: Insufficient balance.")
                    else:
                        st.session_state.balance -= amt
                        txid = f"TXN{random.randint(10000000,99999999)}"
                        st.session_state.transactions.insert(0, {
                            "to": upi,
                            "amt": amt,
                            "date": datetime.now().strftime("%d %b, %I:%M %p"),
                            "id": txid
                        })
                        st.success(f"Successfully sent ₹{amt:,.2f} to {upi}")
                        st.balloons()

            # RECHARGE POPUP
            elif st.session_state.popup == "recharge":
                st.subheader("Mobile Recharge")
                num = st.text_input("Mobile Number", max_chars=10)
                operator = st.selectbox("Operator", ["Jio", "Airtel", "Vi", "BSNL"])
                amt = st.number_input("Plan Amount (₹)", min_value=10.0, step=10.0)
                
                if st.button("Recharge Now", type="primary"):
                    if amt > st.session_state.balance:
                        st.error("Transaction Failed: Insufficient balance.")
                    elif len(num) < 10:
                        st.error("Please enter a valid 10-digit number.")
                    else:
                        st.session_state.balance -= amt
                        txid = f"REC{random.randint(10000000,99999999)}"
                        st.session_state.transactions.insert(0, {
                            "to": f"{operator} Mobile - {num}",
                            "amt": amt,
                            "date": datetime.now().strftime("%d %b, %I:%M %p"),
                            "id": txid
                        })
                        st.success("Recharge successful!")

            st.markdown('</div>', unsafe_allow_html=True)

        # Recent Activity Summary
        st.markdown("<br>### 📊 Recent Activity", unsafe_allow_html=True)
        if st.session_state.transactions:
            for tx in st.session_state.transactions[:3]:
                st.markdown(f"""
                <div class="txn-item">
                    <div class="txn-left">
                        <span class="txn-title">{tx['to']}</span>
                        <span class="txn-date">{tx['date']}</span>
                    </div>
                    <div class="txn-amount">- ₹{tx['amt']:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent transactions found.")

    with col2:
        # Balance Card (Right Side)
        st.markdown(f"""
        <div class="balance-card">
            <h4>Available Balance</h4>
            <h1>₹{st.session_state.balance:,.2f}</h1>
            <span class="bank-info">✔ {st.session_state.profile['bank']} • {st.session_state.profile['mask']}</span>
            <br><br>
            <hr style="border:0; border-top: 1px solid #f1f5f9; margin: 15px 0;">
            <p style="font-size: 0.9rem; color: #64748b; margin:0;">UPI ID: <b>{st.session_state.profile['upi']}</b></p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 2. SEND MONEY (Dedicated Page)
# ==========================================
elif nav_selection == "💸 Send Money":
    st.title("💸 Send Money")
    st.write("Transfer funds securely via UPI.")
    
    with st.container():
        st.markdown('<div class="action-card">', unsafe_allow_html=True)
        rcv_upi = st.text_input("Receiver's UPI ID / Phone Number")
        transfer_amt = st.number_input("Amount (₹)", min_value=1.0, step=50.0)
        remarks = st.text_input("Remarks (Optional)", placeholder="e.g., Dinner split")
        
        if st.button("Secure Transfer", type="primary"):
            if not rcv_upi:
                st.error("Please provide a valid receiver.")
            elif transfer_amt > st.session_state.balance:
                st.error("Insufficient balance.")
            else:
                st.session_state.balance -= transfer_amt
                txid = f"TXN{random.randint(10000000,99999999)}"
                st.session_state.transactions.insert(0, {
                    "to": rcv_upi,
                    "amt": transfer_amt,
                    "date": datetime.now().strftime("%d %b, %I:%M %p"),
                    "id": txid
                })
                st.success(f"Transfer of ₹{transfer_amt:,.2f} completed successfully!")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 3. TRANSACTION HISTORY
# ==========================================
elif nav_selection == "📊 Transaction History":
    st.title("📊 Account Statement")
    st.write("View all your recent transactions here.")
    
    if st.session_state.transactions:
        for tx in st.session_state.transactions:
            st.markdown(f"""
            <div class="txn-item">
                <div class="txn-left">
                    <span class="txn-title">{tx['to']}</span>
                    <span class="txn-date">{tx['date']} &nbsp;•&nbsp; Ref: {tx['id']}</span>
                </div>
                <div class="txn-amount">- ₹{tx['amt']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transaction history available.")


# ==========================================
# 4. MY PROFILE
# ==========================================
elif nav_selection == "👤 My Profile":
    st.title("👤 My Profile")
    p = st.session_state.profile
    
    c1, c2 = st.columns([1, 2])
    with c1:
        # Displaying a QR code using an external API for realism
        st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={p['upi']}", caption="My Receive QR")
        
    with c2:
        st.markdown(f"""
        <div class="action-card">
            <h2 style="margin-top:0;">{p['name']}</h2>
            <hr style="margin:10px 0; border-top: 1px solid #f1f5f9;">
            <p style="margin:5px 0;"><b>UPI ID:</b> <span style="color:#2563eb;">{p['upi']}</span></p>
            <p style="margin:5px 0;"><b>Linked Bank:</b> {p['bank']}</p>
            <p style="margin:5px 0;"><b>Account No:</b> {p['mask']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.button("⚙️ Manage Payment Methods")
        st.button("🔒 Security Settings")
