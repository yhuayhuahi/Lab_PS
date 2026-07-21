from validator import validar_contrasena

def test_validar_contrasena_TC_01():
    assert validar_contrasena("Segura#1") == { "valida": True, "errores": []}

def test_validar_contrasena_TC_02():
    assert validar_contrasena("Ab1!") == { "valida": False, "errores": ["error longitud menor"]}

def test_validar_contrasena_TC_03():
    assert validar_contrasena("segura#1") == { "valida": False, "errores": ["error mayúscula"]}

def test_validar_contrasena_TC_04():
    assert validar_contrasena("SEGURA#1") == { "valida": False, "errores": ["error minúscula"]}

def test_validar_contrasena_TC_05():
    assert validar_contrasena("Segura##") == { "valida": False, "errores": ["error dígito"]}

def test_validar_contrasena_TC_06():
    assert validar_contrasena("Segura12") == { "valida": False, "errores": ["error especial"]}

def test_validar_contrasena_TC_07():
    assert validar_contrasena("") == { "valida": False, "errores": ["error longitud menor", "error mayúscula", "error minúscula", "error dígito", "error especial"]}

def test_validar_contrasena_TC_08():
    assert validar_contrasena("aB1!cDe2") == { "valida": True, "errores": []}

def test_validar_contrasena_TC_09():
    constrasenas_incorrectas = ["Hol@", "estas*", "son", "contraseñ@s", "incorrectAs"]
    assert not any(validar_contrasena(incorrecta).get("valida") for incorrecta in constrasenas_incorrectas)

def test_validar_contrasena_TC_10():
    assert validar_contrasena("Una contras3ñ@") == { "valida": False, "errores": ["error espacio"] }

def test_validar_contrasena_TC_11():
    assert validar_contrasena("Esta3sUnaContraseñ4MuyLarg@") == { "valida": False, "errores": ["error longitud mayor"] }
