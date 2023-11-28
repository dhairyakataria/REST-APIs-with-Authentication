# REST-APIs-with-Authentication

## Description

This project is a REST API implementation with authentication using JWT tokens. It was developed to explore the authentication process using Flask and JWT in Python.

## Features

- Create a new user
- Delete a user
- User login and logout
- Get user by ID

## Authentication and Authorization

In a Flask web app using `flask_jwt_extended` for authentication and authorization, the process involves generating and validating JSON Web Tokens (JWT). Here's a general overview of how this process works:

### Installation

First, you need to install the necessary packages. You can use the following commands:

```bash
pip install Flask flask_jwt_extended flask_smorest
```

### Setup

Import the required modules and initialize your Flask app and the JWTManager:

```python
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
```

### User Authentication

When a user logs in, you can create a JWT and return it to the client. Typically, this is done after verifying the user's credentials:

```python
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app.route('/login', methods=['POST'])
def login():
    # Validate user credentials
    # ...

    # Create JWT token
    access_token = create_access_token(identity=username)
    return {'access_token': access_token}, 200
```

### Protecting Routes

Use the `@jwt_required` decorator to protect routes that require authentication. The `get_jwt_identity()` function retrieves the identity (usually the username) from the JWT:

```python
from flask_jwt_extended import get_jwt_identity, jwt_required

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'message': f'Hello, {current_user}!'}, 200
```

### Authorization

To handle authorization, you can use custom claims in the JWT. For example, you can include a "roles" claim to specify the user's roles:

```python
from flask_jwt_extended import jwt_required, get_jwt_claims

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    current_user_roles = get_jwt_claims()['roles']
    if 'admin' in current_user_roles:
        return {'message': 'Welcome, Admin!'}, 200
    else:
        return {'message': 'Unauthorized'}, 403
```

## Endpoints/APIs

- GET `/user/{id}`: Get user by ID
- POST `/user`: Create a new user
- DELETE `/user/{id}`: Delete user by ID
- POST `/login`: Login user and get JWT token
- POST `/logout`: Logout user and invalidate JWT token

## Technologies Used

- Flask
- Flask views
- Flask Smorest
- Flask JWT Extended
- MySQL (for database)
- Marshmallow (Python library)
- Hashlib (for password encryption)

## Database Schema

```sql
CREATE TABLE USER(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(30) NOT NULL,
    EMAIL VARCHAR(30) NOT NULL,
    U_PASSWORD VARCHAR(64) NOT NULL,
    U_ROLE VARCHAR(10)
);
```

---

Feel free to customize this template further based on your preferences or if you have additional information to include.
