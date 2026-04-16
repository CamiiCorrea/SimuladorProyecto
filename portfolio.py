# Clase sencilla para manejar un portafolio de inversión

class Portafolio:
    def __init__(self, dinero_inicial):
        self.dinero = dinero_inicial   # capital disponible
        self.acciones = {}             # acciones compradas
        self.movimientos = []          # historial de compras y ventas

    def comprar(self, nombre_accion, cantidad, precio, comision=5):
        costo_total = cantidad * precio + comision
        if self.dinero >= costo_total:
            self.dinero -= costo_total
            # sumamos la cantidad comprada
            if nombre_accion in self.acciones:
                self.acciones[nombre_accion] += cantidad
            else:
                self.acciones[nombre_accion] = cantidad
            self.movimientos.append(("COMPRA", nombre_accion, cantidad, precio))
        else:
            print("No tienes suficiente dinero para comprar.")

    def vender(self, nombre_accion, cantidad, precio, comision=5):
        if nombre_accion in self.acciones and self.acciones[nombre_accion] >= cantidad:
            ingreso = cantidad * precio - comision
            self.dinero += ingreso
            self.acciones[nombre_accion] -= cantidad
            self.movimientos.append(("VENTA", nombre_accion, cantidad, precio))
        else:
            print("No tienes suficientes acciones para vender.")

