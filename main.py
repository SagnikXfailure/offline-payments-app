import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
import base64
import os

st.set_page_config(page_title="GPay Clone", page_icon="💳", layout="centered")

# ---------- HELPER: LOAD IMAGE AS BASE64 ----------
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

# ---------- SESSION STATE ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.00

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

# ---------- CSS & STYLING ----------
st.markdown("""
<style>
    /* Simulate a mobile screen width */
    .block-container {
        max-width: 450px;
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* App Background */
    .stApp { background-color: #ffffff; }

    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }

    /* Custom GPay Top Background */
    .gpay-header {
        background: linear-gradient(180deg, #e3edfd 0%, #f0f4fa 70%, #ffffff 100%);
        padding: 20px 15px;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 1rem -1rem;
    }

    /* Search Bar */
    .search-box {
        background: white;
        border-radius: 30px;
        padding: 12px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        color: #5f6368;
        font-size: 14px;
        margin-top: 10px;
    }
    .search-box img { width: 30px; height: 30px; border-radius: 50%; }

    /* Original Promo Banner (Fallback) */
    .promo-banner {
        text-align: center;
        padding: 20px 0;
        margin-top: 10px;
    }
    .promo-banner h3 {
        font-size: 18px;
        color: #202124;
        margin-bottom: 10px;
        font-weight: 500;
    }
    .promo-btn {
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
    }

    /* Action Grid */
    .action-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px 5px;
        text-align: center;
        margin-top: 10px;
    }
    .action-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 12px;
        color: #3c4043;
    }
    .action-icon {
        font-size: 24px;
        color: #1a73e8;
        margin-bottom: 8px;
    }

    /* UPI Pill */
    .upi-pill-container { text-align: center; margin: 25px 0; }
    .upi-pill {
        background-color: #f1f3f4;
        color: #3c4043;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
    }

    /* People Section */
    .section-title {
        font-size: 20px;
        color: #202124;
        margin: 20px 0 15px 5px;
        font-weight: 400;
    }
    .people-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px 10px;
        text-align: center;
    }
    .person-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .avatar {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        margin-bottom: 8px;
    }
    .person-name {
        font-size: 12px;
        color: #3c4043;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 65px;
    }
    
    /* Transaction/Tabs Overrides */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
</style>
""", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
tab_home, tab_pay, tab_history, tab_profile = st.tabs(
    ["🏠 Home", "💸 Pay", "📜 History", "👤 Profile"]
)

# ---------- 1. HOME (GPAY CLONE UI) ----------
with tab_home:
    
    # Process Banner Image dynamically
    image_filename = "watermarked_img_6238150401824861611.png"
    banner_b64 = get_base64_image(image_filename)
    
    if banner_b64:
        # If image is found, render it neatly
        promo_html = f"""
        <div style="margin-top: 20px; text-align: center;">
            <img src="data:image/png;base64,{banner_b64}" 
                 style="width: 100%; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); object-fit: cover;">
        </div>
        """
    else:
        # Fallback to the original text banner if image isn't downloaded yet
        promo_html = """
        <div class="promo-banner">
            <h3>Instant loans up to ₹8 lakhs</h3>
            <button class="promo-btn">Apply now ></button>
        </div>
        """

    st.markdown(f"""
    <div class="gpay-header">
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #202124; font-weight: 500;">
            <span>10:08</span>
            <span>📶 🔋</span>
        </div>
        
        <div class="search-box">
            <span>🔍 Pay friends and merchants</span>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Abhi" alt="Profile">
        </div>
        
        {promo_html}
        
    </div>
    
    <div class="action-grid">
        <div class="action-item"><div class="action-icon">📱</div>Scan any QR</div>
        <div class="action-item"><div class="action-icon">📞</div>Pay contacts</div>
        <div class="action-item"><div class="action-icon">📲</div>Pay phone number</div>
        <div class="action-item"><div class="action-icon">🏦</div>Bank transfer</div>
        <div class="action-item"><div class="action-icon">@</div>Pay UPI ID</div>
        <div class="action-item"><div class="action-icon">🔄</div>Self transfer</div>
        <div class="action-item"><div class="action-icon">🧾</div>Pay bills</div>
        <div class="action-item"><div class="action-icon">⚡</div>Mobile recharge</div>
    </div>
    
    <div class="upi-pill-container">
        <div class="upi-pill">UPI ID: {st.session_state.profile['upi_id']}</div>
    </div>
    
    <div class="section-title">People</div>
    <div class="people-grid">
        <div class="person-item">
            <div class="avatar" style="background-color: #e8eaed; color: #1a73e8;">🔄</div>
            <div class="person-name">Self transfer</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Dipa'); background-size: cover;"></div>
            <div class="person-name">Dipa</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-color: #00897b;">G</div>
            <div class="person-name">GITA MOH...</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Kinjan'); background-size: cover;"></div>
            <div class="person-name">Kinjan</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Sweta'); background-size: cover;"></div>
            <div class="person-name">Sweta</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-color: #1e88e5;">A</div>
            <div class="person-name">ABHI...</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-color: #546e7a;">B</div>
            <div class="person-name">BAPI DAS</div>
        </div>
        <div class="person-item">
            <div class="avatar" style="background-color: white; border: 1px solid #dadce0; color: #1a73e8;">⌄</div>
            <div class="person-name">More</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------- 2. FUNCTIONAL PAY TAB ----------
with tab_pay:
    st.subheader("Make a Payment")
    
    upi_id = st.text_input("Receiver UPI ID / Phone", placeholder="e.g. dipa@okicici")
    amount = st.number_input("Amount (₹)", min_value=1.0, step=10.0, format="%.2f")
    note = st.text_input("Add a note", placeholder="For lunch...")
    
    if st.button("Secure Pay", type="primary", use_container_width=True):
        if not upi_id:
            st.error("Enter a valid UPI ID or phone number.")
        elif amount > st.session_state.balance:
            st.error("Transaction Failed: Insufficient Bank Balance!")
        else:
            with st.spinner("Processing..."):
                time.sleep(1.5)
            
            # Deduct balance and log transaction
            st.session_state.balance -= amount
            tx_id = f"T{random.randint(1000000000, 9999999999)}"
            st.session_state.transactions.insert(0, {
                "Date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "ID": tx_id,
                "To": upi_id,
                "Note": note if note else "UPI Payment",
                "Amount": amount
            })
            
            st.success(f"₹{amount:,.2f} sent to {upi_id} successfully! ✅")
            st.balloons()


# ---------- 3. HISTORY TAB ----------
with tab_history:
    st.subheader("Transaction History")
    st.write(f"**Current Balance:** ₹{st.session_state.balance:,.2f}")
    st.divider()
    
    if st.session_state.transactions:
        for tx in st.session_state.transactions:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 4px solid #ea4335;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <strong style="color: #202124;">To: {tx['To']}</strong>
                    <strong style="color: #ea4335;">- ₹{tx['Amount']:,.2f}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #5f6368;">
                    <span>{tx['Date']} • {tx['Note']}</span>
                    <span>{tx['ID']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent transactions.")


# ---------- 4. PROFILE / ACCOUNTS TAB ----------
with tab_profile:
    profile = st.session_state.profile
    st.subheader("Bank Accounts")
    
    st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e8eaed; text-align: center;">
        <h3 style="color: #202124; margin: 0;">{profile['bank']}</h3>
        <p style="color: #5f6368; margin-top: 5px;">Account ending in {profile['account_mask']}</p>
        <h2 style="color: #1a73e8; margin: 15px 0;">₹{st.session_state.balance:,.2f}</h2>
        <p style="font-size: 12px; color: #5f6368; background: #f1f3f4; padding: 5px; border-radius: 10px; display: inline-block;">Primary Account</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**UPI ID:** {profile['upi_id']}")
    st.write(f"**Phone:** {profile['phone']}")
