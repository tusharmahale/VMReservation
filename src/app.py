from flask import Flask, jsonify, request
from vm_reservation_system import VMReservationSystem

app = Flask(__name__)
vm_reservation_system = VMReservationSystem('VMDB')

@app.route('/health', methods=['GET'])
def health():
    response = {
            'status': 'success',
    }
    return jsonify(response)

@app.route('/checkout', methods=['POST'])
def checkout():
    # extract user_id from request body
    user_id = request.json.get('user_id')

    # check out a VM for the user
    vm_ip = vm_reservation_system.checkout(user_id)

    if vm_ip:
        # return VM IP to user
        response = {
            'status': 'success',
            'vm_ip': vm_ip
        }
    else:
        # no VM available, return error message
        response = {
            'status': 'error',
            'message': 'No VM available at this time, please try again later.'
        }

    return jsonify(response)

@app.route('/checkin', methods=['POST'])
def checkin():
    # extract user_id and vm_ip from request body
    user_id = request.json.get('user_id')
    vm_ip = request.json.get('vm_ip')

    # check in the VM for the user
    success = vm_reservation_system.checkin(user_id, vm_ip)

    if success:
        response = {
            'status': 'success',
            'message': f'VM {vm_ip} has been checked in for user {user_id}.'
        }
    else:
        # invalid user_id or vm_ip
        response = {
            'status': 'error',
            'message': 'Invalid user_id or vm_ip.'
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8000,debug=True)
