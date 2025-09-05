import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY"))
if not API_KEY:
    st.error("⚠️ No API key found! Please set OPENWEATHER_API_KEY in Streamlit Secrets.")

st.set_page_config(page_title="Weather App", page_icon="✨", layout='centered')

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
    background: black !important;
    color: white !important;
}

header[data-testid="stHeader"] * {
    color: white !important;
}
    .stApp {
        background: linear-gradient(135deg, #fce1ec 0%, #ffe6f7 100%);
        font-family: "Comic Sans MS", cursive, sans-serif;
        color: black;
    }
    .metric-card {
        background: linear-gradient(180deg, #fff0f6 0%, #ffd6eb 100%);
        border-radius: 18px;
        padding: 14px;
        margin: 8px;
        box-shadow: 0px 6px 14px rgba(0,0,0,0.08);
        text-align: center;
        font-size: 16px;
    }
    .big-temp {
        font-size: 40px;
        font-weight: 700;
        color: black;
    }
    .stTextInput label {
        color: black !important;
        font-weight: 600;
    }
    div.stButton > button {
        background-color: #ff4d94;
        color: white;
        border-radius: 12px;
        padding: 0.45em 1.3em;
        border: none;
        font-weight: 700;
        display: inline-block;
    }
    div.stButton > button:hover {
        background-color: #e60073;
    }
    /* center the form contents */
    form[data-testid="stForm"] > div[role="group"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* ensure the text input width is reasonable */
    form[data-testid="stForm"] input[type="text"] {
        max-width: 420px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<h1 style='text-align: center;'>✨ Kiruthika's Weather App ✨</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Everyday is Magic!🌸</h4>", unsafe_allow_html=True)


city = st.text_input("Enter a city", "Vellore")
units = "metric"

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def show_weather(city):
    data = fetch_weather(city)
    weather = data["weather"][0]
    main = data["main"]
    temp = main["temp"]
    feels_like = main["feels_like"]
    humidity = main["humidity"]
    clouds = data["clouds"]["all"]
    icon = weather["icon"]
    description = weather["description"].capitalize()
    icon_url = f"http://openweathermap.org/img/wn/{icon}@4x.png"
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    st.markdown(
        f"""
        <div style='text-align:center;'>
            <img src='{icon_url}' width='120'>
            <p style='font-size:20px; font-weight:bold; color:black;'>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='metric-card'>🌡️<br><div class='big-temp'>{temp}°C</div><b>Temperature</b></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'>🥵<br>{feels_like}°C<br><b>Feels Like</b></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"<div class='metric-card'>💧<br>{humidity}%<br><b>Humidity</b></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'>☁️<br>{clouds}%<br><b>Clouds</b></div>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"<div class='metric-card'>🌅<br>{sunrise}<br><b>Sunrise</b></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='metric-card'>🌇<br>{sunset}<br><b>Sunset</b></div>", unsafe_allow_html=True)




if st.button("✨ Show Weather"):
    try:
        show_weather(city)
    except Exception as e:
        st.error(f"Error fetching weather: {e}")
else:
    show_weather("Vellore")
