import smartcar
from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

# TODO: Authorization Step 1a: Launch Smartcar authorization dialog
client = smartcar.AuthClient(
                             client_id=os.environ.get('CLIENT_ID'),
                             client_secret=os.environ.get('CLIENT_SECRET'),
                             redirect_uri=os.environ.get('REDIRECT_URI'),
                             scope=['read_vehicle_info', 'read_location', 'control_security',
                                    'control_security:unlock', 'control_security:lock',
                                    'read_location', 'read_odometer'],
                             test_mode=False,
                             )


@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authorization dialog
    auth_url = client.get_auth_url()
    return redirect(auth_url)

@app.route('/home', methods=['GET'])
def home():
    return render_template('main.html')


@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)
    
    # TODO: Request Step 1: Obtain an access token
    print(code)
    return '', 200

@app.route('/vehicle', methods=['GET'])
def vehicle():
    # TODO: Request Step 2: Get vehicle ids
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    # TODO: Request Step 3: Create a vehicle
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    # TODO: Request Step 4: Make a request to Smartcar API
    info = vehicle.info()
    print(info)
    '''
        {
        "id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
        "make": "TESLA",
        "model": "Model S",
        "year": 2014
        }
        '''
    location = vehicle.location()
    print(location)
    
    odometer = vehicle.odometer()
    print(odometer)
    
    permissions = vehicle.permissions()
    print(permissions)
    
    return jsonify("Vehicle info: ", info, "\\n Vehicle location: ",
                   location, "\\n Vehicle Odometer: ", odometer,
                   "\\n Permissions: ", permissions)
    pass

@app.route('/cars', methods=['GET'])
def cars():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    info = vehicle.info()
    gps = vehicle.location()
    odometer = vehicle.odometer()
    return render_template('results.html',
                           year = info['year'],
                           make = info['make'],
                           model = info['model'],
                           longitude = gps['data']['longitude'],
                           latitude = gps['data']['latitude'],
                           miles= odometer['data']['distance'])

@app.route('/unlock', methods=['GET'])
def unlock():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    vehicle.unlock()
    pass

@app.route('/lock', methods=['GET'])
def lock():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    vehicle.lock()
    pass

@app.route('/location', methods=['GET'])
def location():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    location = vehicle.location()
    print(location)
    return jsonify(location)
    pass

if __name__ == '__main__':
    app.run(port=8000)
