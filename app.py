from flask import Flask, jsonify, request
import json
from functions import todo_producto, producto_acortado

app = Flask(__name__)


@app.route('/mercadoLibre', methods=['GET'])
def mercadoLibre():
    data=json.loads(request.data)
    if "limite" not in data:
        titulo,precios,urls = todo_producto(data['producto'])
    else:
        titulo,precios,urls = producto_acortado(data['producto'], data['limite'])
    return jsonify({"Datos":{'Titulos':titulo, 'Precios':precios, 'Urls':urls}})




if __name__=="__main__":
    app.run(host = "0.0.0.0", debug=True)