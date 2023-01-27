from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
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
    elif(category != None and city != None):
        results = run_statement('CALL get_residencies_by_city_and_category(?,?)', [request.args.get('city_id'), request.args.get('category_id')])
        
        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps('Wrong category and/or city id.', default=str), 400)
        else:
            return make_response(json.dumps('Sorry, an error has occurred.', default=str), 500)
        
def patch():
    is_valid = check_endpoint_info(request.json, ['residency_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    # residency info
    ri = run_statement('CALL get_residency_by_id(?)', [request.json.get('residency_id')])
    if(type(ri) == list and len(ri) == 0):
        return make_response(json.dumps("Wrong id.", default=str), 400)

    #update residency info
    ur = check_data_sent(request.json, ri[0], ['city_id', 'category_id', 'sqft', 'address', 'price'])

    results = run_statement('CALL edit_residency(?,?,?,?,?,?)', [request.json.get('residency_id'), 
    ur['city_id'], ur['category_id'], ur['sqft'], ur['address'], ur['price']])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong residency id.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    