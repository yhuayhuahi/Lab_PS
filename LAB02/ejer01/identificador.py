
def es_identificador_valido(identificador: str) -> bool:
    # Regla 1 – Longitud entre 1 y 6 caracteres
    if not (1 <= len(identificador) <= 6):
        return False
    return True
