import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "productos.db"

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

# Inicializar la base de datos
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Llamamos a la inicialización al arrancar
init_db()

@app.route('/api/productos', methods=['POST'])
def create_producto():
    datos = request.get_json()

    # Caso 2: Validación de datos incompletos (Falta 'nombre' o 'precio')
    if not datos or 'nombre' not in datos or 'precio' not in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    nombre = datos['nombre']
    precio = datos['precio']

    # Caso 3: Validación de tipos de datos (Ej. precio: "ABC")
    if not isinstance(precio, (int, float)):
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO producto (nombre, precio) VALUES (?, ?)', (nombre, precio))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": nuevo_id, "nombre": nombre, "precio": precio}), 201 # 201 Created

@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in productos]), 200

# Caso 1: Validación de recursos inexistentes
@app.route('/api/productos/<int:id>', methods=['GET'])
def get_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    conn.close()

    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404 # 404 Not Found

    return jsonify(dict(producto)), 200

@app.route('/api/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'precio' not in datos:
        return jsonify({"error": "Faltan campos"}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE producto SET nombre = ?, precio = ? WHERE id = ?', 
                (datos['nombre'], datos['precio'], id))
    conn.commit()
    filas_modificadas = cursor.rowcount
    conn.close()

    if filas_modificadas == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto actualizado"}), 200

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    filas_eliminadas = cursor.rowcount
    conn.close()

    if filas_eliminadas == 0:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({"mensaje": "Producto eliminado"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')