import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os


os.makedirs("grafikleri", exist_ok=True)


tsla = yf.download("TSLA", period="1y")


tsla["Daily Return"] = tsla["Close"].pct_change()


tsla["SMA_20"] = tsla["Close"].rolling(window=20).mean()
tsla["SMA_50"] = tsla["Close"].rolling(window=50).mean()


delta = tsla["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
tsla["RSI"] = 100 - (100 / (1 + rs))


plt.figure(figsize=(12,6))
plt.plot(tsla["Close"], label="Fiyat")
plt.title("TSLA Hisse Fiyatı (1 Yıl)")
plt.xlabel("Tarih")
plt.ylabel("Fiyat ($)")
plt.legend()
plt.grid(True)
plt.savefig("grafikleri/fiyat.png")
plt.close()

plt.figure(figsize=(12,6))
tsla["Daily Return"].plot()
plt.title("TSLA Günlük Getiri")
plt.ylabel("Getiri (%)")
plt.grid(True)
plt.savefig("grafikleri/getiri.png")
plt.close()


plt.figure(figsize=(12,6))
plt.plot(tsla["Close"], label="Fiyat", alpha=0.4)
plt.plot(tsla["SMA_20"], label="SMA 20", linestyle="--")
plt.plot(tsla["SMA_50"], label="SMA 50", linestyle="--")
plt.title("TSLA Fiyat ve SMA'lar")
plt.xlabel("Tarih")
plt.ylabel("Fiyat ($)")
plt.legend()
plt.grid(True)
plt.savefig("grafikleri/sma.png")
plt.close()


plt.figure(figsize=(12,6))
plt.plot(tsla["RSI"], label="RSI (14)")
plt.axhline(70, color='red', linestyle='--')
plt.axhline(30, color='green', linestyle='--')
plt.title("TSLA RSI (14 Günlük)")
plt.ylabel("RSI")
plt.grid(True)
plt.savefig("grafikleri/rsi.png")
plt.close()


tsla.to_excel("TSLA_1y_analysis.xlsx")
