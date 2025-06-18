
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="תחזית מסחר חכמה", layout="centered")
st.title("📈 תחזית מסחר חכמה")
st.write("בחר נכס, קבל המלצה בזמן אמת.")

assets = {
    "ביטקוין (BTC)": "BTC-USD",
    "זהב (Gold)": "GC=F",
    "נאסד"ק": "^IXIC"
}

asset_name = st.selectbox("בחר נכס:", list(assets.keys()))
ticker = assets[asset_name]

df = yf.download(ticker, period="7d", interval="30m")

if df.empty:
    st.error("לא נמצאו נתונים.")
else:
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    last_price = df["Close"].iloc[-1]
    sma_20 = df["SMA_20"].iloc[-1]
    sma_50 = df["SMA_50"].iloc[-1]

    if sma_20 > sma_50:
        signal = "📈 המלצה: קנייה (BUY)"
        confidence = "רמת ביטחון: גבוהה"
    elif sma_20 < sma_50:
        signal = "📉 המלצה: מכירה (SELL)"
        confidence = "רמת ביטחון: גבוהה"
    else:
        signal = "⏸ המלצה: להמתין"
        confidence = "רמת ביטחון: בינונית"

    st.subheader(f"נכס: {asset_name}")
    st.metric("מחיר נוכחי", f"{last_price:.2f}")
    st.write(signal)
    st.write(confidence)

    st.line_chart(df[["Close", "SMA_20", "SMA_50"]].dropna())
