import os
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'f57def1301ccf067b1c0c70d12fe2c73'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)

class Order_Item(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)

class Order(db.Model) :
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String, unique=False, nullable=False)
    status = db.Column(db.String(10),nullable=False)
    totalPrice = db.Column(db.Integer,nullable=True)
    items = db.relationship('Order_Item', backref='order', lazy=True)

with app.app_context():
    db.create_all()

    ids = [1,2,3,4,5,6,7,8,9]
    names = ['Realistic NPC doll','Tux doll','Android doll','Orangina','JTX 7077','AC Milan jersey','Vape','Bugatti sparkling water','Oignon cream potato chips']
    values = [10.99,19.99,19.99,1.99,541.99,49.99,15.99,1500.0,7.99]
    descriptions = ['A realistic doll of a Minecraft NPC, do whatever you want with his nose.','A cuddly and adorable tribute to the Linux penguin mascot, perfect for Linux enthusiasts and open-source aficionados.','An Android doll from the Android Dev Summit','It appears that the recipe of this fabulous drink comes from Algeria.','Jay Tracing GPU, use it in your computer or eat it with a bit of pepper','A 100% legit jersey from the football club AC Milan','The vape has been used, just be cautious as we don\'t know what the previous owner did with it.','Non-carbonated water is for poor people, because you can get it direclty from the tap. Rich poeple drink sparkling water.','The Best potato chips variety on Earth.']
    images = ['villager.jpg','tux.png','android.png','orangina.png','gpu.png','acmilan.png','vape.png','water.png','potatochips.png',]

    for i in range(len(ids)):
        # Create a new product instance for each product
        product = Item(name=names[i], value=values[i], description=descriptions[i], image=images[i])
        # Add the product to the session
        db.session.add(product)

    # Commit the session to write the changes to the database
    db.session.commit()

