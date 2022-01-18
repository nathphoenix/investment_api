from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from flask_restful import Resource
from flask import request, make_response, render_template, jsonify, session
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    fresh_jwt_required,
)

from functions.case import resend_confirmation_email

import traceback
from marshmallow import ValidationError
from schemas.user import UserSchema, UserListSchema
from schemas.investment import InvestmentSchema
from models.user import UserModel
from schemas.confirmation import ConfirmationListSchema
from models.confirmation import ConfirmationModel
from models.investment import InvestmentModel
from blacklist import BLACKLIST
from libs.mailgun import GoogleMail
from libs.strings import gettext


invest_list_schema = InvestmentSchema(many=True)
confirm_schema_list = ConfirmationListSchema(many=True)
user_list_schema = UserListSchema()
user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        # try:
        user = request.get_json() if request.get_json() else dict(request.form)
        user = user_schema.load(user)
        user_detail = user.username
        print(user)

        if UserModel.find_by_username(user.username):
            user_resp = f'Username({str(user.username)}) already exist. Please use a different username.'
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('user_exist.html', user_resp = user_resp), headers)
            #return user_resp, 200
        if UserModel.find_by_email(user.email):
            flash('user_email_exists')
            user_resp = f'Email({str(user.email)}) already exist. Please use a different email.'
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('email_exist.html', user_resp = user_resp), headers)

        try:
            # user = UserModel(**user)  # we no longer need to create a user model down here
            user.save_to_db()
            
            confirmation = ConfirmationModel(user.id) # we want to create a confirmation model with the user then save to database before sending confirmation email
            confirmation.save_to_db()
            print('IM HERE POSTMAN PLEASE', user_detail)
            #return user_schema.dump(user), 200
            user.send_confirmation_email()
            headers = {'Content-Type': 'text/html'}
            user_detail = str(user.username)
            return make_response(render_template('welcome.html', user_detail = user_detail), headers)
            #return {"message": gettext("user_registered")}, 201
        
        except TypeError as e:
            user.delete_from_db()  # so that if registration is incomplete without email, we want to remove the user as they can't confirm their account
            headers = {'Content-Type': 'text/html'}
            resp_data = "Please check your network connection"
            return make_response(render_template('error.html', resp_data = resp_data), headers)
        except: #failed to save user to db by deleting the entered data
            traceback.print_exc()
            user.delete_from_db()
            headers = {'Content-Type': 'text/html'}
            resp_data = "Please check your network connection"
            return make_response(render_template('error.html', resp_data = resp_data), headers)


class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200
    # since we are using marshmallow now, we are no longer responding with user.json() which is required by reqparse
    # instead we are using the deserialize form by using dump

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message":gettext("user_deleted")}, 200
    
    


class UserLogin(Resource):
    @classmethod
    def post(cls):
        session.pop('id', None)

        user_json = request.get_json() if request.get_json() else dict(request.form)
        
        user_data = user_schema.load(user_json, partial=("email",))  # we ignore the email field if it is not present
        # we have to tell marshmallow to forget about specific field like the

        user = UserModel.find_by_username(user_data.username)

        # this is what the `authenticate()` function did in security.py
        if user and user.password and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation  #this is ok as we expire old confirmation and pick the latest confirmation
            if confirmation and confirmation.confirmed: #we check if user is activated or not after logging in
                # identity= is what the identity() function did in security.py—now stored in the JWT
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                session['id'] = user.id
                #session['logged_in']=True
                session['access_token']=access_token

                user_investment = InvestmentModel.find_all_name(user_data.username)
                user_investment = invest_list_schema.dump(user_investment)
                user_name = user_data.username
                session['user_name'] = user_name
                #return {'access_token': access_token, 'refresh_token':refresh_token}
                session['user_invest'] = user_investment
                records = invest_list_schema.dump(InvestmentModel.find_all())
                session['records'] = records
                #return  {"items": invest_list_schema.dump(user_investment)}, 200
                #headers = {'Content-Type': 'text/html'}

                #response = make_response(render_template('index.html'), headers)
                response = redirect(url_for('home'))
                #response.headers["Authorization"] = f"Bearer {access_token}"
                #response.headers = {'Authorization': 'Bearer {}'.format(access_token)}
                # response.set_cookie('access_token', f'{access_token}')
                # response.set_cookie('refresh_token', f'{refresh_token}')
                return response
            else:
                if 'user_name' in session:
                    redirect(url_for('user_page'))
                #UserModel.find_by_email(user.username)
                # dets = ConfirmationModel.find_by_id(user.email)
                # UserModel.resend_confirmation_email(user.email)
                unknown_user = gettext("user_not_confirm")
                #return {"message": gettext("user_not_confirmed").format(user.email)}, 400
                return make_response(render_template('index.html', unknown_user = unknown_user))
        #return {"message": gettext("user_invalid_credentials")}, 401
        login_fail = gettext("user_details_credentials")
        return  make_response(render_template('index.html', login_fail = login_fail))


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200

class Loaders():
    def load_user(self, id):
        try:
            return UserModel.query.get(id)
        except:
            return None

class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
 

class SetPassword(Resource):
    @classmethod
    #@fresh_jwt_required
    def post(cls):
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)
        email = user_data.email
        user_name = user_data.username

        if not user:
            #return {"message": gettext("user_not_found")}, 400
            invalid_user = gettext("user_not_found")
            password_status = 'Password change failed'
            message_body = f'This username {user_data.username} does not exist'
            return make_response(render_template('forgotpass.html', message_response=invalid_user, password_status=password_status, message_body=message_body ))

        user.password = user_data.password
        user.save_to_db()
        password_status = 'Password change successfully'
        message_body = f'Password has been change for username {user_data.username}'
        message_body_2 = f'Password has been change for username {user_data.username}\nPlease if you didn"t initiate this process you can get in touch with admin for further assistance.\nThank you'
        GoogleMail.send_payment_alert(user_name, email, message_body_2)
        return make_response(render_template('forgotpass.html', message_response=user,  password_status= password_status, message_body=message_body))



class UserDetails(Resource):
    @classmethod
    def get(cls):
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user_json = user_json['email']
        email = user_json
        #user_data = user_list_schema.load(user_json)
        user = UserModel.find_by_email(user_json)
        print(user)
        #user = user.confirmation[0]
        #user = str(user)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user = user_list_schema.dump(user)
        username = user['username']
        print(type(email))
        user = user['confirmation'][0]
        confirm_id = ConfirmationModel.find_by_id(user)
        user_id = confirm_schema_list.dump(confirm_id)
        user_id = user_id[0]['user']
        ids = user_id
        print('ids', ids)
        try: 
            resend_confirmation_email(username, email, ids, user)
            return 'success', 200
        except:
            return 'Sending failed', 400
        #return resend_confirmation_email(username, email, id), 200
    
#testing confirmation_id 7f9bcb9c189e457d872e3293b790f881
class TestId(Resource):
    @classmethod
    def get(cls):
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user_json = user_json['user_id']
        user = ConfirmationModel.find_by_ids(user_json)
        print(user)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user = confirm_schema_list.dump(user)
        return user, 200