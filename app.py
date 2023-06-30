import flask
from flask import request, json, jsonify, render_template
from flask_mysqldb import MySQL


app = flask.Flask (__name__)


app.config["DEBUG"]= True 
@app.route('/home', methods=['GET'])
def welcome():
    return("Sheheryar Tayyabi")

@app.route("/shiest")
def shiest():
    return helper.something()





if __name__ == '__main__':
    app.run(debug='True')