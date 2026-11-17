def test_chatbot_fallback(client):
    response = client.post('/api/chatbot', json={'message': 'What is health insurance?'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'reply' in data
    assert 'health' in data['reply'].lower()
