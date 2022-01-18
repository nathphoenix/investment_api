import os
from flask import Flask, jsonify, Blueprint, g, render_template, url_for, redirect, session, make_response, abort
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, fresh_jwt_required
from marshmallow import ValidationError
from jinja2 import TemplateNotFound
#flask upload can be use not only for images but some other things also
from flask_uploads import configure_uploads, patch_request_class
from flask_login import logout_user, LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sieve import Sieve

import logging, sys
#This ensures the dotenv is loaded first before all our imported files 
load_dotenv(".env", verbose=True) #we have to manually load the .env file now as we have our default_config file
#which the .env file depends upon

from datetime import timedelta

from ma import ma 
from db import db
from oa import oauth
from blacklist import BLACKLIST
from resources.user import Loaders
from resources.user import UserRegister, UserLogin, User, SetPassword, TokenRefresh, UserLogout, UserDetails, TestId
from resources.sample_resource import SampleFunc
from resources.investment import Investment, InvestmentList, GetUserCreatedDate, CurrentUserInvestment, RemoveInvestment, InvestmentList2
from resources.confirmation import Confirmation, ConfirmationByUser
from sqlalchemy_utils import database_exists, create_database
#from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__, instance_relative_config=False, static_url_path='', static_folder='static/')
Sieve(app)

app.url_map.strict_slashes = False
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
if not database_exists(db_uri):
    create_database(db_uri)

#cache = SimpleCache()

app.config.from_object("default_config")  # load default configs from default_config.py

app.config.from_envvar(
    "APPLICATION_SETTINGS" #which is in the .env file
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']

 
jwt = JWTManager(app)

#setting session expiration time
#app.permanent_session_lifetime = timedelta(minutes=3)

#CORS(app)
CORS(app, resources={r'/v1/*'})
api = Api(app)


#api_blueprint = Blueprint('api', __name__)
#api = Api(api_blueprint)


@app.before_first_request
def create_tables():
    db.create_all()
    


    
@app.before_request
def before_request():
    session.permanent = True
    #setting session expiration time
    app.permanent_session_lifetime = timedelta(minutes=1.0)
    #return redirect(url_for('home'))



@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):    # as except ValidationError as err
    return jsonify(err.messages), 400


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@login_manager.user_loader
def load(id):
    Loaders.load_user(id)

@app.route('/user_account')
def user_page():
    if 'user_name' and 'user_invest' in session:
        user_invest = session['user_invest']
        user_name = session['user_name']
        return render_template("personal.html", user_name = user_name, user_invest = user_invest)
    else:
        return redirect(url_for('home'))

@app.route('/personal')
def personal_page():
    if 'user_name' in session:
        user_name = session['user_name']
        #user_invest = session['user_invest']
        return render_template("personal_2.html", user_name = user_name)
    else:
        #return render_template("index.html")
        return render_template("personal_2.html")

@app.route('/business')
#@jwt_required
def business_page():
    if 'user_name' in session:
        user_name = session['user_name']
        #user_invest = session['user_invest']
        return render_template("business.html", user_name = user_name)
    else:
        return render_template("business.html")
    #return render_template("business.html")

@app.route('/about')
def about_page():
    if 'user_name' in session:
        user_name = session['user_name']
        #user_invest = session['user_invest']
        return render_template("about.html", user_name = user_name)
    else:
        return render_template("about.html")
    #return render_template("about.html")


@app.route('/test')
def test_form():
    return render_template("home.html")

# @app.route('/test3')
# def test_form3():
#     return "home welcome"


@app.route('/change_pass')
def change_pass():
    return render_template("forgotpass.html")

# @app.route('/pytesting')
# def pytest():
#     return "Hello, World!", 200

@app.route('/form')
def modal_form():
    return render_template("get_started.html")

@app.route('/reactivate')
def reactivation():
    return render_template("reactivate.html")

app.route('/welcome_page')
def welcome():
    return render_template("welcome.html")

@app.route('/investment')
def invest():
    if 'user_name' in session:
        user_name = session['user_name']
        #user_invest = session['user_invest']
        return render_template("admin.html", user_name = user_name)
    else:
        return redirect(url_for('home'))

@app.route('/email')
def email():
    
    return render_template("emailmsg.html")
    


@app.route('/all_savings')
def all_saving():
    try:
        if 'user_name' and 'records' in session:
            records = session['records']
            user_name = session['user_name']
            admin = ['cozy', 'nathphoenix']
            if user_name in admin:
                return render_template("investment.html", user_name = user_name, records = records)
            elif not user_name in admin:
                #return render_template("index.html", user_name = user_name)
                return redirect(url_for('home', user_name = user_name))
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    except KeyError:
        return redirect(url_for('home'))

@app.route('/remove_invest')
def remove_invest():
    #return render_template("delete.html")
    if 'user_name' and 'access_token' in session:
        access_token = session.get('access_token')
        print('/remove_invest', access_token)
        user_name = session['user_name']
        if user_name == 'nathphoenix':
            headers={'Content-Type':'application/json', "Authorization" : f"Bearer {access_token}"}
            return render_template("delete.html", user_name = user_name, access_token = access_token, headers=headers)
        else:
            #return render_template("index.html", user_name = user_name)
            return redirect(url_for('home', user_name = user_name))
    else:
        return redirect(url_for('home'))
        

@app.route('/all_invest2')
def all_invest2():
    #return render_template("delete.html")
    if 'user_name' and 'access_token' and 'records' in session:
        access_token = session['access_token']
        user_name = session['user_name']
        records = session['records']
        if user_name == 'nathphoenix':
            headers={'Authorization': session['access_token']}
            return render_template("investment.html", user_name = user_name, access_token = access_token, records=records, headers=headers)
        else:
            #return render_template("index.html", user_name = user_name)
            return redirect(url_for('home', user_name = user_name))


# @app.route('/')
# def home():
# 	return render_template("index.html")

@app.route('/')
def home():
    if 'user_name' in session:
        user_name = session['user_name']
        #user_invest = session['user_invest']
        return render_template("index.html", user_name = user_name)
    else:
        return render_template("index.html")

# @app.route('/')
# def index():
#     response = make_response(render_template("index.html"))
#     response.set_cookie('access_token', 'YOUR_ACCESS_TOKEN')
#     response.set_cookie('refresh_token', 'YOUR_REFRESH_TOKEN')
#     return response


@app.route('/v1')
def v1_home():
    return jsonify({
        "message": "Welcome to DS Scrapper v1 API!"
    })


@app.route('/logouts')
def logout():
    #logout_user()
    session.pop('user_invest', None)
    session.pop('user_name', None)
    headers = {'Content-Type': 'text/html'}
    log_data = "You are Logged out"
    return make_response(render_template('index.html', log_data = log_data), headers), 200



# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserRegister, "/register", endpoint="register")

api.add_resource(GetUserCreatedDate, "/user_invest_date")
api.add_resource(Investment, "/invest", methods=['GET', 'POST'])
api.add_resource(InvestmentList, "/all_invest" )
api.add_resource(InvestmentList2, "/all_invest2" )
api.add_resource(CurrentUserInvestment, "/my_investments")
api.add_resource(RemoveInvestment, "/update_invest")

#FOR TEST PURPOSE
api.add_resource(SampleFunc, '/sample-func')

api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserDetails, '/user_details')
api.add_resource(TestId, '/user_id')
#api.add_resource(UserLogout, "/logout")



api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")  #this is for the html page
api.add_resource(ConfirmationByUser, "/re_confirmation/user")


#app.register_blueprint(api_blueprint, url_prefix='/v1')


if __name__ == "__main__":

    db.init_app(app)
    # this runs in the background and it tell that marshmallow object what flask app it should be talking to
    ma.init_app(app)
    oauth.init_app(app)
# loggings
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "storage/log/app.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    
    app.run(port=5000, debug=True)
