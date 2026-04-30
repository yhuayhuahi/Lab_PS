
def evaluar_rendimiento(nota):
    if nota <= 10 and nota >= 0:
        return "Insuficiente"
    elif nota <= 15 and nota >= 11:
        return "Regular"
    elif nota <= 20 and nota >= 16:
        return "Excelente"
    return "Nota fuera de rango"



