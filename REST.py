from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

app = Flask(__name__) #creates a flask application object in python module

@app.route("/home", methods=["GET"]) #used to define a route or URL endpoint for a specfic function or view
def home():
    return "sheheryar tayyabi"



db = SQLAlchemy() #creates an instance of SQLAlchemy class, which represents the database connection and provides functionality for interacting with the database
ma = Marshmallow() 
mysql = MySQL(app)

class Product(db.Model): #defines a class named 'Product' that is derived from the 'db.model' class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(10), nullable=False)

    def __init__(self,name,price,category): #constructor method in a Python Class. It's when an object of that class is created
        self.name=name
        self.price=price
        self.category=category


class ProductSchema(ma.Schema): #defines a schema or blueprint for serializing and deserializing instances of the product class 
    class Meta:
        fields = ("id", "name", "price", "category")


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/product" #used to configure the URI (Uniform Resource Identifier) or connection string for connecting to a MySQL database using SQLAlchemy
db.init_app(app)
with app.app_context():# statement is used in Flask applications to create a context within which the application's resources and extensions are available. 
    db.create_all()

@app.route("/product/add", methods=["POST"]) #is a decorator used in Flask web applications to define a route or URL endpoint that handles HTTP POST requests for adding a product.
def add_product():
    _json = request.json
    name = _json['name']
    price = _json['price']
    category = _json['category']
    new_product = Product(name=name, price=price, category=category)
    db.session.add(new_product)
    db.session.commit() #save any pending changes made to the database, typically done after performing database operations such as; adding, updating, or deleting data
    return jsonify({"Message": "Your product has been added"})

    

@app.route("/product", methods=["GET"]) #the function or view 
def get_product(): 
    products = []
    data = Product.query.all()
    products = products_schema.dump(data)
    return jsonify(products)



@app.route("/product/<id>", methods=["GET"])
def product_byid(id):
        if str.isdigit(id) == False:
            return jsonify(f"Message: the id of the product cannot be a string")
        else:
            data = []
            product = Product.query.get(id)
            if product is None:
                return jsonify(f"No product was found")
            data = product_schema.dump(product)
            return jsonify(data)
        

@app.route("/product/delete/<id>", methods=['POST'])
def delete_product_byid(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify (f"The product has been deleted")




           


 
if __name__ == "__main__": #construct is used to check if a script is being run directly as the main entry point of the program
    app.run(debug=True)     