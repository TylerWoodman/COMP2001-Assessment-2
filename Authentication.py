import jwt
import requests
import datetime
import os
from flask import Flask, request, jsonify

Authentication_Url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'  # URL of the external authentication service.
Secret_Key = os.getenv('SECRET_KEY')  # The secret key for signing JWT tokens. Must be set as an environment variable.
if not Secret_Key:
    raise ValueError("SECRET_KEY environment variable is not set!")  # Raise an error if the secret key is missing.

Token_Expiration = int(os.getenv('TOKEN_EXPIRATION', 1))  # How long until the token expires, in hours, default is 1 hour.

Flask_App = Flask(__name__)  # This will initialize the Flask application.

def Token_Generation(User_Email, User_Role):
    """
    Generate a JWT token for authenticated users.
    """
    Decoded_Token = {  # The data that will be encoded within the token.
        'User_Email_PL': User_Email,  # Payload containing the user email.
        'User_Role_PL': User_Role,  # Payload containing the user role.
        'Expiry': (datetime.datetime.utcnow() + datetime.timedelta(hours=Token_Expiration)).timestamp(),  # Token expiration.
        'Issued_At': datetime.datetime.utcnow().timestamp()  # Timestamp when the token was issued.
    }
    Jwt_Token = jwt.encode(Decoded_Token, Secret_Key, algorithm='HS256')  # Creating the token using the HS256 algorithm.
    print(f"Generated Token: {Jwt_Token}")  # Log the generated token for debugging.
    return Jwt_Token

def Token_Verification(Jwt_Token):
    """
    Verify and decode the JWT token.
    """
    try:
        print(f"Decoding Token: {Jwt_Token}")  # Log the token that is being decoded.
        Decoded_Token = jwt.decode(Jwt_Token, Secret_Key, algorithms=["HS256"])  # Decode the token.
        print(f"Decoded Payload: {Decoded_Token}")  # Log the decoded data for debugging.
        return Decoded_Token  # Return the decoded token if valid.
    except jwt.ExpiredSignatureError:  # Handle expired tokens.
        print("Token has expired")  # Log token expiration.
        return "Token has expired"
    except jwt.InvalidTokenError as e:  # Handle any invalid tokens.
        print(f"Invalid token error: {e}")  # Log the invalid token error.
        return "Invalid token"

def Bearer_Token_Verification(Jwt_Token):
    """
    Middleware to verify the Bearer token from the Authorization header.
    """
    print(f"Received Token: {Jwt_Token}")  # Log the token received from the header.
    if Jwt_Token.startswith("Bearer "):  # Check whether the token begins with the 'Bearer ' prefix.
        Jwt_Token = Jwt_Token.split(" ")[1]  # Extract the actual token from the input.
    else:
        print("Token does not have 'Bearer ' prefix")  # Log if the token does not have the correct prefix.

    Decoded_Token = Token_Verification(Jwt_Token)  # Decode and verify the token.
    if isinstance(Decoded_Token, str):  # Check whether the token verification returned an error or not.
        raise ValueError(f"Invalid token: {Decoded_Token}")  # If it is invalid, raise an error.
    return Decoded_Token  # Return the valid decoded token.

def User_Authentication():
    """
    Authenticate the user and return a JWT token if successful.
    """
    Authentication_Data = request.json  # Get the JSON payload from the HTTP request.
    if not Authentication_Data or 'email' not in Authentication_Data or 'password' not in Authentication_Data:
        return jsonify({'message': 'Email and password are required!'}), 400  # Return an error if input is invalid.

    try:
        # Send user credentials to the Authenticator API.
        response = requests.post(Authentication_Url, json=Authentication_Data, timeout=5)

        # Log the response for debugging.
        print(f"Authentication API Response: {response.status_code}, {response.text}")

        if response.status_code == 200:  # Check if the authentication was successful (HTTP 200 OK).
            Json_response = response.json()  # Parse the JSON response from the API.
           
            if isinstance(Json_response, list) and len(Json_response) == 2:
                key, value = Json_response  # Extract the elements of the list.
                if key == "Verified" and value == "True":  # This will check if the user is verified.
                    User_Email = Authentication_Data['email']
                    User_Role = "user"  # This will set the default role to 'user'.
                    Jwt_Token = Token_Generation(User_Email, User_Role)  # This will generate a JWT token for the user.
                    return jsonify({'token': Jwt_Token}), 200
                else:
                    return jsonify({'message': 'Authentication failed: User not verified'}), 401

            # Handle unexpected response structures.
            return jsonify({'message': 'Invalid response format from Authenticator API'}), 500

        else:
            # If the API response is not 200, return an error.
            return jsonify({'message': 'Authentication failed: Invalid email or password'}), response.status_code

    except Exception as e:
        # Log and handle unexpected errors during authentication.
        print(f"Error during authentication: {e}")
        return jsonify({'message': 'An error occurred during authentication'}), 500
