# Importamos las librerías necesarias
import yfinance as yf
import matplotlib.pyplot as plt
from portfolio import Portafolio   # usamos la clase que hicimos

# Definimos una lista pequeña de acciones
lista_acciones = ["AAPL", "MSFT", "GOOGL"]

# Descargamos los precios históricos de esas acciones
datos = yf.download(lista_acciones, start="2024-01-01", end="2024-12-31")["Adj Close"]

# Creamos un portafolio con $3000 de dinero inicial
mi_portafolio = Portafolio(dinero_inicial=3000)

# Ejemplo: comprar 1 acción de Apple al último precio disponible
precio_apple = datos["AAPL"].iloc[-1]   # último precio de Apple
mi_portafolio.comprar("AAPL", 1, precio_apple)

# Mostramos resultados en consola
print("Dinero restante:", mi_portafolio.dinero)
print("Acciones en portafolio:", mi_portafolio.acciones)

# Graficamos la evolución de Apple
datos["AAPL"].plot()
plt.title("Precio histórico de Apple")
plt.xlabel("Fecha")
plt.ylabel("Precio en USD")
plt.show()
