  
def validar_contrasena(str):
    errores = []
    valida = True

    caracteres_especiales = ["!", "@", "#", "$", "%", "^", "&", "*"]

    if (not (len(str) >= 8)):
        valida = valida and False
        errores.append("error longitud menor")

    if (not any(caracter.isupper() for caracter in str)):
        valida = valida and False
        errores.append("error mayúscula")

    if (not any(caracter.islower() for caracter in str)):
        valida = valida and False
        errores.append("error minúscula")

    if (not any(caracter.isnumeric() for caracter in str)):
        valida = valida and False
        errores.append("error dígito")

    if (not any(str.find(especial) != -1 for especial in caracteres_especiales)):
        valida = valida and False
        errores.append("error especial")

    if (not str.find(" ") == -1):
        valida = valida and False
        errores.append("error espacio")

    if (not (len(str) <= 25)):
        valida = valida and False
        errores.append("error longitud mayor")
        
    return { "valida": valida, "errores": errores }


