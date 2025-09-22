import requests
import base64
import json

def image_to_base64(image_path):
    """Convierte una imagen a base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_health():
    """Test del endpoint de health"""
    response = requests.get('http://localhost:5000/health')
    print("Health check:", response.json())

def test_detect(image_path):
    """Test del endpoint de detección"""
    image_b64 = image_to_base64(image_path)
    
    payload = {
        "image": image_b64
    }
    
    response = requests.post('http://localhost:5000/detect', json=payload)
    print("Detection result:", response.json())

def test_compare(image1_path, image2_path):
    """Test del endpoint de comparación"""
    image1_b64 = image_to_base64(image1_path)
    image2_b64 = image_to_base64(image2_path)
    
    payload = {
        "image1": image1_b64,
        "image2": image2_b64
    }
    
    response = requests.post('http://localhost:5000/compare', json=payload)
    print("Comparison result:", response.json())

if __name__ == "__main__":
    # Ejecutar tests
    test_health()
    
    # Descomenta y ajusta las rutas para probar con imágenes reales
    # test_detect("path/to/your/image.jpg")
    # test_compare("path/to/image1.jpg", "path/to/image2.jpg")