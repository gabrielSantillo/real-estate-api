from flask import request, make_response
from apihelpers import check_endpoint_info, organize_client_response, check_data_sent, send_client_email, send_team_email
import json
from dbhelpers import run_statement

def post():
    is_valid = check_endpoint_info(request.json, ['preferable_city', 'first_name', 'last_name', 'email', 'phone_number', 'budget'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL add_client(?,?,?,?,?,?)', [request.json.get('preferable_city'), request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('phone_number'), request.json.get('budget')])

    if(type(results) == list and len(results) != 0):
        send_client_email(request.json.get('first_name'), request.json.get('email'))
        send_team_email(request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('phone_number'), results[0]['city'], request.json.get('budget'), results[0]['created_at'])
        return make_response(json.dumps(results[0], default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occured.", default=str), 500)
    
def get():
    results = run_statement('CALL get_client()')
    
    if(type(results) == list and len(results) != 0):
        results = organize_client_response(results)
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('Sorry, an error has occurred.', default=str), 500)
    

def patch():
    is_valid = check_endpoint_info(request.json, ['client_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    # residency info
    ri = run_statement('CALL get_client_by_id(?)', [request.json.get('client_id')])
    if(type(ri) == list and len(ri) == 0):
        return make_response(json.dumps("Wrong id.", default=str), 400)

    #update client info
    ci = check_data_sent(request.json, ri[0], ['preferable_city', 'first_name', 'last_name', 'email', 'phone_number', 'budget'])

    results = run_statement('CALL edit_client(?,?,?,?,?,?,?)', [request.json.get('client_id'), 
    ci['preferable_city'], ci['first_name'], ci['last_name'], ci['email'], ci['phone_number'], ci['budget']])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong client id.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    
def delete():
    is_valid = check_endpoint_info(request.json, ['client_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    results = run_statement("CALL delete_client(?)", [request.json.get('client_id')])

    if(type(results) == list and results[0]['row_updated'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and results[0]['row_updated'] == 0):
        return make_response(json.dumps("Wrong client id.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)