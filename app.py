from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "API com Flask funcionando!"})

# Adicione outras rotas aqui no futuro, como uma rota /tts para gerar áudio
