from flask import Flask, request, send_file, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "API com Flask funcionando!"})

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    texto = data.get("text", "")
    voz = data.get("voice", "pt-br-voice.onnx")

    if not texto:
        return jsonify({"erro": "Texto não fornecido"}), 400

    # Gera nome de arquivo único
    output_id = str(uuid.uuid4())
    output_path = f"static/outputs/{output_id}.wav"

    # Chama o Piper via subprocess
    comando = [
        "./piper/piper",
        "--model", f"voices/{voz}",
        "--output_file", output_path
    ]

    try:
        processo = subprocess.run(comando, input=texto.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if processo.returncode != 0:
            return jsonify({"erro": processo.stderr.decode()}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    # Retorna o arquivo de áudio
    return send_file(output_path, mimetype="audio/wav")


