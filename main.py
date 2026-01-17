import os
from flask import Flask, request, jsonify
from pocketoptionapi.stable_api import PocketOptionAPI

app = Flask(__name__)

# --- CONFIGURAÇÃO DA PONTE ---
# Usei o código que começa com A_ da sua foto
SSID = "A_OEQ0BLQUmg239qW" 
api = PocketOptionAPI(SSID)

@app.route('/')
def home():
    return "Ponte Online!"

@app.route('/executar', methods=['POST'])
def executar_ordem():
    dados = request.json
    ativo = dados.get('ativo', 'EURUSD_otc')
    valor = dados.get('valor', 1)
    direcao = dados.get('direcao') # 'call' ou 'put'
    tempo = dados.get('tempo', 60)

    check, reason = api.connect()
    if check:
        # Comando que envia a ordem para a Pocket Option
        id_ordem = api.buy_order(ativo, valor, direcao, tempo)
        return jsonify({"status": "sucesso", "id": id_ordem})
    else:
        return jsonify({"status": "erro", "motivo": reason}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
