# Pizza Restaurants Management System
## Overview
This repository contains a Flask application designed to manage Pizza Restaurant operations. The API serves as a backend for a fully built React frontend application. This challenge focuses on building and completing various backend functionalities to manage pizzas, restaurants, and restaurant-pizza relationships.

## Key Features
- Flask API for managing pizza restaurants.
- React frontend available for interaction with the API.
- Postman collection for testing API routes.
- Automated testing with pytest to validate API functionality.
## Project Structure
The project includes the following key files and folders:

server/: Contains the Flask application files and models.
client/: Contains the React frontend for interacting with the API.
tests/: Contains automated tests to verify API functionality.
challenge-1-pizzas.postman_collection.json: A Postman collection for manually testing the API endpoints.
Setup Instructions
1. Clone the Repository
Clone this repository to your local machine:
2. Install Dependencies
Ensure you have pipenv installed. Run the following commands to install the dependencies for both the Flask backend and React frontend:
- pipenv install
- pipenv shell
- npm install --prefix client
3. Set Up the Database
Create and set up the SQLite database using Flask-Migrate:
- export FLASK_APP=server/app.py
- flask db init
- flask db upgrade head
You can then run the seed script to populate the database with sample data:
- python server/seed.py
If you encounter issues with the seed data, you can modify or create your own data.

4. Running the Applications
Start the Flask API server on http://localhost:5555:
- python server/app.py
- Start the React frontend on http://localhost:4000:
- npm start --prefix client
5. Testing the API
There are three ways to test the API:
1. Postman: Use the provided Postman collection (challenge-1-pizzas.postman_collection.json) to make requests to your API.
2. Import the collection by clicking the Import button in Postman.
3. Select the file and start testing the routes.
4. Pytest: Run the automated tests to validate your implementation:
- pytest -x
React Frontend: Run the React frontend and interact with the API via the UI.

## Models
This project includes three main models:
- Restaurant: Represents a pizza restaurant.
- Pizza: Represents a type of pizza.
- RestaurantPizza: A join table that connects restaurants and pizzas, with an additional price attribute.
## Model Relationships
* A Restaurant has many Pizzas through RestaurantPizza.
* A Pizza has many Restaurants through RestaurantPizza.
* A RestaurantPizza belongs to both a Restaurant and a Pizza.
Ensure that the relationships are properly configured in server/models.py and that cascading deletes are enabled for associated RestaurantPizzas when a Restaurant is deleted.

## Model Validations
The RestaurantPizza model includes a validation for the price field:
The price must be between 1 and 30.
API Routes:
1. GET /restaurants
Fetch all restaurants in the following format:

json
Copy code
[
  {
    "id": 1,
    "name": "Karen's Pizza Shack",
    "address": "123 Main St"
  },
  ...
]
2. GET /restaurants/int:id
Fetch a specific restaurant by ID, including its associated pizzas:

json
Copy code
{
  "id": 1,
  "name": "Karen's Pizza Shack",
  "address": "123 Main St",
  "restaurant_pizzas": [
    {
      "id": 1,
      "pizza": {
        "id": 1,
        "name": "Margherita",
        "ingredients": "Tomato, Cheese, Basil"
      },
      "price": 15
    }
  ]
}
If the restaurant is not found, it returns a 404 status code with an error message:

json
Copy code
{
  "error": "Restaurant not found"
}
3. DELETE /restaurants/int:id
Delete a specific restaurant and its associated RestaurantPizzas. If successful, return an empty response with a 204 status code. If the restaurant is not found, return a 404 status code with an error message:

json
Copy code
{
  "error": "Restaurant not found"
}
4. GET /pizzas
Fetch all pizzas in the following format:

json
Copy code
[
  {
    "id": 1,
    "name": "Margherita",
    "ingredients": "Tomato, Cheese, Basil"
  },
  ...
]
5. POST /restaurant_pizzas
Create a new RestaurantPizza to associate a pizza with a restaurant. The request body should include:

json
Copy code
{
  "pizza_id": 1,
  "restaurant_id": 3,
  "price": 12
}
If successful, return the created RestaurantPizza along with its associated Pizza and Restaurant:

json
Copy code
{
  "id": 5,
  "pizza_id": 1,
  "restaurant_id": 3,
  "price": 12,
  "pizza": {
    "id": 1,
    "name": "Margherita",
    "ingredients": "Tomato, Cheese, Basil"
  },
  "restaurant": {
    "id": 3,
    "name": "Kiki's Pizza",
    "address": "456 Elm St"
  }
}
If the creation fails due to validation errors (e.g., price out of range), return an error message with a 422 status code:

json
Copy code
{
  "errors": ["Price must be between 1 and 30"]
}
## Authors
This code was written by [Mark Wanjiku]
## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like
to change.