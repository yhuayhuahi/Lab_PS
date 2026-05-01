
def es_identificador_valido(identificador: str) -> bool:
    # Regla 1 – Longitud entre 1 y 6 caracteres
    if not (1 <= len(identificador) <= 6):
        return False

    # Regla 2 – El primer carácter debe ser una letra
    if not identificador[0].isalpha():
        return False


    return True
