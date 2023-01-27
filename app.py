from flask import Flask
from dbcreds import production_mode
import endpoints.city, endpoints.category, endpoints.residencies
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#############################################################
# city
#############################################################

@app.post('/api/city')
def post_city():
    return endpoints.city.post()

@app.get('/api/city')
def get_cities():
    return endpoints.city.get()

@app.delete('/api/city')
def delete_city():
    return endpoints.city.delete()


#############################################################
# category
#############################################################

@app.post('/api/category')
def post_category():
    return endpoints.category.post()

@app.get('/api/category')
def get_categories():
    return endpoints.category.get()

@app.delete('/api/category')
def delete_category():
    return endpoints.category.delete()


#############################################################
# residencie
#############################################################

@app.post('/api/residencies')
def post_residencie():
    return endpoints.residencies.post()

@app.get('/api/residencies')
def get_residencies():
    return endpoints.residencies.get()


# if statement to check if the production_mode variable is true, if yes, run in production mode, if not, run in testing mode
if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5075)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")

    app.run(debug=True)