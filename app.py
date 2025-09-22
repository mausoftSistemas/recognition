from flask import Flask, request, jsonify
import insightface
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

# Inicializar el modelo de InsightFace
model = None

def init_model():
    global model
    try:
        model = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
        model.prepare(ctx_id=0, det_size=(640, 640))
        print("Modelo InsightFace inicializado correctamente")
    except Exception as e:
        print(f"Error inicializando modelo: {e}")

def base64_to_image(base64_string):
    """Convierte base64 a imagen numpy array"""
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def image_to_base64(image):
    """Convierte imagen numpy array a base64"""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/detect', methods=['POST'])
def detect_faces():
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        # Convertir base64 a imagen
        image = base64_to_image(data['image'])
        
        # Detectar caras
        faces = model.get(image)
        
        results = []
        for face in faces:
            result = {
                "bbox": face.bbox.tolist(),
                "confidence": float(face.det_score),
                "landmarks": face.kps.tolist(),
                "age": int(face.age) if hasattr(face, 'age') else None,
                "gender": int(face.gender) if hasattr(face, 'gender') else None,
                "embedding": face.embedding.tolist() if hasattr(face, 'embedding') else None
            }
            results.append(result)
        
        return jsonify({
            "faces_detected": len(results),
            "faces": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_faces():
    try:
        data = request.get_json()
        
        if 'image1' not in data or 'image2' not in data:
            return jsonify({"error": "Two images required"}), 400
        
        # Procesar ambas imágenes
        img1 = base64_to_image(data['image1'])
        img2 = base64_to_image(data['image2'])
        
        faces1 = model.get(img1)
        faces2 = model.get(img2)
        
        if len(faces1) == 0 or len(faces2) == 0:
            return jsonify({"error": "No faces detected in one or both images"}), 400
        
        # Comparar la primera cara de cada imagen
        embedding1 = faces1[0].embedding
        embedding2 = faces2[0].embedding
        
        # Calcular similitud coseno
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        
        return jsonify({
            "similarity": float(similarity),
            "is_same_person": similarity > 0.6  # Umbral ajustable
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_model()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)