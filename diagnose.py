import requests
import time
import sys

BASE_URL = "https://face-recognition-insight-face.3150ox.easypanel.host"

def test_connection():
    """Test básico de conectividad"""
    print("🔍 Probando conectividad básica...")
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ Respuesta del servidor: {response.status_code}")
        print(f"📄 Contenido: {response.text[:200]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - El servicio no está disponible")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servicio está tardando mucho en responder")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_health():
    """Test del endpoint de health"""
    print("\n🏥 Probando endpoint /health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📊 Respuesta JSON: {data}")
                return True
            except:
                print(f"⚠️  Respuesta no es JSON: {response.text}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Contenido: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def wait_for_service(max_wait=600):  # 10 minutos máximo
    """Espera a que el servicio esté disponible"""
    print(f"\n⏳ Esperando a que el servicio esté disponible (máximo {max_wait//60} minutos)...")
    
    start_time = time.time()
    attempt = 1
    
    while time.time() - start_time < max_wait:
        print(f"\n🔄 Intento {attempt} - {int(time.time() - start_time)}s transcurridos")
        
        if test_connection():
            if test_health():
                print("🎉 ¡Servicio disponible!")
                return True
        
        print("⏸️  Esperando 30 segundos antes del siguiente intento...")
        time.sleep(30)
        attempt += 1
    
    print("❌ Timeout: El servicio no estuvo disponible en el tiempo esperado")
    return False

def main():
    print("🚀 Diagnóstico de InsightFace API")
    print(f"🌐 URL: {BASE_URL}")
    print("=" * 60)
    
    # Test inicial
    if test_connection():
        if test_health():
            print("\n✅ ¡El servicio está funcionando correctamente!")
            return
    
    # Si no funciona, esperar
    print("\n⚠️  El servicio no está disponible aún.")
    print("💡 Esto es normal en el primer despliegue (instalación de dependencias)")
    
    if input("\n¿Quieres esperar a que esté disponible? (y/n): ").lower() == 'y':
        wait_for_service()
    else:
        print("\n📋 Recomendaciones:")
        print("1. Revisa los logs en EasyPanel")
        print("2. El primer despliegue puede tardar 5-10 minutos")
        print("3. Vuelve a ejecutar este script en unos minutos")

if __name__ == "__main__":
    main()