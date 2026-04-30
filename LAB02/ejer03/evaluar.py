
def evaluar_rendimiento(nota):
    try:
        if not isinstance(nota, int):
            raise TypeError()
        
        if nota >= 21 or nota <= -1:
            raise ValueError()
        
        if nota <= 10 and nota >= 0:
            return "Insuficiente"
        elif nota <= 15 and nota >= 11:
            return "Regular"
        elif nota <= 20 and nota >= 16:
            return "Excelente"
    except ValueError:
        return "Nota fuera de rango"
    except TypeError:
        return "Error: Por Favor, solo ingrese un número entero para la nota"

