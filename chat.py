from flask import Flask, current_app, render_template, url_for, request, redirect, Blueprint
from models import Message

chat_bp = Blueprint('ChatBP', __name__)

@chat_bp.route("/chatHandle", methods=['GET', 'POST'])
def chatHandle():
    message_model = Message(current_app.config['MESSAGE_TABLE'])
    
    if request.method == 'POST':
        message_content = request.form['message']
        message_model.put_message(sender="User", content=message_content)
        print("Data lisätty")
        return redirect('/chat')