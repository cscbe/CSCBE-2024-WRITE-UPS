import os
import hmac
import hashlib
from flask import Flask, render_template, request, url_for, redirect, flash, make_response, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from urllib.parse import quote_plus


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + '/var/www/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'f57def1301ccf067b1c0c70d12fe2c73'
secret_key = "yUXcOj8MXQp4UiGprgp1S+qrm4uU/oyWnL82SQ=="
flag = os.getenv('flag')


db = SQLAlchemy(app)

def logged(session) :
    if 'username' in session:
        return True
    else :
        return False

def verify_signature(amount, order_id, signature, secret_key):

    message = f"{amount}{order_id}".encode('utf-8')

    expected_signature = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected_signature, signature)

def get_currency() :
    currency = request.cookies.get('currency')
    if currency == "INR":
        return "INR"
    elif currency == "EUR":
        return "EUR"
    elif currency == "USD" :
        return "USD"
    elif currency == "GBP" :
        return "GBP"
    else :
        return "USD"

def convert_to_dollar_from_currency(currency, amount):
    if currency == "INR":
        dollars = amount / 82.85
        return str(round(dollars, 2))
    elif currency == "EUR":
        dollars = amount / 0.92
        return str(round(dollars, 2))
    elif currency == "GBP":
        dollars = amount / 0.79
        return str(round(dollars, 2))
    else:
        return str(round(amount, 2))
    
def convert_from_dollar_to_currency(currency, amount) :
    if currency == "INR":
        rupees = amount * 82.85
        return str(round(rupees,2))
    elif currency == "EUR" :
        eur = amount * 0.92
        return str(round(eur,2))
    elif currency == "GBP" :
        pound = amount * 0.79
        return str(round(pound,2))
    else : 
        return str(round(amount,2)) 


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





@app.errorhandler(404)
def defaultroute(e) :
      return redirect(url_for('home'))

@app.route('/home', methods=['GET'])
def home():
    if logged(session) == True :
        currency = get_currency()
        user = User.query.filter_by(username=session['username']).first()

        balance = convert_from_dollar_to_currency(currency=currency,amount=float(user.balance))

        if currency == "EUR":
            currency = "€"
        elif currency == "USD" :
            currency = "$"
        elif currency == "GBP" :
            currency = "£"
        elif currency == "INR" :
            currency = "₹"

        return render_template('index.html', auth=True, currency=currency,balance=balance)
    else :
        return render_template('index.html',auth=False)

@app.route('/login', methods=['GET','POST'])
def login():
    if logged(session) == True:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html')
    else :
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first() 
        db.session.commit()

        if not user or not check_password_hash(user.password, password):
            
            return render_template('login.html',incorrect_creds=True)
        else :
            session['username'] = username
            session['cart'] = []
            if 'currency' not in request.cookies: 
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('currency','USD')
                return resp
            else :
                return redirect(url_for('home'))
            
@app.route('/logout')
def logout():
    session.clear()
    session.modified=True

    resp = make_response(redirect(url_for('home')))
    return resp



@app.route('/register', methods=['GET', 'POST'])
def register():
    if logged(session) == True:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('register.html')
    else :
        username = request.form.get('username')
        password = request.form.get('password')
        
        if len(password) < 32:
            return render_template('register.html', existing_username=True, short_password=True)

        user = User.query.filter_by(username=username).first()

        if user: 
            return render_template('register.html', existing_username=True)
        else :
            new_user = User(username=username,password=generate_password_hash(password),balance=50.0)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/currency',methods=['POST'])
def setCurrenct():
    data = request.json
    currency = data.get("currency")
    resp = make_response("Currency sucessfully changed")
    
    if currency == "INR":
        resp.set_cookie('currency','INR')
    elif currency == "EUR":
        resp.set_cookie('currency','EUR')
    elif currency == "USD" :
        resp.set_cookie('currency','USD')
    elif currency == "GBP" :
        resp.set_cookie('currency','GBP')
    else :
        resp.set_cookie('currency','USD')
    
    return resp
    

@app.route('/shop')
def shop():
    auth = logged(session)
    items = Item.query.all()

    currency = get_currency()

    for item in items :
        price = convert_from_dollar_to_currency(currency,float(item.value))
        item.value = str(price)

    
    if auth == True :

        user = User.query.filter_by(username=session['username']).first()

        balance = convert_from_dollar_to_currency(currency=currency,amount=float(user.balance))

        if currency == "EUR":
            currency = "€"
        elif currency == "USD" :
            currency = "$"
        elif currency == "GBP" :
            currency = "£"
        elif currency == "INR" :
            currency = "₹"
        return render_template('shop.html',auth=auth,items=items,currency=currency,balance=balance)     

    else : 
        return render_template('shop.html',auth=auth,items=items,currency=currency) 
@app.route('/cart/add',methods=['POST'])
def addProduct():
    if logged(session) == False:
        return redirect(url_for('home'))
    if request.method == 'POST' :

        if not session['cart'] :
            session['cart'].append({'productId':int(request.form.get('productId')),'quantity':1})
        else :
            in_cart = False
            for item in session['cart'] :
                index = session['cart'].index(item)
                if item["productId"] == int(request.form.get('productId')) :
                    # Update quantity if product exists
                    session['cart'][index]['quantity'] += 1
                    in_cart = True
                    break
            if in_cart == False : 
                    session['cart'].append({'productId':int(request.form.get('productId')),'quantity':1})

        session.modified=True
        return redirect(url_for('shop'))

@app.route('/cart/remove',methods=['POST'])
def removeProduct():
    if logged(session) == False:
        return redirect(url_for('home'))
    if request.method == 'POST' :
        productId_to_remove = int(request.form.get('productId'))
        session['cart'] = [item for item in session['cart'] if item['productId'] != productId_to_remove]
        session.modified=True
        return redirect(url_for('cart'))
    
@app.route('/cart/update',methods=['POST'])
def updateCart() :
    if logged(session) == False:
        return redirect(url_for('home'))
    data = request.json
    productId = data.get("productId")
    quantity = data.get("quantity")
    if quantity < 1 :
        return "Quantity can't be smaller than 1"
    else :
        # Modify cart
        for item in session['cart'] :
            index = session['cart'].index(item)
            if item['productId'] == productId:
                session['cart'][index]['quantity'] = quantity
        session.modified = True
        resp = make_response(redirect(url_for('cart')))
        return resp

@app.route('/orders',methods=['GET'])
def get_orders():
    if logged(session) == False:
        return redirect(url_for('home'))
    orders = db.session.query(Order).filter_by(username=session['username'], status="confirmed").all()

    currency = get_currency()

    user = User.query.filter_by(username=session['username']).first()

    balance = convert_from_dollar_to_currency(currency=currency,amount=float(user.balance))
    if currency == "EUR":
        currency = "€"
    elif currency == "USD" :
        currency = "$"
    elif currency == "GBP" :
        currency = "£"
    elif currency == "INR" :
        currency = "₹"

    items = []
    names =[]
    for order in orders :
        items += db.session.query(Order_Item).filter_by(order_id=order.id).all()
    
    for item in items :
        product = db.session.query(Item).filter_by(id=item.product_id).first()

        if product.id == 8 :
            name = flag
            names.append({'name':name,'quantity':item.quantity})
        else :
            names.append({'name':product.name,'quantity':item.quantity})


    return render_template('orders.html',items=names,currency=currency,balance=balance)



@app.route('/order',methods=['POST'])
def create_order() :
    if logged(session) == False:
        return redirect(url_for('home'))
    username = session['username']
    total_price = 0

    for item in session['cart'] :
        product_id = item['productId']  
        quantity = item['quantity']
        product = Item.query.get(product_id)
        if product is None:
            return "Invalid product id"

        price = float(product.value) * int(quantity)
        currency = get_currency()
        total_price += float(convert_from_dollar_to_currency(currency,price))

    order = Order(username=username, status="pending", totalPrice=total_price)
    db.session.add(order)
    db.session.commit()
        
    for item in session['cart']:
        product_id = item['productId']
        quantity = item['quantity']
        order_item = Order_Item(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_item)
    
    db.session.commit()

    amount = str(total_price)
    orderId = str(order.id)

    message = f"{total_price}{order.id}".encode('utf-8')
    signature = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()


    return redirect(url_for('pay',amount=quote_plus(amount), orderId=quote_plus(orderId),signature=quote_plus(signature)))


@app.route('/pay',methods=['GET'])
def pay():
    if logged(session) == False:
        return redirect(url_for('home'))
    orderId = request.args.get("orderId")
    amount = request.args.get("amount")
    signature = request.args.get("signature")
    currency = get_currency()
    user = User.query.filter_by(username=session['username']).first()

    amount_to_pay = convert_to_dollar_from_currency(currency,float(amount)) # convert amount to dollar


    if not verify_signature(amount,orderId,signature,secret_key) :
        return "Invalid Signature"
    else :
        if float(user.balance) < float(amount_to_pay) :
            return "Insufficient balance"
        else :
            order = db.session.query(Order).filter(Order.id == orderId).first()

            if order.username != session['username'] :
                return 'Forbidden'

            order.status = "confirmed"

            user = db.session.query(User).filter_by(username=session['username']).first()

            user.balance -= float(convert_to_dollar_from_currency(currency=currency,amount=float(amount)))
            db.session.commit()
            session['cart'] = []
            session.modified = True
            
            return redirect(url_for('get_orders'))

    


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if logged(session) == False:
        return redirect(url_for('home'))
    
    if request.method == 'GET' :
        items = []
        total_price = 0 
        for item in session['cart'] :
            product =  Item.query.filter_by(id=item['productId']).first()
            items.append({'name':product.name,'id':item['productId'],'price':product.value,'description':product.description,'quantity':item['quantity']})

            total_price += float(product.value) * int(item['quantity'])

        currency = get_currency()

        user = User.query.filter_by(username=session['username']).first()

        balance = convert_from_dollar_to_currency(currency=currency,amount=float(user.balance))

        total_price = convert_from_dollar_to_currency(currency,total_price)

        if currency == "EUR":
            currency = "€"
        elif currency == "USD" :
            currency = "$"
        elif currency == "GBP" :
            currency = "£"
        elif currency == "INR" :
            currency = "₹"

        return render_template('cart.html',items=items,price=total_price,currency=currency,balance=balance)



if __name__ == "__main__":
    app.run(debug=False)