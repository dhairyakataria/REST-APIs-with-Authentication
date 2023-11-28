from flask import Flask, abort, request
from flask.views import MethodView
from db.user import UserDataBase, UserNotFoundException
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from blocklist import BLOCKLIST

from schemas.users import UserQuerySchema, UserSchema, SuccessMessageSchema, LoginSchema

# Create a Flask Blueprint for user operations
blp = Blueprint("users", __name__, description="Operations for users")

# Login endpoint
@blp.route("/login")
class login(MethodView):
    def __init__(self) -> None:
        self.db = UserDataBase()

    # POST method for user login
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(LoginSchema)
    def post(self, login_cred):
        try:
            # Verify user credentials
            user_id = self.db.verify_user(login_cred)
            if user_id:
                # Create and return an access token upon successful login
                return {"message": create_access_token(identity=user_id)}
            abort(401, message="Username or password is incorrect")  # 401 Unauthorized for failed login
        except Exception as e:
            abort(500, message=f"Internal Server Error: {str(e)}")

# Logout endpoint
@blp.route("/logout")
class UserLogout(MethodView):
    # POST method for user logout (requires JWT token)
    @jwt_required()
    def post(self):
        try:
            # Get JWT token ID and add it to the blocklist
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {'message': "Successfully logged out."}
        except Exception as e:
            abort(500, message=f"Internal Server Error: {str(e)}")

# User CRUD operations endpoint
@blp.route("/user")
class Users(MethodView):
    def __init__(self):
        self.db = UserDataBase()


    """Get user data by ID."""
    @blp.response(200, UserSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def get(self, args):
        try:
            id = args.get('id')
            result = self.db.get_user(id)
            print(result)
            return result
        except UserNotFoundException as e:
            # Handle the custom exception for user not found
            abort(404, message=str(e))
        except Exception as e:
            # Handle other exceptions with a 500 error
            abort(500, message=f"Internal Server Error: {str(e)}")


    """Add a new user."""
    @blp.response(201, SuccessMessageSchema)
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            if self.db.add_user(user_data):
                return {"message": "User added successfully"}, 201
            abort(403, message="User already exists")
        except Exception as e:
            abort(500, message=f"Internal Server Error: {str(e)}")


    """Delete a user by ID."""
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(UserQuerySchema, location="query")
    def delete(self, args):
        try:
            id = args.get('id')
            # Check if the user ID exists before attempting deletion
            if not self.db.delete_user(id):
                # If the user ID doesn't exist, raise UserNotFoundException
                raise UserNotFoundException(f"User with ID {id} not found")
            return {'message': 'User deleted successfully'}
        except UserNotFoundException as e:
            # Handle the custom exception for user not found with a 404 error
            abort(404, message=str(e))
        except Exception as e:
            # Handle other exceptions with a 500 error
            abort(500, message=f"Internal Server Error: {str(e)}")
