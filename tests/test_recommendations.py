def test_recommendations(client):
    response = client.post('/recommendations', data={
        'age': 24,
        'insurance_category': 'Health Insurance',
        'monthly_budget': 2000,
        'coverage_preference': 'Standard',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'AI Recommendations' in response.data or b'Recommended Plan' in response.data
