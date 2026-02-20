import streamlit as st

st.set_page_config(page_title="Flip Profit", page_icon="💸")

st.title("💸 Flip Profit")
st.caption("Buy Smart. Flip Smarter.")
# --- PRO ACCESS (manual) ---
st.subheader("🔐 Pro Access")

PRO_USERS = {
    # Add paying customer emails here (lowercase)
    # Example:
    # "customer@email.com",
}

user_email = st.text_input("Enter your purchase email to unlock Pro", "").strip().lower()
is_pro = user_email in PRO_USERS

if is_pro:
    st.success("✅ Pro unlocked")
else:
    st.info("🔒 Pro locked — subscribe below to unlock Pro features.")
# --- END PRO ACCESS ---

# --- Upgrade / Subscribe section ---
st.divider()
st.subheader("🚀 Upgrade to Flip Profit Pro")

st.write("Pro includes unlimited calculations, max-bid guidance, and upcoming pro tools.")
colA, colB = st.columns(2)

MONTHLY_LINK = "https://buy.stripe.com/test_00w4gz480dp57Aa4SUfQI00"
YEARLY_LINK  = "https://buy.stripe.com/test_28E00jawoet9dYyadefQI01"

with colA:
    st.markdown("### ✅ Pro Monthly (Default)")
    st.markdown("**$7/mo**")
    st.link_button("Subscribe Monthly", MONTHLY_LINK)

with colB:
    st.markdown("### ⭐ Pro Yearly (Best Value)")
    st.markdown("**$79/yr**")
    st.link_button("Subscribe Yearly", YEARLY_LINK)

st.caption("Payments are handled securely by Stripe. You’ll be redirected back after checkout.")
st.divider()
# --- End Upgrade section ---

buy = st.number_input("Buy Price ($)", 0.0, 10000.0, 25.0)
sell = st.number_input("Expected Sale Price ($)", 0.0, 20000.0, 60.0)
fees = st.slider("Platform Fee %", 0.0, 20.0, 13.25)
shipping = st.number_input("Shipping You Pay ($)", 0.0, 500.0, 0.0)
repairs = st.number_input("Repairs / Cleaning ($)", 0.0, 500.0, 0.0)
days = st.number_input("Days To Sell", 1, 365, 14)

untested = st.checkbox("Untested")
heavy = st.checkbox("Heavy Shipping")
fragile = st.checkbox("Fragile")
slow = st.checkbox("Slow Category")

confidence = st.slider("Confidence %", 30, 100, 80)
target_profit = st.number_input("Target Profit", 0.0, 1000.0, 25.0)

fee_cost = sell * fees / 100
total = buy + shipping + repairs
net = sell - fee_cost - total
roi = (net / total * 100) if total else 0
ppd = net / days
st.subheader("📌 Max Bid (Pro)")

if is_pro:
    max_bid = sell - fee_cost - shipping - repairs - target_profit
    st.metric("Max Bid (to hit target profit)", f"${max_bid:,.2f}")
else:
    st.warning("Pro feature. Subscribe to unlock Max Bid.")

risk = (untested + heavy + fragile + slow) * 10
confidence_penalty = (100 - confidence) * 0.3

score = max(0, min(100, net*2 + roi*.6 + ppd*5 - risk - confidence_penalty))

max_bid = sell - fee_cost - shipping - repairs - target_profit

rec = "PASS"
if net > 0 and score > 65:
    rec = "BUY"
elif net > 0:
    rec = "MAYBE"

st.metric("Net Profit", f"${net:.2f}")
st.metric("ROI", f"{roi:.1f}%")
st.metric("Profit/Day", f"${ppd:.2f}")

st.progress(int(score))
st.write("Flip Score:", int(score))
st.write("Recommendation:", rec)
st.write("Max Buy Price:", f"${max_bid:.2f}")
