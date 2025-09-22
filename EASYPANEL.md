# InsightFace API - Despliegue en EasyPanel

## Configuración para EasyPanel

### 1. Crear el Proyecto

1. Ve a tu panel de EasyPanel
2. Crea un nuevo proyecto llamado `face_recognition`
3. Agrega un nuevo servicio llamado `insight-face`

### 2. Configuración del Servicio

**Tipo de Servicio:** App  
**Fuente:** GitHub Repository  
**Repositorio:** `https://github.com/mausoftSistemas/recognition.git`  
**Branch:** `main`  
**Build Path:** `/` (raíz del proyecto)  

### 3. Configuración de Red

- **Puerto Interno:** 5000
- **Dominio:** EasyPanel generará automáticamente un dominio
- **HTTPS:** Habilitado automáticamente

### 4. Variables de Entorno

```
PORT=5000
PYTHONUNBUFFERED=1
```

### 5. Volúmenes (Opcional)

Para persistir los modelos descargados:
- **Nombre:** `models_data`
- **Ruta:** `/root/.insightface/models`

### 6. Health Check

EasyPanel detectará automáticamente el health check configurado en el docker-compose.yml:
- **Endpoint:** `/health`
- **Intervalo:** 30s
- **Timeout:** 10s

## Endpoints de la API

Una vez desplegado, tu API estará disponible en el dominio generado por EasyPanel:

### GET /health
```bash
curl https://tu-dominio.easypanel.host/health
```

### POST /detect
```bash
curl -X POST https://tu-dominio.easypanel.host/detect \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

### POST /compare
```bash
curl -X POST https://tu-dominio.easypanel.host/compare \
  -H "Content-Type: application/json" \
  -d '{"image1": "base64_1", "image2": "base64_2"}'
```

## Pruebas

Usa el script `test_api.py` incluido:

```bash
python test_api.py
```

Cuando te pida la URL, ingresa tu dominio de EasyPanel.

## Notas Importantes

- El primer despliegue puede tardar varios minutos debido a la descarga de modelos
- Los modelos se descargan automáticamente en el primer uso
- El servicio usa CPU por defecto (modificable para GPU si está disponible)
- EasyPanel maneja automáticamente SSL/HTTPS y el balanceador de carga

## Troubleshooting

### Error "429 Too Many Requests" de Docker Hub

✅ **SOLUCIONADO**: El proyecto ahora usa GitHub Container Registry (`ghcr.io`) para evitar el rate limiting de Docker Hub.

**Configuración actual:**
- Usa `ghcr.io/linuxserver/baseimage-ubuntu:focal`
- Instala Python y dependencias en runtime
- Sin límites de descarga
- Primer inicio toma ~5 minutos (instalación completa)

**Si aún tienes problemas, alternativas disponibles:**

1. **Quay.io**: Copia el contenido de `docker-compose.quay.yml` a `docker-compose.yml`
2. **GitLab Registry**: Copia el contenido de `docker-compose.alpine.yml` a `docker-compose.yml`

**Para cambiar la configuración:**
```bash
# Opción 1: GitHub Container Registry (actual)
cp docker-compose.yml docker-compose.yml

# Opción 2: Quay.io
cp docker-compose.quay.yml docker-compose.yml

# Opción 3: GitLab Registry  
cp docker-compose.alpine.yml docker-compose.yml
```

### Otros problemas

Si el servicio no inicia:
1. Revisa los logs en EasyPanel
2. Verifica que el health check esté pasando
3. Asegúrate de que el puerto 5000 esté configurado correctamente
4. El primer despliegue puede tardar 5-10 minutos descargando modelos