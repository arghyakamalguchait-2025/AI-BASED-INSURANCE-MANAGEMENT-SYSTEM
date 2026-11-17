class ConversationManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                'history': [],
                'pending': None,
            }
        return self.sessions[user_id]

    def add_message(self, user_id, role, content):
        session = self.get_session(user_id)
        session['history'].append({'role': role, 'content': content})
        if len(session['history']) > 12:
            session['history'] = session['history'][-12:]

    def clear_session(self, user_id):
        self.sessions.pop(user_id, None)


conversation_manager = ConversationManager()
