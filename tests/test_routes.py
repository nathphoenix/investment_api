from flask import Flask, request
import json
from ..views.views import configure_routes
#from . import app, client

# def call_client(request):
#     app.testing = True
#     client = app.test_client()
#     return client



def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/pytesting'

    response = client.get(url)
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200
    
    
def test_form():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/test3'

    response = client.get(url)
    assert response.get_data() == b"home welcome"
    assert response.status_code == 200



def test_post_route__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200


def test_post_route__failure__unauthorized():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    mock_request_headers = {}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401


def test_post_route__failure__bad_request():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/post/test'

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {}

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400
    
    
    

def registration_test():
        app = Flask(__name__)
        #configure_routes(app)
        client = app.test_client()
        data = {
            "username": "nathoceanthet",
            "email": "naathphoenix89@gmail.com",
            "password": "qwerty"
        }
        res=request.post('http://localhost:5000/register', 
                        # headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(data), 
                        content_type='application/json')

        #res_json=json.loads(res.data)
#
        # TestBookCrud.id = res_json['id']
        assert res.get_data() == b"Account created successfully, an email with an activation link has been sent to your email address, please check."
        assert res.status_code == 201
        
        

# def test_v1_sample_post_endpoint(client):
#     payload = {
#         'username': 'test',
#         'key': 4,
#         'time': '15-12-2020'
#     }

#     response = client.post('sample-func', json=payload)
#     response_body = response.get_json()

#     assert response.status_code == 201
#     assert response_body.get('message') == "The return message goes here."





# def test_admin_edit_valid(self, client):
#         token = create_token_internal() 
#         data = {
#             'username': 'tes',
#             'password': 'tes',
#             'email' : 'tes@tes.com'
#         }
#         res=client.put('/admin', 
#                         headers={'Authorization': 'Bearer ' + token},
#                         data=json.dumps(data), 
#                         content_type='application/json')

#         res_json=json.loads(res.data)

#         # TestBookCrud.id = res_json['id']
#         assert res.status_code == 200


