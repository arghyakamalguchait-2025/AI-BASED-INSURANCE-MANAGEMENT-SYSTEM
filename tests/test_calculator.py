def test_calculator(client):
    response = client.post('/calculator', data={
        'insurance_type': 'Health Insurance',
        'age': 30,
        'coverage_amount': 500000,
        'duration': 5,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Estimated Premium' in response.data
