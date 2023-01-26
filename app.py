from flask import Flask
from dbcreds import production_mode
import endpoints.city
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