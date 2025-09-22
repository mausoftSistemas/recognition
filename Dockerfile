FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para OpenCV e InsightFace
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libgoogle-glog-dev \
    libgflags-dev \
    libgtest-dev \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para modelos de InsightFace
RUN mkdir -p ~/.insightface/models

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]