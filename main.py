with home:

    st.markdown(f"""
    <div class="header">
        <h3>Hello, {st.session_state.profile['name']}</h3>
        <p>Welcome back</p>
    </div>

    <div class="balance">
        <div>Available Balance</div>
        <div class="amount">₹{st.session_state.balance:,.2f}</div>
        <small>{st.session_state.profile['bank']} • {st.session_state.profile['mask']}</small>
    </div>
    """, unsafe_allow_html=True)

    # ---------- PRIMARY SHORTCUTS ----------
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

    # ---------- SECONDARY SERVICES ----------
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

    # ---------- RECENT ACTIVITY ----------
    st.markdown("### 📊 Recent Activity")

    if st.session_state.transactions:
        for tx in st.session_state.transactions[:3]:
            st.markdown(f"""
            <div class="card">
                <b>{tx['to']}</b>
                <div style="float:right;color:red;">-₹{tx['amt']:,.2f}</div>
                <div style="font-size:12px;color:gray;">
                    {tx['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent transactions yet.")
