# InsightFace API Backend

Backend API para reconocimiento facial usando InsightFace, preparado para despliegue en Coolify.

## Características

- **Detección de caras**: Detecta caras en imágenes y extrae información como edad, género y landmarks
- **Comparación facial**: Compara dos caras y determina si pertenecen a la misma persona
- **API REST**: Endpoints simples y fáciles de usar
- **Docker**: Listo para despliegue en contenedores

## Endpoints

### GET /health
Verifica el estado del servicio y si el modelo está cargado.

### POST /detect
Detecta caras en una imagen.

**Request:**
```json
{
  "image": "base64_encoded_image"
}
```

**Response:**
```json
{
  "faces_detected": 1,
  "faces": [
    {
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.99,
      "landmarks": [[x1,y1], [x2,y2], ...],
      "age": 25,
      "gender": 1,
      "embedding": [...]
    }
  ]
}
```

### POST /compare
Compara dos caras para determinar si son la misma persona.

**Request:**
```json
{
  "image1": "base64_encoded_image",
  "image2": "base64_encoded_image"
}
```

**Response:**
```json
{
  "similarity": 0.85,
  "is_same_person": true
}
```

## Despliegue Local

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build

# O construir manualmente
docker build -t insightface-api .
docker run -p 5000:5000 insightface-api
```

## Despliegue en Coolify

1. Conecta tu repositorio a Coolify
2. Configura el proyecto como "Docker Compose"
3. Coolify detectará automáticamente el `docker-compose.yml`
4. Despliega y listo

## Variables de Entorno

- `PORT`: Puerto donde correr la aplicación (default: 5000)

## Notas

- El modelo se descarga automáticamente en el primer uso
- Usa CPU por defecto (puedes modificar para GPU si está disponible)
- El umbral de similitud para comparación es 0.6 (ajustable en el código)