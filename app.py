import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from portfolio import Portafolio
from datetime import datetime

st.set_page_config(page_title="Inversión en Portafolio", layout="wide")

st.markdown("<h2 style='color:#1e90ff;text-align:center'>💹 Inversión en Portafolio</h2>", unsafe_allow_html=True)

# Inicializar portafolio en session_state
if "portafolio" not in st.session_state:
    st.session_state.portafolio = Portafolio(7000.0)
if "movimientos" not in st.session_state:
    st.session_state.movimientos = []
if "graficos" not in st.session_state:
    st.session_state.graficos = {}

# Configuración inicial
dinero_inicial = st.sidebar.number_input("Capital inicial:", value=7000.0, step=100.0)

# Botón de reinicio
if st.sidebar.button("🔄 Reiniciar"):
    st.session_state.portafolio = Portafolio(dinero_inicial)
    st.session_state.movimientos = []
    st.session_state.graficos = {}
    st.warning("Simulación reiniciada con dinero inicial.")

# Estado del portafolio
st.subheader("📊 Estado del Portafolio")
estado = st.session_state.portafolio.mostrar_portafolio()
st.success(f"Capital disponible: ${estado['dinero']:,.2f}")
valor_acciones = sum([yf.Ticker(t).history(period="1d")["Close"].iloc[-1].item() * v for t,v in estado["acciones"].items()]) if estado["acciones"] else 0
st.info(f"Valor en acciones: ${valor_acciones:,.2f}")
st.write("Acciones actuales:", estado["acciones"] if estado["acciones"] else "Sin acciones en el portafolio.")

# Nueva orden
st.subheader("📝 Nueva Orden")

tipo = st.radio("Tipo de operación:", ["Compra", "Venta"])
ticker = st.selectbox("Ticker:", ["AAPL","MSFT","TSLA","GOOG","AMZN","META","NVDA","NFLX","BABA","JPM"])
fecha = datetime.now()

# Datos de mercado
data = yf.download(ticker, period="5d")
if not data.empty:
    precio_actual = data["Close"].iloc[-1].item()
    high = data["High"].iloc[-1].item()
    low = data["Low"].iloc[-1].item()
else:
    precio_actual, high, low = 0, 0, 0

st.write(f"**{ticker} — {fecha.strftime('%Y-%m-%d')}**")
st.write(f"Cierre: {precio_actual:.2f} | Rango: Máximo {high:.2f} – Mínimo {low:.2f}")

precio = st.number_input("Precio por acción ($):", value=float(precio_actual), step=0.1)
cantidad = st.number_input("Cantidad:", value=1, step=1)
comision_pct = st.number_input("Comisión (%):", value=1.0, step=0.1)

# Cálculos previos
total_estimado = precio * cantidad
comision_estimado = total_estimado * (comision_pct/100)
capital_restante = estado["dinero"] - total_estimado - comision_estimado if tipo=="Compra" else estado["dinero"] + total_estimado - comision_estimado

st.markdown(f"**Total estimado:** ${total_estimado+comision_estimado:,.2f}")
st.markdown(f"**Comisión estimada:** ${comision_estimado:,.2f}")
st.markdown(f"**Capital restante:** ${capital_restante:,.2f}")

# Botón de ejecución
if st.button(f"Ejecutar {tipo} — {cantidad} {ticker}"):
    if tipo == "Compra":
        st.session_state.portafolio.comprar(ticker, cantidad, precio, fecha, comision=comision_estimado)
        st.session_state.movimientos.append((fecha, f"Compra {cantidad} {ticker} a {precio:.2f}"))
        if ticker not in st.session_state.graficos:
            st.session_state.graficos[ticker] = yf.download(ticker, period="6mo")
        st.success(f"Compra ejecutada: {cantidad} {ticker} a ${precio:.2f}")
    else:
        if ticker not in estado["acciones"] or estado["acciones"][ticker] < cantidad:
            st.error(f"No tienes suficientes acciones de {ticker} para vender.")
        else:
            st.session_state.portafolio.vender(ticker, cantidad, precio, fecha, comision=comision_estimado)
            st.session_state.movimientos.append((fecha, f"Venta {cantidad} {ticker} a {precio:.2f}"))
            if ticker not in st.session_state.graficos:
                st.session_state.graficos[ticker] = yf.download(ticker, period="6mo")
            st.success(f"Venta ejecutada: {cantidad} {ticker} a ${precio:.2f}")

# Historial de movimientos
st.subheader("🕒 Historial de Movimientos")
for fecha, mov in st.session_state.movimientos:
    st.markdown(
        f"<div style='background:#222;color:#fff;padding:8px;margin:5px;border-radius:5px'>{fecha.strftime('%d/%m/%Y %H:%M:%S')} - {mov}</div>",
        unsafe_allow_html=True
    )

# Gráficos
st.subheader("📈 Gráficos de Evolución")

# Evolución de precios de las acciones
fig1, ax1 = plt.subplots()
for t, datos in st.session_state.graficos.items():
    if not datos.empty:
        ax1.plot(datos.index, datos["Close"], label=f"{t} (Cierre)")
ax1.set_title("Precios de acciones")
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Valor ($)")
ax1.legend()
st.pyplot(fig1)

# Gráfico Máximo vs Mínimo del último ticker
st.subheader("📉 Rango de precios (Máximo vs Mínimo)")
if not data.empty:
    fig2, ax2 = plt.subplots()
    ax2.plot(data.index, data["High"], label="Máximo", color="red")
    ax2.plot(data.index, data["Low"], label="Mínimo", color="blue")
    ax2.set_title(f"{ticker} - Máximo vs Mínimo")
    ax2.set_xlabel("Fecha")
    ax2.set_ylabel("Valor ($)")
    ax2.legend()
    st.pyplot(fig2)
