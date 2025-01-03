from flask_sqlalchemy import SQLAlchemy
Database = SQLAlchemy()

#This class represents the trail table in my database.
class Trail(Database.Model):
    __tablename__ = 'Trail'                 #The name of the table.
    __table_args__ = {'schema': 'CW2'}      #This is specifying the schema in which the table is. 
    
    #These are the columns for my Trail table with the constraints. 
    Trail_ID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Trail_Name = Database.Column(Database.String(100), nullable=False)
    Trail_Length = Database.Column(Database.Numeric(5, 2), nullable=False)
    Trail_Summary = Database.Column(Database.String(255), nullable=True)
    Trail_Description = Database.Column(Database.String(1000), nullable=True)
    Difficulty = Database.Column(Database.String(50), nullable=True)
    Elevation_Gain = Database.Column(Database.Numeric(5, 2), nullable=True)
    Route_Type = Database.Column(Database.String(50), nullable=True)
    Owner_ID = Database.Column(Database.Integer, Database.ForeignKey('CW2.Users.User_ID'), nullable=False)
    Location_Point_1 = Database.Column(Database.Integer, Database.ForeignKey('CW2.Location_Points.Location_Point_ID'), nullable=True)
    Location_Point_2 = Database.Column(Database.Integer, Database.ForeignKey('CW2.Location_Points.Location_Point_ID'), nullable=True)
    Location_Point_3 = Database.Column(Database.Integer, Database.ForeignKey('CW2.Location_Points.Location_Point_ID'), nullable=True)
    Location_Point_4 = Database.Column(Database.Integer, Database.ForeignKey('CW2.Location_Points.Location_Point_ID'), nullable=True)
    Location_Point_5 = Database.Column(Database.Integer, Database.ForeignKey('CW2.Location_Points.Location_Point_ID'), nullable=True)

#This is a method that will help convert a Trail object into a JSON format.
    def Convert_To_JSON(self):
        return {
            "Trail_ID": self.Trail_ID,
            "Trail_Name": self.Trail_Name,
            "Trail_Length": float(self.Trail_Length),
            "Trail_Summary": self.Trail_Summary,
            "Trail_Description": self.Trail_Description,
            "Difficulty": self.Difficulty,
            "Elevation_Gain": float(self.Elevation_Gain) if self.Elevation_Gain is not None else None,
            "Route_Type": self.Route_Type,
            "Owner_ID": self.Owner_ID,
            "Location_Point_1": self.Location_Point_1,
            "Location_Point_2": self.Location_Point_2,
            "Location_Point_3": self.Location_Point_3,
            "Location_Point_4": self.Location_Point_4,
            "Location_Point_5": self.Location_Point_5,
        }

#This class is for my Location Points table in the database.
class Location_Point(Database.Model):
    __tablename__ = 'Location_Points'
    __table_args__ = {'schema': 'CW2'}
    
    Location_Point_ID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Point_Latitude = Database.Column(Database.Numeric(9, 6), nullable=False)
    Point_Longitude = Database.Column(Database.Numeric(9, 6), nullable=False) 
    Point_Description = Database.Column(Database.String(255), nullable=True)

#This converts the location point object into JSON. 
    def Convert_To_JSON(self):
        return {
            "Location_Point_ID": self.Location_Point_ID,
            "Point_Latitude": str(self.Point_Latitude),
            "Point_Longitude": str(self.Point_Longitude),
            "Point_Description": self.Point_Description
        }

class User(Database.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    
    User_ID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Email = Database.Column(Database.String(100), unique=True, nullable=False)
    User_Role = Database.Column(Database.String(50), nullable=False)

    def Convert_To_JSON(self):
        return {
            "User_ID": self.User_ID,
            "Email": self.Email,
            "User_Role": self.User_Role
        }

class Trail_Feature(Database.Model):
    __tablename__ = 'Trail_Features'
    __table_args__ = {'schema': 'CW2'}
    
    Feature_ID = Database.Column(Database.Integer, primary_key=True, autoincrement=True)
    Feature_Description = Database.Column(Database.String(100), nullable=False)

    def Convert_To_JSON(self):
        return {
            "Feature_ID": self.Feature_ID,
            "Feature_Description": self.Feature_Description
        }

class Trail_Feature_Link(Database.Model):
    __tablename__ = 'Trail_Features_Link'
    __table_args__ = {'schema': 'CW2'}
    
    Trail_ID = Database.Column(Database.Integer, Database.ForeignKey('CW2.Trail.Trail_ID'), primary_key=True, nullable=False)
    Feature_ID = Database.Column(Database.Integer, Database.ForeignKey('CW2.Trail_Features.Feature_ID'), primary_key=True, nullable=False)

    def Convert_To_JSON(self):
        return {
            "Trail_ID": self.Trail_ID,
            "Feature_ID": self.Feature_ID
        }
