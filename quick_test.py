import requests
import time

URL = "https://face-recognition-insight-face.3150ox.easypanel.host"

def quick_test():
    print("🚀 Test rápido de la API...")
    
    try:
        # Test básico
        response = requests.get(f"{URL}/health", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API funcionando!")
            print(f"Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Contenido: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    for i in range(5):
        print(f"\n--- Intento {i+1} ---")
        if quick_test():
            break
        if i < 4:
            print("Esperando 30 segundos...")
            time.sleep(30)