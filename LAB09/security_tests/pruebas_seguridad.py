import requests

# URL base de tu API Flask
BASE_URL = "http://127.0.0.1:5000/api/productos"

def probar_recurso_inexistente():
    print("\n--- CASO 1: Validación de Recursos Inexistentes ---")
    url = f"{BASE_URL}/99999"  # ID que no existe
    
    try:
        response = requests.get(url)
        print(f"URL probada: {url}")
        print(f"Código recibido: {response.status_code}")
        
        if response.status_code == 404:
            print("Resultado: PASS (Respondió correctamente con 404 Not Found)")
        else:
            print(f"Resultado: FAIL (Se esperaba 404, pero se obtuvo {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API. ¿Está Flask ejecutándose?")

def probar_datos_incompletos():
    print("\n--- CASO 2: Validación de Datos Incompletos ---")
    payload = {
        "precio": 100.0
    }
    
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Payload enviado: {payload}")
        print(f"Código recibido: {response.status_code}")
        print(f"Respuesta JSON: {response.text}")
        
        if response.status_code == 400:
            print("Resultado: PASS (Respondió correctamente con 400 Bad Request)")
        else:
            print(f"Resultado: FAIL (Se esperaba 400, pero se obtuvo {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API.")

def probar_tipos_datos_invalidos():
    print("\n--- CASO 3: Validación de Tipos de Datos ---")
    payload = {
        "nombre": 12345,   # Debería ser string
        "precio": "ABC"    # Debería ser numérico
    }
    
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Payload enviado: {payload}")
        print(f"Código recibido: {response.status_code}")
        print(f"Respuesta JSON: {response.text}")
        
        if response.status_code in [400, 422]:
            print("Resultado: PASS (La API rechazó correctamente los datos inválidos)")
        else:
            print(f"Resultado: FAIL (Se esperaba 400/422, pero se obtuvo {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API.")

def probar_metodo_no_permitido():
    print("\n--- CASO 4: Métodos HTTP No Permitidos ---")
    
    try:
        # Probamos enviando PATCH a la ruta principal
        response = requests.patch(BASE_URL)
        print(f"Método probado: PATCH sobre {BASE_URL}")
        print(f"Código recibido: {response.status_code}")
        
        if response.status_code == 405:
            print("Resultado: PASS (Respondió correctamente con 405 Method Not Allowed)")
        else:
            print(f"Resultado: FAIL (Se esperaba 405, pero se obtuvo {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API.")

if __name__ == "__main__":
    print("==================================================")
    print(" EJECUCIÓN DE PRUEBAS BÁSICAS DE SEGURIDAD (API)")
    print("==================================================")
    
    probar_recurso_inexistente()
    probar_datos_incompletos()
    probar_tipos_datos_invalidos()
    probar_metodo_no_permitido()
    
    print("\n==================================================")
    print(" PRUEBAS FINALIZADAS")
    print("==================================================")
