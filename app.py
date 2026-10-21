import streamlit as st
import pandas as pd
import joblib


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Albion Market Predictor",
    page_icon="📈",
    layout="wide"
)


# -----------------------------
# Load model
# -----------------------------

model = joblib.load("albion_price_model.pkl")


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    padding: 2rem;
    border-radius: 15px;
    background: linear-gradient(135deg, #171b24, #202633);
    border: 1px solid #303744;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 0.3rem;
}

.hero p {
    color: #aeb6c4;
    font-size: 1.1rem;
}

.card {
    padding: 1.5rem;
    border-radius: 15px;
    background: #171b24;
    border: 1px solid #303744;
    margin-bottom: 1rem;
}

.prediction {
    padding: 2rem;
    border-radius: 15px;
    background: #171b24;
    border: 1px solid #3d4655;
    text-align: center;
}

.prediction-label {
    color: #aeb6c4;
    font-size: 1rem;
}

.prediction-value {
    font-size: 3rem;
    font-weight: 700;
    margin-top: 0.5rem;
}

.metric-title {
    color: #aeb6c4;
    font-size: 0.9rem;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #707887;
    margin-top: 3rem;
    font-size: 0.85rem;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------

st.markdown("""
<div class="hero">

<h1>📈 Albion Market Price Predictor</h1>

<p>
Machine-learning based price estimation for Albion Online market data.
</p>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙️ Market Inputs")

st.sidebar.markdown(
    "Enter the latest market information to estimate the next price."
)


location = st.sidebar.selectbox(
    "📍 Location",
    ["Caerleon", "Bridgewatch"]
)


item_count = st.sidebar.number_input(
    "📦 Item Count",
    min_value=0,
    value=10,
    step=1
)


day_of_week = st.sidebar.selectbox(
    "📅 Day of Week",
    options=list(range(7)),
    format_func=lambda x: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ][x]
)


month = st.sidebar.slider(
    "🗓️ Month",
    min_value=1,
    max_value=12,
    value=5
)


previous_price = st.sidebar.number_input(
    "💰 Previous Price",
    min_value=0,
    value=20000,
    step=100
)


previous_price_2 = st.sidebar.number_input(
    "💰 Price Before Previous",
    min_value=0,
    value=19000,
    step=100
)


price_change = previous_price - previous_price_2


# -----------------------------
# Main dashboard
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Location</div>
        <div class="metric-value">📍 {}</div>
    </div>
    """.format(location), unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="card">
        <div class="metric-title">Previous Price</div>
        <div class="metric-value">💰 {:,.0f}</div>
    </div>
    """.format(previous_price), unsafe_allow_html=True)


with col3:

    change_symbol = "📈" if price_change >= 0 else "📉"

    st.markdown("""
    <div class="card">
        <div class="metric-title">Price Change</div>
        <div class="metric-value">{} {:,.0f}</div>
    </div>
    """.format(change_symbol, price_change), unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# Prediction
# -----------------------------

st.subheader("🔮 Price Prediction")

st.write(
    "The Random Forest model uses historical market information "
    "to estimate the market price."
)


if st.button(
    "🚀 Predict Market Price",
    use_container_width=True
):

    location_code = 0 if location == "Caerleon" else 1

    input_data = pd.DataFrame(
        [[
            item_count,
            location_code,
            day_of_week,
            month,
            previous_price,
            previous_price_2,
            price_change
        ]],
        columns=[
            "item_count",
            "location_code",
            "day_of_week",
            "month",
            "previous_price",
            "previous_price_2",
            "price_change"
        ]
    )

    prediction = model.predict(input_data)[0]

    difference = prediction - previous_price

    difference_percent = (
        difference / previous_price * 100
        if previous_price != 0
        else 0
    )

    st.markdown(
        f"""
        <div class="prediction">

        <div class="prediction-label">
        Estimated Market Price
        </div>

        <div class="prediction-value">
        💰 {prediction:,.0f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Difference from Previous Price",
            f"{difference:,.0f}",
            f"{difference_percent:+.2f}%"
        )

    with col2:
        st.metric(
            "Previous Price",
            f"{previous_price:,.0f}"
        )


# -----------------------------
# Model information
# -----------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🤖 About the Model")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Algorithm", "Random Forest")

with col2:
    st.metric("R² Score", "0.47")

with col3:
    st.metric("MAE", "3,927")


st.markdown("""
<div class="card">

<b>Features used by the model:</b>

<br><br>

📦 Item count &nbsp;&nbsp; • &nbsp;&nbsp;
📍 Location &nbsp;&nbsp; • &nbsp;&nbsp;
📅 Day of week &nbsp;&nbsp; • &nbsp;&nbsp;
🗓️ Month

<br><br>

💰 Previous price &nbsp;&nbsp; • &nbsp;&nbsp;
💰 Price before previous &nbsp;&nbsp; • &nbsp;&nbsp;
📊 Price change

</div>
""", unsafe_allow_html=True)


# -----------------------------
# Footer
# -----------------------------

st.markdown("""
<div class="footer">

Albion Online Market Price Predictor  
Built with Python • Pandas • Scikit-learn • Streamlit

</div>
            """, unsafe_allow_html=True)
