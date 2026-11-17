from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from ai.chatbot import rule_based_response
from ai.intent_detector import detect_intent
from ai.ollama_client import chat_with_ollama
from ai.conversation_manager import conversation_manager

chatbot_bp = Blueprint('chatbot', __name__)


def get_chat_history(user_id):
    session_data = conversation_manager.get_session(user_id)
    return session_data.get('history', [])


@chatbot_bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@chatbot_bp.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({'reply': 'Please enter a message for InsureBot AI.'}), 400

    user_id = getattr(current_user, 'id', 'guest') if current_user.is_authenticated else 'guest'

    intent = detect_intent(message)
    response = rule_based_response(message, intent=intent)

    try:
        model = 'qwen2.5-coder:3b'
        messages = [
            {'role': 'system', 'content': 'You are InsureBot AI. Answer insurance questions using fictional demonstration data only.'},
            {'role': 'user', 'content': message},
        ]
        generated, err = chat_with_ollama(messages, model=model)
        if generated and not err:
            response = generated
    except Exception:
        response = response

    conversation_manager.add_message(user_id, 'user', message)
    conversation_manager.add_message(user_id, 'assistant', response)
    return jsonify({'reply': response, 'timestamp': datetime.utcnow().strftime('%H:%M')})
