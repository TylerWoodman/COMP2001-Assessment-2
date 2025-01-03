import connexion
from Models import Database
from Authentication import User_Authentication, Bearer_Token_Verification

 #This is the database configuration details, this will help me link to my sql server.
Database_Configuration = {                          
    "username": "TWoodman",
    "password": "ZcxX595+",
    "server": "dist-6-505.uopnet.plymouth.ac.uk",
    "database": "COMP2001_TWoodman",
    "driver": "ODBC+Driver+17+for+SQL+Server",
}

 #This connection string is constructed for SQLalchemy to connect to the database.
Connection_String = (                               
    f"mssql+pyodbc://{Database_Configuration['username']}:{Database_Configuration['password']}@"
    f"{Database_Configuration['server']}/{Database_Configuration['database']}"
    f"?driver={Database_Configuration['driver']}&TrustServerCertificate=yes&Encrypt=yes"
)

#These two lines are initliazing the connexion app and the flask app.
Connexion_App = connexion.App(__name__, specification_dir="./")     
Flask_App = Connexion_App.app

# Here we are configuring the flask app using the connection string.
Flask_App.config['SQLALCHEMY_DATABASE_URI'] = Connection_String     
Flask_App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#This will initialize the database with the flask app.
Database.init_app(Flask_App)

#This line will add the api specifications from the swagger file. 
Connexion_App.add_api("Swagger.yml", options={"swagger_ui": True}, arguments={"bearerInfoFunc": Bearer_Token_Verification})

#This is the main point of entry for the app.
if __name__ == "__main__":
    with Flask_App.app_context():
        Database.create_all()               #This will ensure that all databases are created before running the app.
    Connexion_App.run(use_reloader=True)    #This will run the connexion app with auti-reload enabled. 

