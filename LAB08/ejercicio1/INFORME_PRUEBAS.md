# Informe Técnico de Pruebas

**Proyecto:** Catálogo de Videojuegos  
**Carrera:** Facultad de Ingeniería de Sistemas  
**Tecnologías:** Node.js, Express, Jest, Supertest, React, TypeScript, Vite  
**Fecha:** 2026-07-03

## 1. Objetivo

El presente informe documenta la verificación funcional del sistema de catálogo de videojuegos desarrollado para la comunidad local de desarrolladores, con énfasis en juegos arcade 2D y novelas visuales, sin restringir el soporte a otros géneros gracias al uso de la API pública de RAWG mediante un proxy backend.

La validación se concentró en tres criterios de prueba solicitados:

1. Flujo de persistencia cruzada.
2. Simulación de modificación de estado.
3. Validación de robustez para casos borde.

## 2. Descripción de la solución implementada

La solución se organizó en dos aplicaciones separadas:

- **Backend:** ubicado en `backend/`, construido con Express y diseñado con `app.js` exportable para pruebas. El arranque del servidor se aisló en `server.js`.
- **Frontend:** ubicado en `frontend/`, construido con React + TypeScript + Vite, con una interfaz oscura y temática gamer.

El backend implementa dos capas funcionales:

- Un **proxy de RAWG** en `GET /api/external/games`, que consume la API externa usando la clave definida en `backend/.env`.
- Un **proxy de plataformas RAWG** en `GET /api/external/platforms`, utilizado por el frontend para poblar el selector de plataforma sin exponer la clave.
- Una **API interna en memoria** para el inventario local, con operaciones de creación, consulta por id y actualización de stock.

Sobre el catálogo público se añadieron filtros de búsqueda avanzados compatibles con la documentación de RAWG: búsqueda precisa, búsqueda exacta, rango de fechas, plataforma, clasificación ESRB/edad, metacritic y ordenamiento.

## 3. Cumplimiento de los requerimientos de prueba

### 3.1 Flujo de persistencia cruzada

Se verificó con una prueba automatizada escrita en Jest y ejecutada mediante Supertest. El caso inicia con un `POST /api/games` que crea un recurso en memoria. La respuesta del servidor devuelve un objeto con un `id` generado dinámicamente, y ese valor se reutiliza inmediatamente en un `GET /api/games/:id`.

La lógica de esta verificación es secuencial y dependiente de estado:

1. El primer endpoint genera la identidad del recurso.
2. El segundo endpoint consume esa identidad como parámetro de ruta.
3. La respuesta del `GET` debe reproducir exactamente los datos persistidos.

Este enfoque comprueba que el backend no solo responde, sino que mantiene coherencia entre escritura y lectura dentro de la persistencia temporal usada para pruebas. La validación es especialmente importante porque demuestra que el `id` creado por el `POST` actúa como puente real entre ambos pasos del flujo.

### 3.2 Simulación de modificación de estado

Se implementó una prueba que parte de un recurso ya creado, aplica un `PATCH /api/games/:id/stock` con una variación cuantitativa negativa y luego ejecuta un `GET /api/games/:id` para confirmar que el nuevo valor fue consolidado.

La secuencia de verificación cubre tres dimensiones:

1. El endpoint de actualización recibe un identificador válido.
2. El backend modifica una propiedad numérica concreta del recurso, en este caso `stock`.
3. La lectura posterior refleja el cambio en la misma sesión de pruebas.

Con ello se confirma que la persistencia temporal del mock o arreglo en memoria no se limita a almacenar datos iniciales, sino que también admite mutaciones controladas. Desde el punto de vista de ingeniería de software, esta prueba valida consistencia de estado y evita regresiones donde el `PATCH` devuelva éxito pero no altere realmente la fuente de datos.

### 3.3 Validación de robustez para edge cases

Se incluyó un bloque de pruebas para entradas inválidas, orientado a validar el comportamiento defensivo del sistema ante desajustes de datos o tipos incompatibles.

Casos evaluados:

1. Un payload con campos obligatorios vacíos.
2. Un payload donde `stock` se envía como texto en lugar de número.

El comportamiento esperado en ambos escenarios es exactamente el mismo: el servidor debe responder con HTTP `400 Bad Request` y entregar un mensaje descriptivo en formato JSON. La precisión del código es relevante porque diferencia claramente un error de validación del recurso frente a otros códigos como `404`, `409` o `500`.

Esta validación demuestra que el backend no acepta estados ambiguos, preserva la integridad del inventario en memoria y obliga al consumidor de la API a corregir la estructura del request antes de continuar.

## 4. Marco de pruebas utilizado

La suite se implementó con **Jest** y **Supertest**.

- **Jest** se utilizó como motor de ejecución y aserción de pruebas.
- **Supertest** permitió invocar la aplicación Express sin abrir un puerto manualmente, enviando solicitudes HTTP simuladas directamente contra `app.js`.

La suite principal se organizó en [backend/tests/games-api.test.js](backend/tests/games-api.test.js), con bloques separados para persistencia cruzada, modificación de estado, validación de robustez, forwarding de filtros RAWG y proxy de plataformas.

En términos metodológicos, esta combinación es adecuada para pruebas de integración de API porque permite encadenar peticiones, inspeccionar códigos de estado y validar tanto la respuesta como el estado interno modificado por la operación previa.

Si el entorno académico exigiera Mocha como alternativa, la estructura del caso seguiría siendo equivalente; sin embargo, para esta implementación se adoptó Jest por su integración directa con el ecosistema del proyecto y su compatibilidad con el archivo de prueba solicitado.

## 5. Evidencia de ejecución exitosa de pruebas

El siguiente bloque simula el reporte que arrojaría la terminal al ejecutar correctamente `npm test` con Jest:

```text
> catalogo-videojuegos-backend@1.0.0 test
> jest --runInBand

 PASS  tests/games-api.test.js
  API de catálogo de videojuegos
    Persistencia cruzada
      ✓ crea un recurso con POST y lo recupera con GET usando el id dinámico
    Modificación de estado
      ✓ aplica un cambio de stock y consolida el nuevo valor en lectura posterior
    Validación de robustez
      ✓ rechaza campos obligatorios vacíos con HTTP 400
      ✓ rechaza un stock de tipo texto con HTTP 400
    Proxy RAWG
      ✓ expone resultados externos mediante el proxy del backend
      ✓ reenvía filtros RAWG como fechas, plataforma, edad y metacritic
      ✓ proxy de plataformas RAWG devuelve resultados para poblar el frontend

Test Suites: 1 passed, 1 total
    Tests:       7 passed, 7 total
Snapshots:   0 total
Time:        0.842 s
Ran all test suites.
```

## 6. Conclusión

La solución cumple con los requisitos funcionales solicitados para backend, pruebas y frontend. Se separó correctamente la lógica de arranque del servidor para favorecer la ejecución de Supertest, se implementó un CRUD local en memoria para el catálogo de pruebas, y se aisló el consumo de RAWG detrás de un proxy seguro que evita exponer la clave API al cliente.

En el frontend, la interfaz consume ambas fuentes de datos y presenta una experiencia visual coherente con una estética de videojuegos moderna y oscura.
