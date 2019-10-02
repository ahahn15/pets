# Pets API
## Endpoints
- POST /pet
    Takes a JSON body that specifies a list of pets to be created:

    ```
    [{
    	"name": "Rover",
    	"type": "dog",
    	"age": 3,
    	"sex": "m", 
    	"description": "Schnauzer",
    	"owner_email": "bob.smith@mail.com", 
    	"image_url": "www.example.com"
    },
    {
    	"name": "Nemo",
    	"type": "fish",
    	"age": 30,
    	"sex": "m", 
    	"description": "Clownfish",
    	"owner_email": "esther.jones@mail.com", 
    	"image_url": "www.example.com"
    },
    {
    	"name": "Tweety",
    	"type": "bird",
    	"age": 10,
    	"sex": "f", 
    	"description": "Parrot",
    	"owner_email": "alice.park@mail.com", 
    	"image_url": "www.example.com"
    }]
    ```
    Returns: a list of ids created.
- PUT /pet
    Takes a JSON body that specifies a list of pets, their ids, and properties to be updated:
    ```
    [{
    	"id": 0,
    	"name": "Rover Jr."
    }]
    ```
- DELETE /pet
    Takes a JSON body that specifies a list of ids of pets to delete:
    ```
    [ 1, 2 ]
    ```
- GET /pet
    Takes a JSON body that specifies keys and values to use as filters in querying pets in the database:
    ```
    {
	    "type": "fish"
    }
    ```
    Returns: a list of pets that match the given criteria.

## Running locally
- If using Conda, create a new environment using Python 3.7.2: 
    `conda create --name cozi_pets python=3.7.2`
- Activate the new environment via the command line and install necessary libraries.
- In the command line, from the project root directory, run `python app.py`
- Use an application like Postman to make requests to localhost on port 8000.
- To reset the database, delete the `pets.pdl` file in the root directory.

## Running tests
- From the project root directory run `python test.py`.

## Recommended enhancements:
This API was created as a simple example given a short set of requirements. A more robust API would require:
- a full database
- validation of input to endpoints e.g. restrict values of 'sex' and 'type' to an enum, handle required/optional properties when creating resource
- tests for valid/invalid input specified above
- more error handling e.g. incorrect input
- a WSGI server that can handle multiple connections e.g. gunicorn
- scalable deployment e.g. on Docker image to ECS container
- more robust architecture e.g. model-view-controller