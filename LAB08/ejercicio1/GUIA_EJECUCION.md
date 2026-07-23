# Guía de instalación, ejecución y pruebas

Este archivo resume las líneas necesarias para instalar dependencias, levantar el backend y el frontend, y ejecutar las pruebas.

## 1. Backend

### Instalar dependencias
```bash
cd backend
npm install
```

### Levantar el servidor en modo desarrollo
```bash
npm run dev
```

### Ejecutar pruebas
```bash
npm test
```

## 2. Frontend

### Instalar dependencias
```bash
cd frontend
npm install
```

### Levantar la aplicación en modo desarrollo
```bash
npm run dev
```

### Generar build de producción
```bash
npm run build
```

### Previsualizar el build
```bash
npm run preview
```

## 3. Orden recomendado de uso

1. Levantar primero el backend.
2. Luego levantar el frontend.
3. Finalmente ejecutar las pruebas del backend con Jest.

## 4. Comando rápido por carpeta

### Backend
```bash
cd backend
npm install
npm run dev
npm test
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
