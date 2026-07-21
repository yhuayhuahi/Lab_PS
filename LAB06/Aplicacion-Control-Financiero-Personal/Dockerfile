# Usamos Python 3.11 que es totalmente compatible con PySide6 6.7.0
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para interfaces gráficas (Qt/PySide6)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx0 \
    libglib2.0-0 \
    libegl1 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libfreetype6 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libdbus-1-3 \          
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar los requerimientos primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Comando por defecto
CMD ["python", "main.py"]
