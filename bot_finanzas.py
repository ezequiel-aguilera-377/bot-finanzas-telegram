import requests
import yfinance as yf
from datetime import datetime
import os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = "7638035451"

def obtener_variacion(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="2d")

    if len(hist) < 2:
        return None

    cierre_ayer = hist["Close"].iloc[-2]
    cierre_hoy = hist["Close"].iloc[-1]

    variacion = ((cierre_hoy - cierre_ayer) / cierre_ayer) * 100

    return cierre_hoy, variacion

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto
    }
    requests.post(url, data=payload)

def main():
    activos = {
        "Merval": "^MERV",
        "S&P 500": "^GSPC",
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Petróleo WTI": "CL=F",
        "Soja": "ZS=F"
    }

    mensaje = "📊 Informe Financiero Diario\n\n"

    for nombre, ticker in activos.items():
        resultado = obtener_variacion(ticker)

        if resultado:
            precio, variacion = resultado
            flecha = "↑" if variacion > 0 else "↓"
            mensaje += f"{nombre}: {precio:.2f} ({flecha} {variacion:.2f}%)\n"

    mensaje += f"\nFecha: {datetime.now().strftime('%d/%m/%Y')}"

    enviar_mensaje(mensaje)

if __name__ == "__main__":
    main()
