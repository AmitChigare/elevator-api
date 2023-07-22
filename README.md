# JumpingMinds Django Backend Challenge

The project is a backend API for controlling elevators in a building. It allows users to interact with elevators by making requests to move to specific floors, start/stop elevators, and open/close elevator doors. The API provides endpoints to retrieve elevator details, put elevators under maintenance, and get pending requests. The project includes models for elevators and elevator requests, along with serializer classes for data serialization. The API is designed to efficiently manage elevator operations, simulate elevator movements, and handle user requests for smooth building transportation.

## Repository Setup

1. Clone the repository to your local machine (`main` branch):

   ```
   $ git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   $ cd <directory>
   ```

3. Install the required dependencies:

   ```
   $ pip install -r requirements.txt
   ```

4. Set up the database:

   ```
   $ python manage.py makemigrations
   $ python manage.py migrate
   ```

5. Create a superuser to access the admin interface:

   ```
   $ python manage.py createsuperuser
   ```

6. Start the development server:

   ```
   $ python manage.py runserver
   ```

7. Open your web browser and visit [http://127.0.0.1:8000/api/v1/elevators/](http://127.0.0.1:8000/api/v1/elevators/) . Make a POST request to add an Elevator (Please refer [API Documentation (md)](./APIDocs.md) for `body` requirements).

#### Admin Panel:

- Admin Panel has the functionality to have access over all the Entries and Users. Do check it out to have more control over the api. [Admin Panel](http://localhost:8000/admin)

### Configuration

- Modify the project settings in `settings.py` as needed, such as database settings, static files, etc. If hosted, remember to add the host address in the `setting.py` file.

## Running the Test Suite

- Run the tests to make sure everything is working correctly:

  ```
  $ python manage.py test
  ```

  This command will run all the tests and display the results in the console.

## Running the API Server

- Run the following command to start the API server:
  ```
  $ python manage.py runserver 8000
  ```
  The API server will start, and you can access it at http://localhost:8000/ in your web browser or via API clients like cURL or Postman.
  Make sure to replace 8000 with the appropriate port number if you have configured a different port for your Django project.

## Deployment

- Refer to the official Django documentation for instructions on deploying Django projects to production environments.

## API Documentation

[API Live Postman Collection](https://documenter.getpostman.com/view/21453554/2s946mYp1b)<br>
[API Documentation (markdown)](./APIDocumention.md)
