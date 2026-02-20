import streamlit as st

st.set_page_config(page_title="Flip Profit", page_icon="💸")

st.title("💸 Flip Profit")
st.caption("Buy Smart. Flip Smarter.")

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
