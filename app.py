from flask import Flask, request
from blocklist import BLOCKLIST
from routes.users import blp as UserBluePrint
from flask_smorest import Api
from flask_jwt_extended import JWTManager

# Create a Flask app
app = Flask(__name__)

# Configuration for Flask-Smorest and Flask-JWT-Extended
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Users Rest API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Secret key for JWT
app.config["JWT_SECRET_KEY"] = "d8deb755-84fb-40cb-be01-760f8e62a978"

# Initialize Flask-Smorest API and Flask-JWT-Extended
api = Api(app)
jwt = JWTManager(app)

# Register the User Blueprint
api.register_blueprint(UserBluePrint)

# JWT token blocklist loader
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # Check if the token's JTI (JWT ID) is in the blocklist
    return jwt_payload["jti"] in BLOCKLIST

# Revoked token loader callback
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    # Return a response for revoked tokens
    return (
        {
            "description": "User has been logged out",
            "error": "token_revoked"
        },
        401
    )
