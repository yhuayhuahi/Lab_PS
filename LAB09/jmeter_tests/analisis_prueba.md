
## 1. Extracción de Datos por Escenario

###  Escenario 1 (20 Usuarios Concurrentes | Ramp-Up 10s | 5 Iteraciones)

* **GET - Listar Productos:**
* **Muestras (# Samples):** 100
* **Tiempo promedio de respuesta:** 2 ms
* **Tiempo mínimo:** 2 ms
* **Tiempo máximo:** 4 ms
* **Desviación estándar:** 0.59
* **Error Rate:** 0.00%
* **Throughput:** 10.5 /sec


* **POST - Crear Producto:**
* **Muestras (# Samples):** 100
* **Tiempo promedio de respuesta:** 12 ms
* **Tiempo mínimo:** 11 ms
* **Tiempo máximo:** 18 ms
* **Desviación estándar:** 1.26
* **Error Rate:** 0.00%
* **Throughput:** 10.4 /sec


* **TOTAL (Consolidado Escenario 1):**
* **Muestras Totales:** 200
* **Tiempo promedio de respuesta:** **7 ms**
* **Tiempo mínimo:** **2 ms**
* **Tiempo máximo:** **18 ms**
* **Desviación estándar:** **4.86**
* **Error Rate:** **0.00%**
* **Throughput:** **20.9 /sec**

###  Escenario 2 (50 Usuarios Concurrentes | Ramp-Up 20s | 10 Iteraciones)

* **GET - Listar Productos:**
* **Muestras (# Samples):** 500
* **Tiempo promedio de respuesta:** 3 ms
* **Tiempo mínimo:** 2 ms
* **Tiempo máximo:** 8 ms
* **Desviación estándar:** 0.79
* **Error Rate:** 0.00%
* **Throughput:** 22.5 /sec


* **POST - Crear Producto:**
* **Muestras (# Samples):** 500
* **Tiempo promedio de respuesta:** 17 ms
* **Tiempo mínimo:** 11 ms
* **Tiempo máximo:** 1452 ms
* **Desviación estándar:** 74.61
* **Error Rate:** 0.00%
* **Throughput:** 22.5 /sec


* **TOTAL (Consolidado Escenario 2):**
* **Muestras Totales:** 1000
* **Tiempo promedio de respuesta:** **10 ms**
* **Tiempo mínimo:** **2 ms**
* **Tiempo máximo:** **1452 ms**
* **Desviación estándar:** **53.25**
* **Error Rate:** **0.00%**
* **Throughput:** **45.0 /sec**

###  Escenario 3 (100 Usuarios Concurrentes | Ramp-Up 30s | 15 Iteraciones)

* **GET - Listar Productos:**
* **Muestras (# Samples):** 1500
* **Tiempo promedio de respuesta:** 8 ms
* **Tiempo mínimo:** 2 ms
* **Tiempo máximo:** 937 ms
* **Desviación estándar:** 32.32
* **Error Rate:** 0.00%
* **Throughput:** 49.8 /sec


* **POST - Crear Producto:**
* **Muestras (# Samples):** 1500
* **Tiempo promedio de respuesta:** 15 ms
* **Tiempo mínimo:** 11 ms
* **Tiempo máximo:** 459 ms
* **Desviación estándar:** 17.36
* **Error Rate:** 0.00%
* **Throughput:** 49.8 /sec


* **TOTAL (Consolidado Escenario 3):**
* **Muestras Totales:** 3000
* **Tiempo promedio de respuesta:** **12 ms**
* **Tiempo mínimo:** **2 ms**
* **Tiempo máximo:** **937 ms**
* **Desviación estándar:** **26.19**
* **Error Rate:** **0.00%**
* **Throughput:** **99.6 /sec**

## 2. Tabla Comparativa de Rendimiento

| Métrica | Escenario 1 (20 usuarios) | Escenario 2 (50 usuarios) | Escenario 3 (100 usuarios) |
| --- | --- | --- | --- |
| **Muestras Totales (# Samples)** | 200 | 1,000 | 3,000 |
| **Tiempo Promedio (Average)** | **7 ms** | **10 ms** | **12 ms** |
| **Tiempo Mínimo (Min)** | **2 ms** | **2 ms** | **2 ms** |
| **Tiempo Máximo (Max)** | **18 ms** | **1,452 ms** | **937 ms** |
| **Desviación Estándar (Std. Dev.)** | **4.86** | **53.25** | **26.19** |
| **Rendimiento (Throughput)** | **20.9 req/seg** | **45.0 req/seg** | **99.6 req/seg** |
| **Porcentaje de Error (Error %)** | **0.00%** | **0.00%** | **0.00%** |

---

## 3. Análisis del Comportamiento del Sistema

1. **Escalabilidad y Capacidad de Procesamiento (Throughput):**
* El sistema demuestra una excelente capacidad de escalamiento horizontal a nivel de solicitudes. Conforme se incrementa la carga de usuarios concurrentes de 20 a 100, el **Throughput aumenta de manera casi lineal**, pasando de **20.9 req/s a 99.6 req/s**. Esto indica que el servidor web Flask no llegó a un punto de saturación total ni de estrangulamiento (*bottleneck*) drástico.


2. **Estabilidad en Tiempos Promedio de Respuesta:**
* A pesar de aumentar la carga un 500% (de 20 a 100 usuarios), el **tiempo promedio de respuesta se mantuvo sumamente bajo y controlado**, pasando de **7 ms a 12 ms**. Esto representa un incremento de apenas 5 ms en promedio bajo la carga más alta.


3. **Picos de Latencia y Variabilidad (Desviación Estándar):**
* En el **Escenario 1**, el sistema operó con altísima estabilidad ($\text{Std. Dev.} = 4.86$).
* En los **Escenarios 2 y 3**, se observaron picos puntuales de latencia máxima (**1,452 ms** en Escenario 2 y **937 ms** en Escenario 3). Estos picos aislados son atribuibles a la concurrencia de acceso a disco/escritura en la base de datos SQLite (bloqueos temporales de transacción o concurrencia de I/O) o a la sobrecarga inicial del *Ramp-Up*, aunque el promedio general no se vio afectado significativamente.


4. **Confiabilidad del Sistema (Tasa de Error):**
* En los tres escenarios evaluados, el **Error Rate fue estrictamente del 0.00%**. Ninguna petición falló ni devolvió códigos de error HTTP de la familia 5xx/4xx, demostrando la robustez de la API ante cargas masivas simultáneas.
