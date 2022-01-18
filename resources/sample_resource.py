from flask.helpers import flash, url_for
from flask_restful import Resource, reqparse
import os
from flask import request
from pymongo import MongoClient
from bson.objectid import ObjectId

# To import and use and environment variable from the .env file do this
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_COLLECTION = os.environ.get('DATABASE_COLLECTION')
TEST_DATABASE = os.environ.get('TEST_DATABASE')
# After importing like this you can then use the variable you define. please follow the alpha case
client = MongoClient(DATABASE_URL)


class SampleFunc(Resource):
    def get(self):
        # To handle get request please follow this pattern.
        try:
            '''
                To retrieve the get request params follow this method as it is the standard.
                You can define as many parameters as possible. This parameters are the same one that should be passed as
                a params in get request not as a request body. 
            '''
            parser = reqparse.RequestParser()
            parser.add_argument('param1', type=int, trim=True, required=True)
            parser.add_argument('param2', type=str, trim=True, required=False)

            args = parser.parse_args()

            f_param = args.param1
            s_param = args.param2

            data = {'first_param': f_param, 'second_param': s_param}

            return {
                'status': 'success',
                'data': 'The data you want to return to user goes here. ' + str(data),
                'message': 'The return message goes here.'
            }, 200

        except Exception as e:
            return {
                'status': 'failed',
                'data': None,
                'message': str(e)
            }, 500

    def post(self):
        # To handle post request please follow this pattern.
        try:
            '''
                To retrieve the get data sent through the request body follow this method as it is the standard.
            '''
            # all the data sent via the request body will available on the json_data variable
            json_data = request.get_json()

            # to access any of the data sent do this
            username = json_data['username']

            '''
                to run validation on a particular value i.e to check the validity of the data, whether the data was sent 
                and if it was sent to be sure it is not empty
            '''
            req_fields = ['username', 'key', 'time']
            for field in req_fields:
                if field not in json_data:
                    return {
                       'status': 'failed',
                       'data': None,
                       'message': field + ' is required'
                    }, 400
                elif json_data[field] == '':
                    return {
                       'status': 'failed',
                       'data': None,
                       'message': field + ' cannot be empty'
                    }, 400
                else:
                    pass

            db = client[TEST_DATABASE]
            collection = db[DATABASE_COLLECTION]

            return {
               'status': 'success',
               'data': 'The data you want to return to user goes here. ' + str(json_data),
               'message': 'The return message goes here.'
            }, 201

        except Exception as e:
            return {
                'status': 'failed',
                'data': None,
                'message': str(e)
            }, 500

    def patch(self, doc_id):
        # to handle and update request follow the pattern
        """
         A patch and put request are different while a patch request update parts of a dataset a put request
            updates the entire dataset.
        :param doc_id: is the database id of the data you want to update. the naming (doc_id) must be the same with the
        one you define when creating the endpoint in the app.py file.
        :return:
        """
        try:
            # As with the post request all the data sent via the request body will available on the json_data variable
            json_data = request.get_json()
            # the id of will be accessible with the doc_id.

            """
                as a practise always define your database collection as an environment variable so that in the event 
                that is changes it will be easy to update
            """
            db = client[TEST_DATABASE]
            collection = db[DATABASE_COLLECTION]

            collection.find_one_and_update({
                {'_id': ObjectId(doc_id)},
                {'$set': json_data}
            })

            return {
                'status': 'success',
                'data': 'The data you want to return to user goes here. ' + str(json_data),
                'message': 'The return message goes here.'
            }, 201
        except Exception as e:
            return {
               'status': 'failed',
               'data': None,
               'message': str(e)
            }, 500
