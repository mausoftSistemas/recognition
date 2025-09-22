#!/bin/bash

echo "🚀 Iniciando InsightFace API..."

# Instalar dependencias del sistema si no están instaladas
if ! command -v curl &> /dev/null; then
    echo "📦 Instalando dependencias del sistema..."
    apt-get update
    apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgl1-mesa-glx wget curl
    apt-get clean
    rm -rf /var/lib/apt/lists/*
fi

# Instalar dependencias Python si no están instaladas
if [ ! -f "/app/.deps_installed" ]; then
    echo "🐍 Instalando dependencias Python..."
    pip install --no-cache-dir -r requirements.txt
    touch /app/.deps_installed
fi

# Crear directorio para modelos
mkdir -p ~/.insightface/models

echo "✅ Iniciando servidor..."
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 app:app