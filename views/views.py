from flask import request, make_response, render_template
import json



def configure_routes(app):
    @app.route('/pytesting')
    def hello_world():
        return 'Hello, World!'
    
    @app.route('/test3')
    def test_form3():
        return "home welcome"
    
    @app.route('/post/test', methods=['POST'])
    def receive_post():
        headers = request.headers

        auth_token = headers.get('authorization-sha256')
        if not auth_token:
            return 'Unauthorized', 401

        data_string = request.get_data()
        data = json.loads(data_string)

        request_id = data.get('request_id')
        payload = data.get('payload')

        if request_id and payload:
            return 'Ok', 200
        else:
            return 'Bad Request', 400
        
    #@app.route('/register', methods=['POST'])
    # def post(cls):
    #     # try:
    #     user = request.get_json() if request.get_json() else dict(request.form)
    #     user = user_schema.load(user)
    #     user_detail = user.username
    #     print(user)

    #     if UserModel.find_by_username(user.username):
    #         user_resp = f'Username({str(user.username)}) already exist. Please use a different username.'
    #         headers = {'Content-Type': 'text/html'}
    #         return make_response(render_template('user_exist.html', user_resp = user_resp), headers)
    #         #return user_resp, 200
    #     if UserModel.find_by_email(user.email):
    #         user_resp = f'Email({str(user.email)}) already exist. Please use a different email.'
    #         headers = {'Content-Type': 'text/html'}
    #         return make_response(render_template('email_exist.html', user_resp = user_resp), headers)

    #     try:
    #         # user = UserModel(**user)  # we no longer need to create a user model down here
    #         user.save_to_db()
            
    #         confirmation = ConfirmationModel(user.id) # we want to create a confirmation model with the user then save to database before sending confirmation email
    #         confirmation.save_to_db()
    #         print('IM HERE POSTMAN PLEASE', user_detail)
    #         #return user_schema.dump(user), 200
    #         #user.send_confirmation_email()
    #         headers = {'Content-Type': 'text/html'}
    #         user_detail = str(user.username)
    #         #return make_response(render_template('welcome.html', user_detail = user_detail), headers)
    #         return {"message": gettext("user_registered")}, 201
        
    #     except TypeError as e:
    #         user.delete_from_db()  # so that if registration is incomplete without email, we want to remove the user as they can't confirm their account
    #         headers = {'Content-Type': 'text/html'}
    #         resp_data = "Please check your network connection"
    #         return make_response(render_template('error.html', resp_data = resp_data), headers)
    #     except: #failed to save user to db by deleting the entered data
    #         #traceback.print_exc()
    #         user.delete_from_db()
    #         headers = {'Content-Type': 'text/html'}
    #         resp_data = "Please check your network connection"
    #         return make_response(render_template('error.html', resp_data = resp_data), headers)

