# import pytest, json, logging
# from flask import Flask, request, json
# # from blueprints import app, db
# from app import cache
# # from blueprints.admin.model import Admins
# # from blueprints.client.model import Clients
# # from blueprints.client_detail.model import ClientDetails
# # from blueprints.product.model import Products

# def call_client(request):
#     app.testing = True
#     client = app.test_client()
#     return client

# @pytest.fixture
# def client(request):
#     return call_client(request)


# def reset_database():

#     db.drop_all()
#     db.create_all()

#     admin = Admins("tes", "tes", "tes@tes.com")
#     client = Clients("tes", "tes", "tes@tes.com")
#     # client_detail = ClientDetails(1, "fullname", "081208520813", "address")
#     product = Products("name", "description", "category", "image", 10000, 10, 9000, 20)
    

#     # save users to database
#     db.session.add(admin)
#     db.session.add(client)
#     # db.session.add(client_detail)
#     db.session.add(product)
#     db.session.commit()

# def create_token_non_internal():
#     token = cache.get('token-non-internal')
#     if token is None:
#         ## prepare request input
#         data = {
#             'username': 'tes',
#             'password': 'tes'
#         }

#         ## do request
#         req = call_client(request)
#         res = req.post('/token', data=json.dumps(data), content_type='application/json') # seperti nembak API luar (contoh weather.io)

#         ## store response
#         res_json = json.loads(res.data)

#         logging.warning('RESULT : %s', res_json)

#         ## assert / compare with expected result
#         assert res.status_code == 200

#         ## save token into cache
#         cache.set('token-non-internal', res_json['token'], timeout=60)

#         ## return because it useful for other test
#         return res_json['token']
#     else:
#         return token


# def create_token_internal():
#     token = cache.get('token-internal')
#     if token is None:
#         ## prepare request input
#         data = {
#             'username': 'tes',
#             'password': 'tes',
#             'email' : 'tes@tes.com'
#         }

#         ## do request
#         req = call_client(request)
#         res = req.post('/token/admin', data=json.dumps(data), content_type='application/json') # seperti nembak API luar (contoh weather.io)

#         ## store response
#         res_json = json.loads(res.data)

#         logging.warning('RESULT : %s', res_json)

#         ## assert / compare with expected result
#         assert res.status_code == 200

#         ## save token into cache
#         cache.set('token-internal', res_json['token'], timeout=60)

#         ## return because it useful for other test
#         return res_json['token']
#     else:
#         return token
    
        