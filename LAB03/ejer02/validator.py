  
def validar_contrasena(str):
    errores = []
    valida = True

    caracteres_especiales = ["!", "@", "#", "$", "%", "^", "&", "*"]

    cadena_vacia = False
    if (len(str) == 0):
        cadena_vacia = True

    if (cadena_vacia or not (len(str) >= 8)):
        valida = valida and False
        errores.append("error longitud")

    if (cadena_vacia or not any(caracter.isupper() for caracter in str)):
        valida = valida and False
        errores.append("error mayúscula")

    if (cadena_vacia or not any(caracter.islower() for caracter in str)):
        valida = valida and False
        errores.append("error minúscula")

    if (cadena_vacia or not any(caracter.isnumeric() for caracter in str)):
        valida = valida and False
        errores.append("error dígito")

    if (cadena_vacia or not any(str.find(especial) != -1 for especial in caracteres_especiales)):
        valida = valida and False
        errores.append("error especial")

    return { "valida": valida, "errores": errores }


