from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, save_file
import json
from dbhelpers import run_statement
import os

def post():
    is_valid = check_endpoint_info(request.form, ['residency_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    is_valid_file = check_endpoint_info(request.files, ['uploaded_file'])
    if(is_valid_file != None):
        return make_response(json.dumps(is_valid_file, default=str), 400)
    
    filename = save_file(request.files['uploaded_file'])
    if(filename == None):
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    
    results = run_statement("CALL add_residency_image(?,?)", [request.form['residency_id'], filename])

    if(type(results) == list and results[0]['id'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and results[0]['id'] == 0):
        image_path = os.path.join('residencies_images', filename)
        os.remove(image_path)
        return make_response(json.dumps("Wrong residency id.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    
def get():
    is_valid = check_endpoint_info(request.args, ['file_name'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL get_image(?)', [request.args.get('file_name')])

    if(type(results) != list):
        return make_response(json.dumps(results, default=str), 500)
    elif(len(results) == 0):
        return make_response(json.dumps("Wrong file name or wrong token.", default=str), 400)

    return send_from_directory('residencies_images', results[0]['file_name'])