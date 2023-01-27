from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import json
from dbhelpers import run_statement

def post():
    is_valid = check_endpoint_info(request.json, ['preferable_city', 'first_name', 'last_name', 'email', 'phone_number', 'budget'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL add_client(?,?,?,?,?,?)', [request.json.get('preferable_city'), request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('phone_number'), request.json.get('budget')])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occured.", default=str), 500)