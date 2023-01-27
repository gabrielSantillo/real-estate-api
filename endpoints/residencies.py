from flask import request, make_response
from apihelpers import check_endpoint_info
import json
from dbhelpers import run_statement

def post():
    is_valid = check_endpoint_info(request.json, ['city_id', 'category_id', 'sqft', 'address', 'price'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL add_residencie(?,?,?,?,?)', [request.json.get('city_id'), request.json.get('category_id'), request.json.get('sqft'), request.json.get('address'), request.json.get('price')])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occured.", default=str), 500)
    
def get():
    city = request.args.get('city_id')
    category = request.args.get('category_id')

    if(city == None and category == None):
        results = run_statement('CALL get_all_residencies()')
        
        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps('Sorry, an error has occurred.', default=str), 500)
    elif(city != None and category == None):
        results = run_statement('CALL get_residencies_by_city(?)', [request.args.get('city_id')])
        
        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps('Wrong city id.', default=str), 400)
        else:
            return make_response(json.dumps('Sorry, an error has occurred.', default=str), 500)
    elif(category != None and city == None):
        results = run_statement('CALL get_residencies_by_category(?)', [request.args.get('category_id')])
        
        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps('Wrong category id.', default=str), 400)
        else:
            return make_response(json.dumps('Sorry, an error has occurred.', default=str), 500)