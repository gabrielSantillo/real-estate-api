import os
from uuid import uuid4
from dbhelpers import run_statement
import smtplib
import email.message    


def save_file(file):
    # Check to see if first, the filename contains a . character. 
    # Then, split the filename around the . characters into an array
    # Then, see if the filename ends with any of the given extensions in the array
    # You can add or remove file types you want or do not want the user to store
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['gif','png','jpg','jpeg', 'webp', 'pdf']):
        # Create a new filename with a token so we don't get duplicate file names
        # End the filename with . and the original filename extension
        filename = uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            # Use built-in functions to save the file in the images folder
            # You can put any path you want, in my example I just need them in the images folder right here
            file.save(os.path.join('residencies_images', filename))
            # Return the filename so it can be stored in the DB
            return filename
        except Exception as error:
            # If something goes wrong, print out to the terminal and return nothing
            print("FILE SAVE ERROR: ", error)
    # If any conditional is not met or an error occurs, None is returned

# function responsible to the sent_data that will is going to be request.args or request.json and the
# expected_data taht is going to be the list of keys the endpoint requires
# this function will return a string in case of error and None otherwise
def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if (sent_data.get(data) == None):
            return f"The {data} argument is required."

# function responsible fill in data was not sent by the client when trying to update data in the db
def check_data_sent(sent_data, original_data, expected_data):
    for data in expected_data:
        if (sent_data.get(data) != None):
            original_data[data] = sent_data[data]
    return original_data


def organize_client_response(response):
    organized_list = []
    cities = []

    for data in response:
        if (data['city_name'] in cities):
            new_client = {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'phone_number': data['phone_number'],
                'budget': data['budget']
            }
            client['clients'].append(new_client)
        else:
            cities.append(data['city_name'])

            client = {
                'city_name': data['city_name'],
                'clients': [{
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'phone_number': data['phone_number'],
                    'budget': data['budget']
                }]
            }
            organized_list.append(client)
    return organized_list

def send_email(name, client_email):
    email_body = """
    <h1>Hello, {name}</h1><br>
    <p>We are happy to have you with us!</p>
    <p>Soon enough someone from our great team will reach you out based on your preferences.</p>
    <br>
    <p>Kind regards.</p>
    <br><hr>
    <h4>Real Estate Dream Team</h4>
    """.format(name=name)

    msg = email.message.EmailMessage()
    msg['Subject'] = 'Hello from Real Estate Corporation'
    msg['From'] = 'gasantillo7@gmail.com'
    msg['To'] = client_email
    password = 'jxehxxfdhjxadehd'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_body)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))