import yfinance as yf
import matplotlib.pyplot as plt
from portfolio import Portafolio


# Lista de al menos 10 acciones
tickers = ["AAPL","MSFT","TSLA","AMZN","GOOG","META","NVDA","JPM","NFLX","BAC"]

# Descargar precios históricos
data = yf.download(tickers, period="1mo")["Close"]

# Crear portafolio
mi_portafolio = Portafolio(dinero_inicial=100000)
valor_inicial = mi_portafolio.dinero

# Invertir en renta fija
mi_portafolio.invertir_renta_fija(2000, tasa_diaria=0.0005)

# Simular 10 días
evolucion = []
for dia in range(10):
    precios_dia = data.iloc[dia]

    # AQUÍ es donde pegas las compras de varias empresas
    precio_aapl = precios_dia["AAPL"]
    mi_portafolio.comprar("AAPL", 1, precio_aapl,
                          precio_min=precio_aapl*0.95,
                          precio_max=precio_aapl*1.05)

    precio_msft = precios_dia["MSFT"]
    mi_portafolio.comprar("MSFT", 1, precio_msft,
                          precio_min=precio_msft*0.95,
                          precio_max=precio_msft*1.05)

    precio_tsla = precios_dia["TSLA"]
    mi_portafolio.comprar("TSLA", 1, precio_tsla,
                          precio_min=precio_tsla*0.95,
                          precio_max=precio_tsla*1.05)

    # Liquidar renta fija cada día
    mi_portafolio.liquidar_renta_fija()

    # Guardar evolución
    evolucion.append(mi_portafolio.dinero + sum([rf.dinero for rf in mi_portafolio.renta_fija]))


# Mostrar portafolio final
mi_portafolio.mostrar_portafolio()
print("Rentabilidad neta:", mi_portafolio.calcular_rentabilidad_neta(valor_inicial), "%")

# Graficar evolución
plt.plot(evolucion, marker="o")
plt.title("Evolución histórica del portafolio")
plt.xlabel("Días")
plt.ylabel("Valor total ($)")
plt.show()