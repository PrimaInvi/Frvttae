from flask import Flask, request, redirect, render_template, send_from_directory
from pymongo import MongoClient
import re

app = Flask(__name__)

client = MongoClient("mongodb+srv://danielak892:2005@frvttae.krihlms.mongodb.net/")
db = client["frvttae"]
users_collection = db["users"]
users_collection.create_index("email", unique=True)

@app.route('/img/<path:filename>')
def custom_static_img(filename):
    return send_from_directory('img', filename)


@app.route("/", methods=["POST"])
def register():
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if not re.match(email_regex, email):
        return "Correo electrónico inválido"

    if password != confirm_password:
        return "Las contraseñas no coinciden"
    
    if users_collection.find_one({"email": email}):
        return "El correo electrónico ya esta registrado"
    
    users_collection.insert_one({
        "email": email,
        "username": username,
        "password": password
    })

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
