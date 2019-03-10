import smartcar
from flask import Flask, redirect, request, jsonify
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
    scope=['read_vehicle_info','read_location','control_security', 'control_security:unlock', 'control_security:lock', 'read_vin', 'read_odometer'],
    test_mode=False,
)

@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authorization dialog
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')
    # TODO: Request Step 1: Obtain an access token
    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)

    # TODO: Authorization Step 3: Handle Smartcar response
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
    response = vehicle.location()
    print(response)
    return jsonify(response)

@app.route('/lock', methods=['GET'])
def lock():
    # TODO: Request Step 2: Get vehicle ids
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    # TODO: Request Step 3: Create a vehicle
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    # TODO: Request Step 4: Make a request to Smartcar API
    vehicle.lock()

@app.route('/unlock', methods=['GET'])
def unlock():
    # TODO: Request Step 2: Get vehicle ids
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    # TODO: Request Step 3: Create a vehicle
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    # TODO: Request Step 4: Make a request to Smartcar API
    vehicle.unlock()

@app.route('/getstatus', methods=["GET"])
def getstatus():
    # TODO: Request Step 2: Get vehicle ids
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    # TODO: Request Step 3: Create a vehicle
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    # TODO: Request Step 4: Make a request to Smartcar API
    info = vehicle.info()
    location = vehicle.location()
    odometer = vehicle.odometer()
    vin = vehicle.vin()

    print("I am here")
    print("Vehicle Informatio: ", info, "/n", "Vehicle Location: ", location, "Odometer: ", odometer, "VIN: ", vin)

    return jsonify(info, location, odometer, vin)


if __name__ == '__main__':
    app.run(port=8000)
