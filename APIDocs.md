## API Documentation

The backend API provides the following endpoints:

### Elevator Endpoints

#### List Elevators

- URL: `/api/v1/elevators/`
- Method: GET
- Description: Retrieve a list of all elevators.
- Response: Returns a JSON array of elevator objects.

#### Create Elevator

- URL: `/api/v1/elevators/`
- Method: POST
- Description: Creates a new elevator.
- Request Body:
  - current_floor (integer, optional): The current floor of the elevator (default: 1).
  - direction (string, optional): The direction of the elevator ("up", "down", or "idle") (default: "up").
  - status (string, optional): The status of the elevator ("idle", "running", or "maintenance") (default: "idle").
  - operational (boolean, optional): The operational status of the elevator (default: True).
  - door_open (boolean, optional): The door open status of the elevator (default: False).
- Response: Returns the details of the newly created elevator.

#### Retrieve Elevator Details

- URL: `/api/v1/elevators/<int:elevator_id>/`
- Method: GET
- Description: Retrieve details of a specific elevator.
- Response: Returns a JSON object with the elevator details.

#### Start Elevator

- URL: `/api/v1/elevators/<int:elevator_id>/start/`
- Method: POST
- Description: Start the specified elevator.
- Response: Returns a success message.

#### Stop Elevator

- URL: `/api/v1/elevators/<int:elevator_id>/stop/`
- Method: POST
- Description: Stop the specified elevator.
- Response: Returns a success message.

#### Open Elevator Door

- URL: `/api/v1/elevators/<int:elevator_id>/door/open/`
- Method: POST
- Description: Open the door of the specified elevator.
- Response: Returns a success message.

#### Close Elevator Door

- URL: `/api/v1/elevators/<int:elevator_id>/door/close/`
- Method: POST
- Description: Close the door of the specified elevator.
- Response: Returns a success message.

#### Create Elevator Request

- URL: `/api/v1/elevators/<int:elevator_id>/request/`
- Method: POST
- Description: Make a request to the specified elevator to go to a specific floor.
- Request Body:
  - `floor` (integer, required): The floor number to which the elevator should go.
- Response: Returns a success message with information about the request.

#### Put Elevator Under Maintenance

- URL: `/api/v1/elevators/<int:elevator_id>/maintenance/`
- Method: POST
- Description: Put the specified elevator under maintenance.
- Response: Returns a success message.

#### Get Pending Requests

- URL: `/api/v1/elevators/<int:elevator_id>/get_pending_requests/`
- Method: GET
- Description: Get a list of pending requests for the specified elevator.
- Response: Returns a JSON array of elevator requests.

### Serializer Classes

#### ElevatorSerializer

- Description: Serializer class for the Elevator model.
- Fields:
  - `id`: IntegerField
  - `current_floor`: PositiveIntegerField
  - `direction`: CharField
  - `status`: CharField
  - `operational`: BooleanField
  - `door_open`: BooleanField

#### ElevatorRequestSerializer

- Description: Serializer class for the ElevatorRequest model.
- Fields:
  - `id`: IntegerField
  - `elevator`: PrimaryKeyRelatedField
  - `floor`: PositiveIntegerField

### Models

#### Elevator

- Description: Represents an elevator.
- Fields:
  - `id`: AutoField (Primary Key)
  - `current_floor`: PositiveIntegerField (default=1)
  - `direction`: CharField (choices: "up", "down", "idle"; default="up")
  - `status`: CharField (choices: "idle", "running", "maintenance"; default="idle")
  - `operational`: BooleanField (default=True)
  - `door_open`: BooleanField (default=False)

#### ElevatorRequest

- Description: Represents a user request for a specific elevator to go to a floor.
- Fields:
  - `id`: AutoField (Primary Key)
  - `elevator`: ForeignKey (related to Elevator model)
  - `floor`: PositiveIntegerField
