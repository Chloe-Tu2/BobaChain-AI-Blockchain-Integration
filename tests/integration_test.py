from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Integration test for the BobaChain application
def test_integration():
    # Test the API endpoint for retrieving batch information
    response = requests.get('http://localhost:5000/api/batch/1')
    assert response.status_code == 200
    assert 'name' in response.json()
    assert 'origin' in response.json()
    
    # Test the API endpoint for creating a new batch
    new_batch = {
        'name': 'Tapioca Pearls',
        'origin': 'Taiwan',
        'tracking_history': []
    }
    response = requests.post('http://localhost:5000/api/batch', json=new_batch)
    assert response.status_code == 201
    assert response.json()['name'] == new_batch['name']
    
    # Test the interaction with the blockchain
    response = requests.get('http://localhost:5000/api/blockchain/status')
    assert response.status_code == 200
    assert 'blockchain' in response.json()

if __name__ == '__main__':
    test_integration()