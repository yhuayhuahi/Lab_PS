def calcular_reembolso(monto, horas, es_vip):
    if monto < 0:
        raise ValueError("MONTO DE RESERVA NEGATIVO!")

    if horas > 72:
        porcentaje = 1.0  
    elif 24 <= horas <= 72:
        porcentaje = 0.5  
    else:
        porcentaje = 0.0  


    if es_vip and porcentaje < 0.5:
        porcentaje = 0.5

    return monto * porcentaje