#!/bin/bash

# Configura tu dominio de Coolify aquí
BASE_URL="https://tu-dominio-coolify.com"

echo "🚀 Probando InsightFace API con curl..."
echo "📡 URL: $BASE_URL"
echo "----------------------------------------"

# Test de health check
echo "✅ Probando health check..."
curl -X GET "$BASE_URL/health" \
  -H "Content-Type: application/json" \
  --max-time 30

echo -e "\n\n"

# Test básico de detección (necesitarás una imagen en base64)
echo "📝 Para probar detección y comparación:"
echo "1. Convierte tu imagen a base64:"
echo "   base64 -i tu_imagen.jpg > imagen_base64.txt"
echo ""
echo "2. Prueba detección:"
echo "   curl -X POST \"$BASE_URL/detect\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"image\": \"'$(cat imagen_base64.txt)'\"}'"
echo ""
echo "3. Prueba comparación:"
echo "   curl -X POST \"$BASE_URL/compare\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"image1\": \"'$(cat imagen1_base64.txt)'\", \"image2\": \"'$(cat imagen2_base64.txt)'\"}'"