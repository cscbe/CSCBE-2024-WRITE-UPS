from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
import jwt
import re
import requests

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db.init_app(app)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True) 
    content = db.Column(db.String(512), nullable=False)

    def json(self):
        return {'id': self.id,'content': self.content} 
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/message', methods=['POST'])
def generate_response():
    message = request.json.get('message')
    if len(message) > 255:
        return 'Your message is too long ! Stop hacking !'
    response = requests.post('http://llamacpp:8081/completion', json={'prompt': '[INST] ' + message + ' [/INST]',
                                                                      "n_predict": 5, "temperature": 0.3})
    pattern = re.compile(r'\bSAFE(?:\.)?\b')
    if response.status_code == 200:
        if pattern.search(response.json().get('content')):
            new_message = Message(content=message)
            db.session.add(new_message)
            db.session.commit()
            return 'Your message has been sent to the admin !'
        else:
            return 'Your message was not safe ! Stop hacking !'
    else:
        return 'My AI assistant is having trouble right now !'

@app.route('/admin', methods=['GET'])
def dashboard():
    if request.cookies.get('Cookie') is None:
        return 'You are not an admin !'
    user = jwt.decode(request.cookies.get('Cookie'), environ.get('SECRET'), algorithms=["HS256"])
    if user.get('username') != 'admin':
        return 'You are not an admin !'
    messages = Message.query.all()
    Message.query.delete()
    db.session.commit()
    return render_template('admin.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)