class RentaFija:
    def __init__(self, dinero_inicial, tasa_diaria):
        self.dinero = dinero_inicial
        self.tasa = tasa_diaria
        self.dias = 0
        self.historial = []

    def pasar_dia(self):
        self.dinero *= (1 + self.tasa)
        self.dias += 1
        self.historial.append(self.dinero)
        return self.dinero
