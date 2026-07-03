# Informe Tabulado de Pruebas Propuestas

**Proyecto:** Catalogo de Videojuegos (Backend API + Proxy RAWG)  
**Fuente de referencia:** Suite de integracion en backend/tests/games-api.test.js  
**Fecha:** 2026-07-03

## Resumen General

| Indicador | Valor |
|---|---:|
| Total de suites | 1 |
| Total de pruebas propuestas | 28 |
| Pruebas por API interna | 22 |
| Pruebas por proxy RAWG | 6 |
| Enfoque | Integracion HTTP con Jest + Supertest |

## 1) Flujo de Persistencia Cruzada

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| FPC-01 | Crea un recurso y lo recupera por ID dinamico | POST /api/games, GET /api/games/:id | title, genre, stock validos | POST 201, GET 200 y payload consistente |
| FPC-02 | Crea multiples recursos y valida aislamiento por ID | POST /api/games (x2), GET /api/games/:id (x2) | Dos juegos distintos | IDs distintos y lectura coherente por cada ID |
| FPC-03 | GET con ID inexistente | GET /api/games/:id | id-falso-o-inexistente | 404 con mensaje de error |
| FPC-04 | Actualizacion completa y verificacion de persistencia | PUT /api/games/:id, GET /api/games/:id | title/genre/stock nuevos | PUT 200 y GET posterior con datos actualizados |

## 2) Simulacion de Modificacion de Estado

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| SME-01 | Resta stock y consolida cambio | PATCH /api/games/:id/stock, GET /api/games/:id | delta negativo | PATCH 200 y stock actualizado |
| SME-02 | Suma stock y consolida cambio | PATCH /api/games/:id/stock | delta positivo | PATCH 200 y stock incrementado |
| SME-03 | Evita stock por debajo de cero | PATCH /api/games/:id/stock | delta que deja stock < 0 | 400 con mensaje de validacion |
| SME-04 | PATCH sobre recurso inexistente | PATCH /api/games/:id/stock | id inexistente | 404 |

## 3) Listado, Paginacion y Busqueda (Colecciones)

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| LPB-01 | Lista vacia sin registros | GET /api/games | Sin datos previos | 200 y arreglo vacio |
| LPB-02 | Lista completa con registros creados | GET /api/games | Dos registros previos | 200 y longitud esperada |
| LPB-03 | Filtrado por query parameter (genre) | GET /api/games?genre=RPG | Datos mixtos por genero | 200 y solo items del genero filtrado |

## 4) Ciclo de Vida Completo (DELETE)

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| CVC-01 | Elimina recurso existente y valida no existencia posterior | DELETE /api/games/:id, GET /api/games/:id | id existente | DELETE 200/204 y GET posterior 404 |
| CVC-02 | DELETE sobre recurso inexistente | DELETE /api/games/:id | id-fantasma | 404 |

## 5) Validacion de Robustez (Edge Cases)

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| VRE-01 | Campos obligatorios vacios | POST /api/games | title y genre vacios | 400 con mensaje de validacion |
| VRE-02 | Body completamente vacio | POST /api/games | {} | 400 |
| VRE-03 | Tipo invalido en stock | POST /api/games | stock como texto | 400 |
| VRE-04 | Stock inicial negativo | POST /api/games | stock < 0 | 400 |
| VRE-05 | Tipos invalidos en title/genre | POST /api/games | title numerico, genre booleano | 400 |
| VRE-06 | PATCH sin propiedad delta | PATCH /api/games/:id/stock | payload con amount en lugar de delta | 400 |

## 6) Seguridad y Casos Extremos de Validacion (Malicious Input)

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| SEV-01 | Rechaza titulo de longitud excesiva | POST /api/games | title de 300 caracteres | 400 con mensaje de longitud maxima |
| SEV-02 | Ignora intento de modificar campo protegido (id) | PATCH /api/games/:id/stock, GET /api/games/:id | delta + id malicioso | Operacion valida sin alteracion de id real |
| SEV-03 | JSON invalido por sintaxis | POST /api/games | JSON mal formado | 400 |

## 7) Proxy RAWG y Resiliencia

| ID | Caso de prueba | Endpoint(s) | Entrada principal | Resultado esperado |
|---|---|---|---|---|
| PRX-01 | Proxy de juegos retorna datos externos | GET /api/external/games | search + page_size | 200 con count/results |
| PRX-02 | Reenvio de filtros RAWG | GET /api/external/games | dates, platforms, esrb_rating, metacritic, ordering, etc. | URL externa contiene filtros y respuesta controlada |
| PRX-03 | Proxy de plataformas para frontend | GET /api/external/platforms | page_size | 200 con listado de plataformas |
| PRX-04 | Manejo de error del proveedor (5xx externo) | GET /api/external/games | mock RAWG status 500 | 500 o 502 con mensaje |
| PRX-05 | Manejo de timeout/fallo de red | GET /api/external/games | fetch rechazado (timeout) | 500/503/504 con mensaje controlado |
| PRX-06 | Endpoint externo por ID no encontrado | GET /api/external/games/:id | id inexistente en RAWG | 404 |

## Matriz de Cobertura por Tipo

| Tipo de validacion | Casos cubiertos | Total |
|---|---|---:|
| Flujo CRUD local | FPC-01, FPC-02, FPC-04, CVC-01, CVC-02 | 5 |
| Estado y reglas de negocio de stock | SME-01, SME-02, SME-03, SME-04 | 4 |
| Listado y filtrado de colecciones | LPB-01, LPB-02, LPB-03 | 3 |
| Validacion de payload y tipos | VRE-01 a VRE-06 | 6 |
| Seguridad y entradas maliciosas | SEV-01 a SEV-03 | 3 |
| Integracion y resiliencia con proveedor externo | PRX-01 a PRX-06 | 6 |
| **Total general** | **Todos los casos anteriores** | **28** |

## Observaciones Finales

- La suite propuesta no solo valida respuestas HTTP, tambien valida persistencia temporal, integridad de estado y comportamiento ante errores externos.
- El conjunto de pruebas cubre tanto happy paths como escenarios negativos y de resiliencia.
- La organizacion por bloques facilita trazabilidad entre requerimientos funcionales y verificacion automatizada.
