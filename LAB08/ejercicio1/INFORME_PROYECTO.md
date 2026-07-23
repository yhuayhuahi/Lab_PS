# Informe General del Proyecto

**Proyecto:** Catalogo de Videojuegos con Proxy RAWG e Inventario Local  
**Facultad:** Ingenieria de Sistemas  
**Fecha:** 2026-07-03

## 1. Eleccion de la API

Se selecciono la API de RAWG como fuente externa principal por los siguientes motivos:

- Provee un catalogo amplio de videojuegos con metadatos relevantes para un sistema de consulta: nombre, fecha de lanzamiento, generos, rating, plataformas y clasificacion ESRB.
- Permite filtrar por criterios avanzados en el endpoint de juegos, lo que habilita una experiencia de busqueda mas realista para frontend.
- Su documentacion expone parametros de consulta consistentes con los requerimientos del proyecto (fechas, plataforma, metacritic, ordenamiento, etc.).

Para proteger la clave de acceso, el consumo de RAWG no se hace desde el cliente, sino desde el backend mediante un proxy.

## 2. Requerimientos Funcionales

El sistema implementa dos dominios funcionales principales:

1. Catalogo externo (RAWG):
- Consultar juegos mediante proxy backend.
- Aplicar filtros por busqueda, fechas, plataforma, edad (ESRB), metacritic y orden.
- Consultar plataformas para poblar filtros del frontend.

2. Inventario local (API interna en memoria):
- Crear videojuegos con validacion estricta de datos.
- Obtener juego por identificador unico dinamico.
- Listar juegos y filtrar por genero.
- Actualizar stock por delta con reglas de negocio (sin stock negativo).
- Reemplazar recurso completo (PUT).
- Eliminar recurso (DELETE).

Tambien se incluye manejo de errores para entradas invalidas y respuestas HTTP coherentes (400, 404, 5xx segun corresponda).

## 3. Arquitectura Utilizada

### 3.1. Arquitectura general

Se adopto una arquitectura cliente-servidor desacoplada:

- Frontend SPA en React + TypeScript (Vite), responsable de UX y consumo de API.
- Backend REST en Express, responsable de logica de negocio, validaciones y orquestacion de acceso a RAWG.
- Persistencia temporal en memoria para el inventario local, orientada a pruebas de integracion.

Flujo principal:

1. El frontend envia solicitudes al backend.
2. El backend decide si la consulta es local o externa.
3. Para datos externos, el backend llama a RAWG y retorna una respuesta normalizada.
4. Para datos locales, opera sobre el arreglo en memoria y responde segun reglas de validacion.

### 3.2. Estructura del proyecto

El proyecto se organiza en dos aplicaciones separadas:

- `backend/`
  - `app.js`: configuracion de Express, rutas, validaciones, middlewares y export del app para test.
  - `server.js`: arranque de servidor (`app.listen`).
  - `tests/games-api.test.js`: suite de pruebas de integracion con Jest + Supertest.
  - `.env`: clave de acceso RAWG.

- `frontend/`
  - `src/App.tsx`: interfaz principal, filtros y vista detallada.
  - `src/lib/api.ts`: cliente HTTP tipado para backend.
  - `src/types.ts`: contratos TypeScript de datos.
  - `src/styles.css`: estilos de la interfaz.

### 3.3. Tecnologias utilizadas

Backend:

- Node.js
- Express
- dotenv
- cors
- Jest
- Supertest

Frontend:

- React
- TypeScript
- Vite

## 4. Diseno de la API

La API se divide en dos bloques:

1. API interna (inventario local)

- `POST /api/games`
  - Crea un juego.
  - Campos: `title`, `genre`, `stock`.

- `GET /api/games`
  - Lista juegos.
  - Soporta filtro `genre`.

- `GET /api/games/:id`
  - Recupera juego por ID.

- `PUT /api/games/:id`
  - Reemplaza el recurso completo.

- `PATCH /api/games/:id/stock`
  - Modifica stock por `delta`.
  - Regla: no permite stock final negativo.

- `DELETE /api/games/:id`
  - Elimina recurso por ID.

2. API externa proxied (RAWG)

- `GET /api/external/games`
  - Reenvia filtros soportados por RAWG (`search`, `dates`, `platforms`, `esrb_rating`, `metacritic`, `ordering`, etc.).

- `GET /api/external/games/:id`
  - Consulta detalle puntual en RAWG por ID.

- `GET /api/external/platforms`
  - Consulta catalogo de plataformas RAWG.

Criterios de diseno aplicados:

- No exponer `RAWG_API_KEY` al cliente.
- Retornar codigos HTTP semanticos.
- Responder mensajes de error controlados y comprensibles.

## 5. Diseno de las Pruebas de Integracion

La suite de integracion en `backend/tests/games-api.test.js` esta estructurada por escenarios funcionales:

1. Flujo de Persistencia Cruzada
- Verifica creacion (POST) y lectura posterior (GET) usando ID dinamico.
- Evalua aislamiento entre recursos y 404 para IDs inexistentes.
- Incluye actualizacion total con PUT y verificacion posterior.

2. Simulacion de Modificacion de Estado
- Verifica modificaciones de stock positivas y negativas.
- Valida regla de negocio: no permitir stock menor a cero.
- Valida 404 para recursos inexistentes.

3. Listado, Paginacion y Busqueda
- Verifica respuesta de coleccion vacia.
- Verifica listado con multiples recursos.
- Verifica filtro por query parameter (`genre`).

4. Ciclo de Vida Completo
- Verifica eliminacion y posterior 404 al consultar el recurso eliminado.

5. Robustez y Seguridad
- Verifica cuerpos vacios, tipos invalidos, valores negativos y longitud excesiva.
- Verifica payload JSON invalido.
- Verifica proteccion de campos sensibles en operaciones de actualizacion.

6. Proxy RAWG y Resiliencia
- Verifica forwarding de filtros.
- Verifica proxy de plataformas.
- Verifica manejo de error del proveedor y fallos de red.

## 6. Resultados de las Pruebas

Resultado observado en la ejecucion actual de la suite backend:

- **Test Suites:** 1 passed, 1 total
- **Tests:** 28 passed, 28 total
- **Snapshots:** 0 total

Interpretacion:

- La API interna cumple los contratos funcionales definidos por los escenarios de persistencia, actualizacion, listado, borrado y validacion.
- El proxy RAWG responde de forma consistente tanto en exito como en fallos controlados.
- El sistema se considera estable para el alcance del laboratorio bajo el esquema de persistencia temporal en memoria.

Como evidencia complementaria, se recomienda adjuntar en anexos capturas de terminal de `npm test` y `npm run build`.
