from flask import Flask, render_template, Blueprint, current_app
from models import Message

routes_bp = Blueprint('Routes', __name__)

@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@routes_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    message_model = Message(current_app.config['MESSAGE_TABLE'])
    
    chat_history = message_model.get_messages()
    return render_template('chat.html', chat_history=chat_history)

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')