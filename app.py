
import streamlit as st
import pandas as pd
import joblib

model = joblib.load("albion_price_model.pkl")

st.title("Albion Online Market Price Predictor")

st.write("Predict the average market price using historical market data.")

location = st.selectbox(
    "Location",
    ["Caerleon", "Bridgewatch"]
)

item_count = st.number_input(
    "Item Count",
    min_value=0,
    value=10
)

day_of_week = st.number_input(
    "Day of Week (0 = Monday, 6 = Sunday)",
    min_value=0,
    max_value=6,
    value=2
)

month = st.number_input(
    "Month",
    min_value=1,
    max_value=12,
    value=5
)

previous_price = st.number_input(
    "Previous Price",
    min_value=0,
    value=20000
)

previous_price_2 = st.number_input(
    "Price Before Previous",
    min_value=0,
    value=19000
)

price_change = previous_price - previous_price_2

st.write("Price Change:", price_change)

if st.button("Predict Price"):

    location_code = 0 if location == "Caerleon" else 1

    input_data = pd.DataFrame([[
        item_count,
        location_code,
        day_of_week,
        month,
        previous_price,
        previous_price_2,
        price_change
    ]], columns=[
        "item_count",
        "location_code",
        "day_of_week",
        "month",
        "previous_price",
        "previous_price_2",
        "price_change"
    ])

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Price: {prediction:,.0f}")
