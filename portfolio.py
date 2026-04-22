from renta_fija import RentaFija   # importamos la clase de renta fija
from datetime import datetime


class Portafolio:
    def __init__(self, dinero_inicial):
        self.dinero = dinero_inicial
        self.acciones = {}
        self.movimientos = []
        self.dividendos = 0
        self.renta_fija = []   # lista de inversiones de renta fija

    def _timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def comprar(self, nombre_accion, cantidad, precio, precio_min, precio_max, comision=5):
        precio = float(round(precio, 2))  # limpiar np.float64
        if precio < precio_min or precio > precio_max:
            print(f"No puedes comprar {nombre_accion} fuera del rango ({precio_min}-{precio_max}).")
            return
        costo_total = cantidad * precio + comision
        if self.dinero >= costo_total:
            self.dinero -= costo_total
            self.acciones[nombre_accion] = self.acciones.get(nombre_accion, 0) + cantidad
            self.movimientos.append(("COMPRA", nombre_accion, cantidad, precio, comision, self._timestamp()))
        else:
            print("No tienes suficiente dinero para comprar.")

    def vender(self, nombre_accion, cantidad, precio, precio_min, precio_max, comision=5):
        precio = float(round(precio, 2))  # limpiar np.float64
        if precio < precio_min or precio > precio_max:
            print(f"No puedes vender {nombre_accion} fuera del rango ({precio_min}-{precio_max}).")
            return 

    def recibir_dividendos(self, nombre_accion, pago_por_accion):
        if nombre_accion in self.acciones:
            total_dividendo = self.acciones[nombre_accion] * pago_por_accion
            self.dinero += total_dividendo
            self.dividendos += total_dividendo
            self.movimientos.append(("DIVIDENDO", nombre_accion, self.acciones[nombre_accion], pago_por_accion, self._timestamp()))
        else:
            print(f"No tienes acciones de {nombre_accion} para recibir dividendos.")

    def invertir_renta_fija(self, monto, tasa_diaria):
        if self.dinero >= monto:
            self.dinero -= monto
            activo = RentaFija(monto, tasa_diaria)
            self.renta_fija.append(activo)
            self.movimientos.append(("COMPRA_RF", monto, tasa_diaria, self._timestamp()))
        else:
            print("No tienes suficiente dinero para invertir en renta fija.")

    def liquidar_renta_fija(self):
        total_interes = 0
        for activo in self.renta_fija:
            activo.pasar_dia()
            interes = activo.historial[-1] - activo.historial[-2]
            self.dinero += interes
            total_interes += interes
        self.movimientos.append(("INTERES_RF", total_interes, self._timestamp()))

    def calcular_rentabilidad_neta(self, valor_inicial):
        valor_total_rf = sum([activo.dinero for activo in self.renta_fija])
        valor_total = self.dinero + valor_total_rf
        rentabilidad = (valor_total - valor_inicial) / valor_inicial * 100
        return rentabilidad

    def mostrar_portafolio(self):
        print("\n=== ESTADO DEL PORTAFOLIO ===")
        print(f"Dinero disponible: ${self.dinero:,.2f}")
        print(f"Acciones en portafolio: {self.acciones}")
        print(f"Dividendos recibidos: ${self.dividendos:,.2f}")
        print("Renta fija:")
        for i, rf in enumerate(self.renta_fija, start=1):
            print(f"  - Activo {i}: ${rf.dinero:,.2f} (días: {rf.dias})")

        print("\nHistorial de movimientos:")
        for mov in self.movimientos:
            tipo = mov[0]
            fecha = mov[-1]  # último elemento es el timestamp
            if tipo == "COMPRA":
                print(f"[{fecha}] COMPRA {mov[2]} de {mov[1]} a ${mov[3]:.2f} (comisión ${mov[4]:.2f})")
            elif tipo == "VENTA":
                print(f"[{fecha}] VENTA {mov[2]} de {mov[1]} a ${mov[3]:.2f} (comisión ${mov[4]:.2f})")
            elif tipo == "DIVIDENDO":
                print(f"[{fecha}] DIVIDENDO de {mov[1]}: {mov[2]} acciones x ${mov[3]:.2f}")
            elif tipo == "COMPRA_RF":
                print(f"[{fecha}] Inversión en renta fija: ${mov[1]:.2f} a tasa diaria {mov[2]}")
            elif tipo == "INTERES_RF":
                print(f"[{fecha}] Interés renta fija del día: ${mov[1]:.2f}")


