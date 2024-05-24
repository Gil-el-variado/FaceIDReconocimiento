from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

def obtener_bytes_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        return imagen.read()

def comparar_rostros(bytes_1, bytes_2):
    cliente = boto3.client('rekognition')

    try:
        respuesta = cliente.compare_faces(
            SourceImage={'Bytes': bytes_1},
            TargetImage={'Bytes': bytes_2},
            SimilarityThreshold=60,
            QualityFilter='NONE'
        )
        
        if respuesta and respuesta['ResponseMetadata']['HTTPStatusCode'] == 200:
            if respuesta['FaceMatches']:
                return "Los rostros son similares. Similitud: {}%".format(respuesta['FaceMatches'][0]['Similarity'])
            else:
                return "Los rostros no son similares."
        
    except ClientError as error:
        return "Ocurrió un error al llamar a la API de Rekognition: {}".format(str(error))

@app.route('/')
def index():
    return '¡Bienvenido al servidor de comparación de rostros!'

@app.route('/compare-faces', methods=['POST'])
def compare_faces():
    image1 = request.files['image1'].read()
    image2 = request.files['image2'].read()

    result = comparar_rostros(image1, image2)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
