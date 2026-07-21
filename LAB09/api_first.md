# 📄 Contrato de la API REST: Sistema de Gestión de Productos

* **Servidor Base (Entorno Local):** `http://localhost:5000`
* **Formato de datos:** `JSON`
* **Encabezado obligatorio para solicitudes POST y PUT:** `Content-Type: application/json`

---

## 1. Resumen de Endpoints

| Método | Endpoint | Descripción | Código HTTP Éxito |
| --- | --- | --- | --- |
| **GET** | `/api/productos` | Obtener la lista completa de productos | `200 OK` |
| **GET** | `/api/productos/<id>` | Obtener el detalle de un producto por ID | `200 OK` |
| **POST** | `/api/productos` | Crear/registrar un nuevo producto | `201 Created` |
| **PUT** | `/api/productos/<id>` | Actualizar todos los datos de un producto | `200 OK` |
| **DELETE** | `/api/productos/<id>` | Eliminar un producto por ID | `200 OK` |

---

## 2. Definición de la Entidad (Objeto Producto)

Todo producto manipulado por la API debe tener la siguiente estructura de campos y tipos de datos:

| Campo | Tipo | Requerido en POST | Descripción / Regla de Validación |
| --- | --- | --- | --- |
| `id` | Entero (`int`) | No (Lo genera el sistema) | Identificador único numérico mayor a 0. |
| `nombre` | Cadena (`string`) | **Sí** | Texto no vacío. Ejemplo: `"Teclado Mecánico"`. |
| `precio` | Número (`float` / `int`) | **Sí** | Valor numérico mayor o igual a 0. |
| `stock` | Entero (`int`) | **Sí** | Cantidad de unidades disponibles (entero $\ge 0$). |
| `categoria` | Cadena (`string`) | **Sí** | Categoria del producto. Ejemplo: `"Accesorios"`. |

---

## 3. Especificación Detallada de Endpoints

### 🟢 3.1. Obtener todos los productos

* **Ruta:** `GET /api/productos`
* **Entrada:** Ninguna.
* **Respuesta Exitosa (`200 OK`):**
```json
[
  {
    "id": 1,
    "nombre": "Laptop Pro 15",
    "precio": 1250.00,
    "stock": 10,
    "categoria": "Computación"
  },
  {
    "id": 2,
    "nombre": "Mouse Inalámbrico",
    "precio": 25.50,
    "stock": 50,
    "categoria": "Accesorios"
  }
]

```
---

### 🟢 3.2. Obtener un producto por ID

* **Ruta:** `GET /api/productos/<id>`
* **Parámetro de URL:** `<id>` debe ser un número entero.
* **Respuesta Exitosa (`200 OK`):**
```json
{
  "id": 1,
  "nombre": "Laptop Pro 15",
  "precio": 1250.00,
  "stock": 10,
  "categoria": "Computación"
}

```

* **Respuesta de Error (`404 Not Found`):** (Si el ID no existe)
```json
{
  "error": "Producto no encontrado"
}

```
---

### 🟡 3.3. Crear un nuevo producto

* **Ruta:** `POST /api/productos`
* **Encabezado:** `Content-Type: application/json`
* **Cuerpo de la Petición (Ejemplo válido):**
```json
{
  "nombre": "Monitor 27 Pulgadas",
  "precio": 300.00,
  "stock": 15,
  "categoria": "Pantallas"
}

```

* **Respuesta Exitosa (`201 Created`):**
```json
{
  "id": 3,
  "nombre": "Monitor 27 Pulgadas",
  "precio": 300.00,
  "stock": 15,
  "categoria": "Pantallas"
}
```

* **Respuestas de Error:**
* **Faltan campos obligatorios (`400 Bad Request`):**
```json
{
  "error": "El campo 'nombre' es obligatorio"
}

```

* **Tipos de datos inválidos (`400 Bad Request`):**
```json
{
  "error": "El campo 'precio' debe ser un valor numérico"
}

```

---

### 🔵 3.4. Actualizar un producto existente

* **Ruta:** `PUT /api/productos/<id>`
* **Encabezado:** `Content-Type: application/json`
* **Cuerpo de la Petición:**
```json
{
  "nombre": "Monitor 27 Pulgadas 4K",
  "precio": 350.00,
  "stock": 12,
  "categoria": "Pantallas"
}

```


* **Respuesta Exitosa (`200 OK`):** Retorna el objeto completamente actualizado.
* **Respuestas de Error:**
* **Recurso no encontrado (`404 Not Found`):** Si el ID no existe.
* **Datos inválidos / incompletos (`400 Bad Request`).**



---

### 🔴 3.5. Eliminar un producto

* **Ruta:** `DELETE /api/productos/<id>`
* **Entrada:** Ninguna en el cuerpo.
* **Respuesta Exitosa (`200 OK`):**
```json
{
  "mensaje": "Producto eliminado exitosamente"
}

```


* **Respuesta de Error (`404 Not Found`):** Si el ID no existe.

---

## 4. Códigos de Estado HTTP y Comportamiento Global

La API debe retornar de manera uniforme estos códigos según la situación:

* **`200 OK`**: Petición procesada con éxito (GET, PUT, DELETE).
* **`201 Created`**: Recurso creado exitosamente (POST).
* **`400 Bad Request`**: Datos de entrada incompletos, vacíos o con tipos de datos incorrectos (Ejercicio 4 - Casos 2 y 3).
* **`404 Not Found`**: El identificador solicitado en la URL no existe (Ejercicio 4 - Caso 1).
* **`405 Method Not Allowed`**: Se intenta acceder a una ruta usando un método HTTP no implementado como `PATCH` o `TRACE` (Ejercicio 4 - Caso 4).

---

## 5. Distribución de Tareas por Integrante según el Contrato

1. **Persona 1 (API Flask):** Programa el servidor implementando exactas estas rutas y asegurando devolver los códigos `200`, `201`, `400`, `404` y `405`.
2. **Persona 2 (JMeter):** Configura los *HTTP Requests* apuntando a `http://localhost:5000/api/productos` para `GET` y `POST`.
3. **Persona 3 (K6):** Prepara el script simulando lecturas (`GET /api/productos`) y escrituras (`POST /api/productos`) con los campos exactos del contrato.
4. **Persona 4 (Python - Seguridad):** Prepara los scripts probando peticiones a IDs inexistentes (p. ej. `/api/productos/999`), datos incompletos (POST sin `nombre`), tipos incorrectos (`precio: "ABC"`), y el método `PATCH /api/productos`.
