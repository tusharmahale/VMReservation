# VM Reservation System API

This API provides endpoints to allow clients to check out and check in Virtual Machines (VMs) in a cloud environment. The API also includes functionality to perform cleanup on checked-in VMs before adding them back to the pool of available VMs.


## Installation
To run the API, you must have Python 3 and the following packages installed:
- sqlite3
- threading
- random
- string
- paramiko
- Flask
- jsonify
- requests

## Endpoints
### Checkout VM - /checkout
Request
```json
{
    "user_id": "1234"
}
```
Success Response
```json
{
  "status": "success",
  "vm_ip": "10.20.0.11"
}
```
No VM available Response
```json
{
  "message": "No VM available at this time, please try again later.",
  "status": "error"
}
```
### Checkin VM - /checkin
Request
```json
{
    "user_id": "1234",
    "vm_ip": "10.20.0.11"
}
```
Success Response
```json
{
  "message": "VM 10.20.0.11 has been checked in for user 1234.",
  "status": "success"
}
```
Failure Response
```json
{
  "message": "Invalid user_id or vm_ip.",
  "status": "error"
}
```

### Checking health of application - /health
Returns Success if application is running fine
```json
{
  "status": "success"
}
```

## Persistence
The API uses a file-based database to persist information about checked-out and available VMs. This means that if the API is restarted, it will still know all the information about VMs that have been checked out and VMs that are available.

## Docker
You can create docker container and deploy code as specified in Jenkinsfile