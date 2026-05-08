from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

#Asigno los productos de ropa
productos = [
    {"id": 1, "nombre": "Remera basica", "precio": 5000},
    {"id": 2, "nombre": "Pantalon jean", "precio": 15000},
    {"id": 3, "nombre": "Buzo", "precio": 12000},
    {"id": 4, "nombre": "Campera", "precio": 20000},
    {"id": 5, "nombre": "Zapatillas urbanas", "precio": 30000},
    {"id": 6, "nombre": "Traje", "precio": 40000}
]

carrito = []

#Aca se lsitan los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    """
    Lista todos los productos.
    ---
    tags:
      - Productos
    responses:
      200:
        description: Lista de productos de la tienda de ropa
    """
    return jsonify(productos)


#Agregar al carrito
@app.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    """
    Agrega un producto al carrito.
    ---
    tags:
      - Carrito
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
    responses:
      200:
        description: Producto agregado correctamente.
      404:
        description: Producto no encontrado.
    """
    data = request.get_json()
    id_producto = data.get("id")

    producto = next((p for p in productos if p["id"] == id_producto), None)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    carrito.append(producto)

    return jsonify({
        "mensaje": "Producto agregado al carrito",
        "carrito": carrito
    })


#Metodo para eliminar productos del carrito
@app.route('/carrito/<int:id>', methods=['DELETE'])
def eliminar_del_carrito(id):
    """
    Elimina un producto del carrito.
    ---
    tags:
      - Carrito
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar.
        example: 1
    responses:
      200:
        description: Producto eliminado correctamente.
    """
    global carrito
    carrito = [p for p in carrito if p["id"] != id]

    return jsonify({
        "mensaje": "Producto eliminado",
        "carrito": carrito
    })


#Se calcula el total del carrito
@app.route('/carrito/total', methods=['GET'])
def calcular_total():
    """
    Calcula el total del carrito.
    ---
    tags:
      - Carrito
    responses:
      200:
        description: Total calculado.
    """
    total = sum(p["precio"] for p in carrito)

    return jsonify({
        "total": total
    })


#Ejecuta
if __name__ == '__main__':
    app.run(debug=True)