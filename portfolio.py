from datetime import datetime
from renta_fija import RentaFija

class Portafolio:
    def __init__(self, dinero_inicial):
        self.dinero = dinero_inicial
        self.acciones = {}
        self.movimientos = []
        self.dividendos = 0.0
        self.renta_fija = []

    def comprar(self, simbolo, cantidad, precio, fecha, comision=5):
        costo_total = cantidad * precio + comision
        if self.dinero >= costo_total:
            self.dinero -= costo_total
            self.acciones[simbolo] = self.acciones.get(simbolo, 0) + cantidad
            self.movimientos.append((fecha, f"Compra {cantidad} {simbolo} a {precio:.2f}"))
        else:
            self.movimientos.append((fecha, f"No hay dinero para comprar {simbolo}"))

    def vender(self, simbolo, cantidad, precio, fecha, comision=5):
        if simbolo in self.acciones and self.acciones[simbolo] >= cantidad:
            ingreso = cantidad * precio - comision
            self.dinero += ingreso
            self.acciones[simbolo] -= cantidad
            self.movimientos.append((fecha, f"Venta {cantidad} {simbolo} a {precio:.2f}"))
        else:
            self.movimientos.append((fecha, f"No hay suficientes acciones de {simbolo}"))

    def invertir_renta_fija(self, monto, tasa_diaria, fecha):
        if self.dinero >= monto:
            self.dinero -= monto
            rf = RentaFija(monto, tasa_diaria)
            self.renta_fija.append(rf)
            self.movimientos.append((fecha, f"Inversión renta fija: {monto:.2f}"))
        else:
            self.movimientos.append((fecha, "No hay dinero para invertir en renta fija"))

    def liquidar_renta_fija(self):
        total = 0
        for rf in self.renta_fija:
            total += rf.pasar_dia()
        self.dinero += total
        self.renta_fija.clear()

    def mostrar_portafolio(self):
        return {
            "dinero": self.dinero,
            "acciones": self.acciones,
            "dividendos": self.dividendos,
            "movimientos": self.movimientos
        }

    def reset(self, dinero_inicial):
        self.__init__(dinero_inicial)
