# from flask import Flask, render_template, jsonify, request, redirect, send_from_directory, url_for, flash
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Se crea la app
app = Flask(__name__)

# Se guarda en el SO la existencia de la carpeta, se le info a la app
# CARPETA = os.path.join('uploads')
# app.config['CARPETA'] = CARPETA

# Permite el acceso del FrontEnd a las rutas de la app
CORS(app)

# Configuración a la base de datos                     //User - Pass - Local Host - Nombre BD
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1:3307/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



# Se crean 2 objetos
# Permite manipular la BD de la app
db = SQLAlchemy(app)
# Permite acceder a la aplicación y va a dar herramientas para converitr datos completos (json) a objetos
ma = Marshmallow(app)

# Se define la clase Producto (Es una estructura de la tabla de una BD)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))
    
    # Definir e iniciar el constructor
    def __init__(self, nombre, precio, stock, imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen



# código para cear las tablas
with app.app_context():
    db.create_all()

# Se crea la clase que permite acceder a los métodos de conversión de datos
class ProductoSchema(ma.Schema): # Se puede poner cualquier nombre no solo "ProductoSchema"
    # ProductoSchema -- Hereda del objeto Marshmallow una herramienta que se llama Schema
    class Meta:
        fields = ("id", "nombre", "precio", "stock", "imagen")


# Se crean 2 objetos que se usan cuando se quiere convertir un JSON o un listado de JSON
producto_schema = ProductoSchema()   # singular - un solo JSON
productos_schema = ProductoSchema(many=True)  # plural - listado de JSON


# Creación de rutas (5 en total)

# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
# '/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET
# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
# '/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT


# ENDPOINT ó ruta
@app.route("/productos", methods=['GET'])
def get_productos():
    # Se consulta toda la info de la tabla producto
    all_productos = Producto.query.all()
    
    return productos_schema.jsonify(all_productos)


# Esta ruta crea un nuevo registro en la tabla
@app.route("/productos", methods=['POST'])
def create_producto():
    
#     Ejemplo de entrada de datos
#     {
#       "imagen": "https://picsum.photos/200/300?grayscale",
#       "nombre": "MICROONDAS",
#       "precio": 50000,
#       "stock": 10
#      }

    nombre = request.json['nombre']
    precio =request.json['precio'] 
    stock =request.json['stock'] 
    imagen = request.json['imagen']
    #-------------------------------- foto = request.files['fileFoto']---------------------------
    
    # Persistencia en BD con SQLAlchemy
    # ----------------------new_producto = Producto(nombre, precio, stock, foto) -------------------# Almacena
    new_producto = Producto(nombre, precio, stock, imagen) # Almacena
    db.session.add(new_producto) # Agrega
    db.session.commit()# Guarda
    
    return producto_schema.jsonify(new_producto)

    

# Este Endpoint muestra el producto por id
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    # Consulta por id a la clase Producto a través de una query
    producto=Producto.query.get(id)
    
    # Retorna el JSON de un objeto que recibió como parámetro y lo convierte
    return producto_schema.jsonify(producto)  

# Controlador para borrar
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()
    return redirect('/productos')


# Controlador para MODIFICAR
@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)

    #  Recibir los datos a modificar
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']

    # Del objeto resultante de la consulta modificar los valores  
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    producto.imagen=imagen
    #  Guardar los cambios
    db.session.commit()
    # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return producto_schema.jsonify(producto)

# Mostrar la foto
# @app.route('/uploads/<fileFoto>')
# def uploads(fileFoto):
#     return send_from_directory(app.config['CARPETA'], fileFoto)


# Bloque principal del programa
if __name__== "__main__":
    app.run(debug=True)