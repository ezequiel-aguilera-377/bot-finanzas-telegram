import requests
from telegram import Bot
from datetime import datetime

TOKEN = "TU_TOKEN"
CHAT_ID = "TU_CHAT_ID"

bot = Bot(token=TOKEN)

# -------------------------
# DÓLARES
# -------------------------

def obtener_dolares():
    url = "https://api.argentinadatos.com/v1/cotizaciones/dolares"
    data = requests.get(url).json()

    mensaje = "💵 *Cotizaciones del Dólar*\n\n"

    for dolar in data:
        nombre = dolar["casa"].capitalize()
        compra = dolar["compra"]
        venta = dolar["venta"]

        # Endpoint histórico para calcular variación
        historial_url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{dolar['casa']}"
        historial = requests.get(historial_url).json()

        if len(historial) >= 2:
            hoy = historial[-1]["venta"]
            ayer = historial[-2]["venta"]
            variacion = ((hoy - ayer) / ayer) * 100
            variacion_str = f"{variacion:+.2f}%"
        else:
            variacion_str = "N/D"

        mensaje += (
            f"*{nombre}*\n"
            f"Compra: ${compra}\n"
            f"Venta: ${venta}\n"
            f"Variación: {variacion_str}\n\n"
        )

    return mensaje


# -------------------------
# INFLACIÓN
# -------------------------

def obtener_inflacion():
    url = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
    data = requests.get(url).json()

    if len(data) >= 2:
        ultimo = data[-1]
        anterior = data[-2]

        valor = ultimo["valor"]
        valor_anterior = anterior["valor"]

        variacion = valor - valor_anterior

        mensaje = (
            "📊 *Inflación (IPC)*\n\n"
            f"Último dato ({ultimo['fecha']}): {valor:.2f}%\n"
            f"Variación vs mes anterior: {variacion:+.2f} pp\n"
        )
    else:
        mensaje = "📊 No hay datos suficientes de inflación."

    return mensaje


# -------------------------
# MENSAJE FINAL
# -------------------------

def enviar_resumen():
    mensaje = "📅 *Resumen Económico Diario*\n"
    mensaje += f"{datetime.now().strftime('%d/%m/%Y')}\n\n"
    mensaje += obtener_dolares()
    mensaje += "\n"
    mensaje += obtener_inflacion()

    bot.send_message(
        chat_id=CHAT_ID,
        text=mensaje,
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    enviar_resumen()
