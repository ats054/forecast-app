import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="תחזית מסחר חכמה", layout="centered")
st.title("תחזית מסחר חכמה")
st.write("בחר נכס, קבל המלצה בזמן אמת.")

assets = {
    "ביטקוין (BTC)": "BTC-USD",
    "זהב (Gold)": "GC=F",
    "נאסד\"ק": "^IXIC"
}

asset_name = st.selectbox("בחר נכס:", list(assets.keys()))
ticker = assets[asset_name]

df = yf.download(ticker, period="7d", interval="30m")

if df.empty or df["Close"].dropna().empty:
    st.error("לא נמצאו נתונים.")
else:
    df = df.dropna(subset=["Close"])
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    try:
        last_price = df["Close"].iloc[-1]
        sma_20 = df["SMA_20"].iloc[-1]
        sma_50 = df["SMA_50"].iloc[-1]

        if sma_20 > sma_50:
            signal = "המלצה: קנייה (BUY)"
            confidence = "רמת ביטחון: גבוהה"
        elif sma_20 < sma_50:
            signal = "המלצה: מכירה (SELL)"
            confidence = "רמת ביטחון: גבוהה"
        else:
            signal = "המלצה: להמתין"
            confidence = "רמת ביטחון: בינונית"

        st.subheader(f"נכס: {asset_name}")
        st.write("מחיר נוכחי:")
        if not np.isnan(last_price):
            st.metric(label="", value=f"{last_price:.2f}")
        else:
            st.write("המחיר לא זמין")
        st.write(signal)
        st.write(confidence)

        st.line_chart(df[["Close", "SMA_20", "SMA_50"]].dropna())

    except Exception as e:
        st.error(f"שגיאה במהלך החישוב: {e}")
