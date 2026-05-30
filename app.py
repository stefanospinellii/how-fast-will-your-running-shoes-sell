import streamlit as st
import joblib

st.set_page_config(
    page_title="Running Shoes Sale Time Estimator",
    page_icon="🏃‍♂️",
    layout="centered"
)

model = joblib.load("liquidity_model.pkl")
feature_names = joblib.load("feature_names.pkl")

if "current_price" not in st.session_state:
    st.session_state.current_price = 100

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "saved_message" not in st.session_state:
    st.session_state.saved_message = None

st.title("🏃‍♂️ How fast will your running shoes sell?")

st.write(
    "Estimate how long your running shoes may take to sell and discover simple actions that could help you sell faster."
)

st.subheader("Insert your running shoes details")

brand_models = {
    "Nike": ["Pegasus 41", "Vaporfly 3", "Invincible 3"],
    "Adidas": ["Ultraboost", "Boston 12", "Adizero Pro"],
    "Hoka": ["Clifton 9", "Bondi 8", "Mach 6"],
    "ASICS": ["Gel-Kayano 30", "Novablast 4", "Nimbus 26"],
    "New Balance": ["1080v13", "880v14"],
    "On Running": ["Cloudmonster", "Cloudsurfer"],
    "Brooks": ["Ghost 15", "Glycerin 21"],
    "Saucony": ["Ride 17", "Endorphin Speed"],
    "Mizuno": ["Wave Rider", "Wave Sky"],
    "Other": ["Other"]
}

brand = st.selectbox(
    "Brand",
    list(brand_models.keys())
)

model_name = st.selectbox(
    "Model",
    brand_models[brand]
)

condition = st.selectbox(
    "Condition",
    ["New with tags", "New without tags", "Very Good", "Good", "Fair"]
)

listing_price = st.number_input(
    "Your listing price (€)",
    min_value=10,
    max_value=500,
    value=st.session_state.current_price
)

photos_count = st.slider(
    "Photos uploaded",
    min_value=1,
    max_value=12,
    value=6
)


def estimate_market_price(brand, condition):
    base = {
        "Nike": 90,
        "Adidas": 85,
        "Hoka": 100,
        "ASICS": 90,
        "New Balance": 95,
        "On Running": 110,
        "Brooks": 80,
        "Saucony": 80,
        "Mizuno": 75,
        "Other": 60
    }

    multiplier = {
        "New with tags": 1.25,
        "New without tags": 1.15,
        "Very Good": 1.00,
        "Good": 0.80,
        "Fair": 0.60
    }

    return base[brand] * multiplier[condition]


def estimate_days(price, market_price, photos):
    price_gap_pct = (price - market_price) / market_price
    days = 18 + price_gap_pct * 35 - photos * 0.6
    return max(3, days)


def days_range(days):
    low = max(1, round(days - 2))
    high = round(days + 2)
    return f"{low}-{high} days"


if st.button("Estimate Sale Time"):
    st.session_state.show_results = True


if st.session_state.show_results:

    market_price = estimate_market_price(
        brand,
        condition
    )

    current_days = estimate_days(
        listing_price,
        market_price,
        photos_count
    )

    suggested_price = round(
        listing_price * 0.8
    )

    new_days = estimate_days(
        suggested_price,
        market_price,
        photos_count
    )

    saved_days = current_days - new_days

    st.subheader("Estimated sale time")
    st.markdown(f"## {days_range(current_days)}")

    if st.session_state.saved_message:
        st.success(st.session_state.saved_message)

    st.subheader("Suggestions to sell faster")

    if saved_days >= 2:

        st.info(
            f"Want to sell faster? Lower your price to €{suggested_price}."
        )

        if st.button(f"Lower price to €{suggested_price}"):

            st.session_state.current_price = suggested_price

            st.session_state.saved_message = (
                f"🎉 You may save around {days_range(saved_days)}."
            )

            st.rerun()

    if photos_count < 8:

        missing_photos = 8 - photos_count

        st.info(
            f"Add {missing_photos} more photos to make your listing more attractive."
        )

        st.button(
            "Add photos",
            disabled=True
        )

        st.caption(
            "*Intended as not actionable"
        )

st.divider()

st.caption(
    "*Based on a synthetic dataset of 5,000 running shoe listings."
)
