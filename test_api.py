import requests
import base64
import json
from PIL import Image
import io

# Configura aquí tu dominio de EasyPanel
BASE_URL = "https://tu-dominio.easypanel.host"  # Reemplaza con tu dominio real

def create_test_image():
    """Crea una imagen de prueba simple"""
    img = Image.new('RGB', (200, 200), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def image_to_base64(image_path):
    """Convierte una imagen a base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_health(base_url):
    """Test del endpoint de health"""
    try:
        response = requests.get(f'{base_url}/health', timeout=30)
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_detect_with_sample(base_url):
    """Test del endpoint de detección con imagen de muestra"""
    try:
        # Crear imagen de prueba
        test_image = create_test_image()
        
        payload = {
            "image": test_image
        }
        
        response = requests.post(f'{base_url}/detect', json=payload, timeout=60)
        print(f"✅ Detection test: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
        return False

def test_detect(base_url, image_path):
    """Test del endpoint de detección con imagen real"""
    try:
        image_b64 = image_to_base64(image_path)
        
        payload = {
            "image": image_b64
        }
        
        response = requests.post(f'{base_url}/detect', json=payload, timeout=60)
        print(f"✅ Detection result: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Detection failed: {e}")
        return False

def test_compare_with_samples(base_url):
    """Test del endpoint de comparación con imágenes de muestra"""
    try:
        # Crear dos imágenes de prueba diferentes
        test_image1 = create_test_image()
        
        img2 = Image.new('RGB', (200, 200), color='blue')
        buffer2 = io.BytesIO()
        img2.save(buffer2, format='JPEG')
        test_image2 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        
        payload = {
            "image1": test_image1,
            "image2": test_image2
        }
        
        response = requests.post(f'{base_url}/compare', json=payload, timeout=60)
        print(f"✅ Comparison test: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        return False

def test_compare(base_url, image1_path, image2_path):
    """Test del endpoint de comparación con imágenes reales"""
    try:
        image1_b64 = image_to_base64(image1_path)
        image2_b64 = image_to_base64(image2_path)
        
        payload = {
            "image1": image1_b64,
            "image2": image2_b64
        }
        
        response = requests.post(f'{base_url}/compare', json=payload, timeout=60)
        print(f"✅ Comparison result: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        return False

def main():
    print("🚀 Probando InsightFace API...")
    print(f"📡 URL base: {BASE_URL}")
    print("-" * 50)
    
    # Test básico de salud
    if not test_health(BASE_URL):
        print("❌ El servicio no está disponible. Verifica la URL y el despliegue.")
        return
    
    # Tests con imágenes de muestra
    print("\n🖼️  Probando con imágenes de muestra...")
    test_detect_with_sample(BASE_URL)
    test_compare_with_samples(BASE_URL)
    
    print("\n📝 Para probar con tus propias imágenes:")
    print("1. Coloca tus imágenes en el directorio actual")
    print("2. Descomenta las líneas al final del script")
    print("3. Ajusta las rutas de las imágenes")

if __name__ == "__main__":
    # ⚠️  IMPORTANTE: Reemplaza esta URL con tu dominio real de EasyPanel
    BASE_URL = input("Ingresa tu dominio de EasyPanel (ej: https://tu-app.easypanel.host): ").strip()
    
    if not BASE_URL:
        print("❌ Debes ingresar la URL de tu aplicación")
        exit(1)
    
    main()
    
    # 🔧 Descomenta estas líneas para probar con imágenes reales:
    # print("\n🖼️  Probando con imágenes reales...")
    # test_detect(BASE_URL, "tu_imagen.jpg")
    # test_compare(BASE_URL, "imagen1.jpg", "imagen2.jpg")