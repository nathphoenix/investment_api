# from flask_restful import Resource, reqparse
from email import message
from flask_restful import Resource
from flask import request, render_template, make_response, session, redirect, url_for
from flask_jwt_extended import jwt_required, fresh_jwt_required
from marshmallow import ValidationError
from models.investment import InvestmentModel
from schemas.investment import InvestmentSchema, InvestmentDeleteSchema
from libs.strings import gettext
from flask_login import login_required
from libs.mailgun import  GoogleMail

import traceback

# BLANK_ERROR = "'{}' cannot be blank."  as the parser goes, we are no longer in need of the blank error
NAME_ALREADY_EXISTS = "An item with username '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

invest_schema = InvestmentSchema()
invest_delete_schema = InvestmentDeleteSchema()
invest_list_schema = InvestmentSchema(many=True)  # instead of passing a single item model to d schema, we can pass it as a list




class Investment(Resource):

    @classmethod
    def post(cls):
        #session.get('access_token')
        # try:


        # invest = invest_schema.load(request.get_json())

        invest = request.get_json() if request.get_json() else dict(request.form)
        invest = invest_schema.load(invest)
        print(invest)

        try:
            if invest.creator == 'nathcozy':
                invest.save_to_db()
                #return {"message": gettext("investment_registered")}, 201
                message =  gettext("investment_registered")
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('add_invest.html', response = message), headers)
            else:
                message =  gettext("investment_failed")
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('add_invest.html', response = message), headers)
        except Exception as e:
            #invest.delete_from_db()  # so that if registration is incomplete without email, we want to remove the invest as they can't confirm their account
            message =  gettext("investment_error")
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('add_invest.html', response = message), headers)


    @classmethod
    def get(cls):
        
        result_json =  request.get_json() if request.get_json() else dict(request.form)
        print('HERE', result_json)
        result_json = invest_schema.load(result_json)
        
        created_at = result_json.created_at
        print(created_at)
        item = InvestmentModel.find_by_date(created_at)
 
        if item:
            headers = {'Content-Type': 'text/html'}
            data = invest_schema.dump(item)
            #return make_response(render_template('admin_created_at.html', user_invest = data), headers)
            return data, 200
        return {"message": gettext("item_not_found")}, 404

    
    @classmethod
    def delete(cls):
        
        result_jsons =  request.get_json() if request.get_json() else dict(request.form)
        result_json = invest_delete_schema.load(result_jsons)
        created_at = result_json.created_at
        item = InvestmentModel.find_by_date(created_at)
        if item:
            data = invest_schema.dump(item)
            # item.status = result_jsons["status"]
            # item.save_to_db()
            # item.delete_from_db()
            return {"message": data}, 200
            
        return {"message": gettext("item_not_found")}, 404

    @classmethod
    #@fresh_jwt_required
    def put(cls):
        # data = cls.parser.parse_args() takes arg that are coming through json
        item_json = request.get_json() if request.get_json() else dict(request.form)
        # result_json = invest_schema.load(request.get_json())
        username = item_json['username']
        item = InvestmentModel.find_by_name(username)  # then check if the item exist

        if item:   # if true it update it
            item.amount = item_json["amount"]
        else:
            item_json["username"] = username

            item = invest_schema.load(item_json)  # when we do item schema load, we are going to pass price and

        item.save_to_db()

        return invest_schema.dump(item), 200
    
    
class GetUserCreatedDate(Resource):
    @classmethod
    #@jwt_required
    def post(cls):
        try:
            result_json =  request.get_json() if request.get_json() else dict(request.form)
            print('HERE', result_json)
            result_json = invest_schema.load(result_json)
            
            created_at = result_json.created_at
            print(created_at)
            user_name = session.get('user_name')
            print('SESSION', user_name)
            item = InvestmentModel.find_by_date(created_at)
            if item:
                headers = {'Content-Type': 'text/html'}
                data = invest_schema.dump(item)
                user_invest = data
                user_invest['session'] = user_invest
                return make_response(render_template('admin_created_at.html', user_invest = user_invest, user_name= user_name), headers)
            headers = {'Content-Type': 'text/html'}
            record_not_found = gettext("details_not_found")
            return make_response(render_template('admin_created_at.html', record_not_found = record_not_found, user_name= user_name), headers)
        except:
            user_name = session.get('user_name')
            headers = {'Content-Type': 'text/html'}
            record_not_found = 'Invalid time format has been passed'
            return make_response(render_template('admin_created_at.html', record_not_found = record_not_found, user_name= user_name), headers)


#UPDATE RECORD FROM ACTIVE TO PAY
class RemoveInvestment(Resource):
    #@login_required
    @classmethod
    #@jwt_required
    def post(cls):
        print('I AM HERE NOW')
        try:
        # access_tokens = session.get('access_token')
        # print('access_token access_token access_token', access_tokens)
        # headers={'Authorization': session['access_token']}

        # if access_tokens:
            result_jsons =  request.get_json() if request.get_json() else dict(request.form)
            result_json = invest_schema.load(result_jsons)
            created_at = result_json.created_at
            item = InvestmentModel.find_by_date(created_at)
            user_name = session.get('user_name')
            if item:
                data = invest_schema.dump(item)
                item.status = result_jsons["status"]
                email = data['email']
                print(email)
                item.save_to_db()
                title_response = f'Payment Updated'
                headers = {'Content-Type': 'text/html'}
                update_response = f'User record has been updated to paid'
                message_body = f"Your investment on this date {created_at}  has been successfully settled and updated,\nYou are seeing this message as our loyal investor\nThank you for trusting us with your monry"
                GoogleMail.send_payment_alert(user_name, email, message_body)
                return make_response(render_template('update_payment.html', user_name= user_name, update_response = update_response, title_response = title_response ), headers)
                #return {"message": data}, 200
            else:
                title_response = f'Payment Update Failed'
                headers = {'Content-Type': 'text/html'}
                update_response = f'Unable to update records, record not found'
                return make_response(render_template('update_payment.html', user_name= user_name, update_response = update_response, title_response = title_response ), headers)
        except:
            user_name = session.get('user_name')
            title_response = f'Payment Update Failed'
            headers = {'Content-Type': 'text/html'}
            update_response = f'Invalid input was passed'
            return make_response(render_template('update_payment.html', user_name= user_name, update_response = update_response, title_response = title_response ), headers)

            #return {"message": 'gettext("item_not_found")'}, 404

class CurrentUserInvestment(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        session.get('access_token')
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user_json = invest_schema.load(user_json)
        username = user_json.username
        user_investment = InvestmentModel.find_all_name(username)
        user_investment = invest_list_schema.dump(user_investment)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('personal.html', resp_data = user_investment ), headers)
    


class InvestmentList(Resource):
    # @login_required
    @classmethod
    
    def get(cls):
        # return {"items": [item.json() for item in InvestmentModel.find_all()]}, 200
        #return {"items": invest_list_schema.dump(InvestmentModel.find_all())}, 200
        records = invest_list_schema.dump(InvestmentModel.find_all())
        session['records'] = records
        headers = {'Content-Type': 'text/html'}
        #return make_response(render_template('investment.html', all_savings = records), headers)
        response = redirect(url_for('all_saving'))
        return response
    # item_list_schema returns a list of each items

class InvestmentList2(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        access_token = session.get('access_token')
        if access_token:
            records = invest_list_schema.dump(InvestmentModel.find_all())
            session['records'] = records
            return records, 200
        #headers = {'Content-Type': 'text/html'}
        #return make_response(render_template('investment.html', all_savings = records), headers)
        # response = redirect(url_for('all_saving'))
        # return response