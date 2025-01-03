import jwt
import requests
import datetime
import os
from flask import Flask, request, jsonify

Authentication_Url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'     #URL of the external authentication service. 
Secret_Key = os.getenv('SECRET_KEY', 'secret_key')                                  #The secret key for signing jwt tokens. 
Token_Expiration = 1                                                                #How long until the token expires , in hours.     

Flask_App = Flask(__name__)                             #This will initalize the flask application.

def Token_Generation(User_Email, User_Role):
    """
    Generate a JWT token for authenticated users.
    """
    Decoded_Token = {                                   #The data that will be within the token. 
        'User_Email_PL': User_Email,
        'User_Role_PL': User_Role,
        'Expiry': (datetime.datetime.utcnow() + datetime.timedelta(hours=Token_Expiration)).timestamp(), #Token expiration 
        'Issued_At': datetime.datetime.utcnow().timestamp()  #When the token was issued.                                   
    }
    Jwt_Token = jwt.encode(Decoded_Token, Secret_Key, algorithm='HS256') #Creating the token using the HS256 Algorithm.
    print(f"Generated Token: {Jwt_Token}")  
    return Jwt_Token

def Token_Verification(Jwt_Token):
    """
    Verify and decode the JWT token.
    """
    try:
        print(f"Decoding Token: {Jwt_Token}")  
        Decoded_Token = jwt.decode(Jwt_Token, Secret_Key, algorithms=["HS256"])  #Decode the token.
        print(f"Decoded Payload: {Decoded_Token}")  #Log the decoded data.
        return Decoded_Token   #Return the decoded token. 
    except jwt.ExpiredSignatureError:  #Handle expired tokens. 
        print("Token has expired")  
        return "Token has expired"
    except jwt.InvalidTokenError as e:      #Handles any invalid tokens. 
        print(f"Invalid token error: {e}")  
        return "Invalid token"

def Bearer_Token_Verification(Jwt_Token):
    """
    Middleware to verify the Bearer token from the Authorization header.
    """
    print(f"Received Token: {Jwt_Token}")    #This will log the token from the header.
    if Jwt_Token.startswith("Bearer "):         #To check whether the token begins with a Bearer. 
        Jwt_Token = Jwt_Token.split(" ")[1]     #To extract the actualy token from the input.
    else:
        print("Token does not have 'Bearer ' prefix")  

    Decoded_Token = Token_Verification(Jwt_Token)       #This will decode and verify the token.
    if isinstance(Decoded_Token, str):                  #This will check whether the token verification returned an error or not.
        raise ValueError(f"Invalid token: {Decoded_Token}")     #If it is invalid then an error is raised.
    return Decoded_Token        #This will return the valid decoded token. 

def User_Authentication():
    """
    Authenticate the user and return a JWT token if successful.
    """
    Authentication_Data = request.json     #This will get the JSON Payload from the HTTP request.
    if not Authentication_Data or 'email' not in Authentication_Data or 'password' not in Authentication_Data:   #Validating the input.
        return jsonify({'message': 'Email and password required!'}), 400        #If the input is invalid then return an error. 

    response = requests.post(Authentication_Url, json=Authentication_Data)      #Sends the user details to the authentication service. 
    if response.status_code == 200:         #200 to show if the authentication was successful. 
        try:
            Json_response = response.json()     #This will parse the JSON response.
            if isinstance(Json_response, list) and 'Verified' in Json_response: #To checl whether Verified is within the response.
                User_Email = Authentication_Data['email']       #Extarct the user email.
                User_Role = 'user'          #Set the default role to user, out of user and admin.
                Jwt_Token = Token_Generation(User_Email, User_Role)     #This will generate a JWT token for the user.
                return jsonify({'token': Jwt_Token}), 200
        except requests.JSONDecodeError:
            return jsonify({'message': 'Invalid response from Authenticator API'}), 500
    else:
        return jsonify({'message': 'Authentication failed!'}), response.status_code
