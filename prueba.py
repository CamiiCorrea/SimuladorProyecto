from portfolio import Portafolio
import matplotlib.pyplot as plt

# Crear portafolio con $2000
mi_portafolio = Portafolio(dinero_inicial=2000)

# Comprar 3 acciones de Apple a $150 cada una
mi_portafolio.comprar("AAPL", 3, 150)

# Comprar 2 acciones de Microsoft a $200 cada una
mi_portafolio.comprar("MSFT", 2, 200)

# Vender 1 acción de Apple a $160
mi_portafolio.vender("AAPL", 1, 160)

# Vender 1 acción de Microsoft a $210
mi_portafolio.vender("MSFT", 1, 210)

# Mostrar el estado final del portafolio
mi_portafolio.mostrar_portafolio()

# Graficar el historial de movimientos
acciones = [mov[1] for mov in mi_portafolio.movimientos]   # nombres de acciones
tipos = [mov[0] for mov in mi_portafolio.movimientos]      # COMPRA o VENTA

plt.figure(figsize=(6,4))
plt.plot(range(len(acciones)), tipos, "o-")
plt.title("Historial de movimientos")
plt.xlabel("Número de operación")
plt.ylabel("Tipo de movimiento")
plt.show()

