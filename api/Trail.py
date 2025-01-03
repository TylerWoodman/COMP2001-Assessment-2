from flask import jsonify, request, abort
from Models import Database, Trail
from sqlalchemy.sql import text
from marshmallow import Schema, fields, validate, ValidationError

#This is defining a schema called Trail_Schema that will validate and serialize trail data.
class Trail_Schema(Schema):
    Trail_ID = fields.Int(dump_only=True)
    Trail_Name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    Trail_Length = fields.Float(required=True, validate=validate.Range(min=0))
    Trail_Summary = fields.Str(validate=validate.Length(max=255))
    Trail_Description = fields.Str(validate=validate.Length(max=1000))
    Difficulty = fields.Str(validate=validate.OneOf(["Easy", "Medium", "Hard"]))
    Elevation_Gain = fields.Float(validate=validate.Range(min=0))
    Route_Type = fields.Str(validate=validate.OneOf(["Loop", "Point to Point"]))
    Owner_ID = fields.Int(required=True)
    Location_Point_1 = fields.Int(allow_none=True)
    Location_Point_2 = fields.Int(allow_none=True)
    Location_Point_3 = fields.Int(allow_none=True)
    Location_Point_4 = fields.Int(allow_none=True)
    Location_Point_5 = fields.Int(allow_none=True)

#Creating schema instances for serializing and de-serializing both one trail or mutliple trails.
Trail_schema = Trail_Schema()               #Schema for just one trail.
Trails_schema = Trail_Schema(many=True)     #Schema for mutliple trails.  

#A function to retreive all the trails within the database when called.
def Retrieve_All_Trails():
    All_Trails = Trail.query.all()
    return Trails_schema.dump(All_Trails), 200

#A function to retrieve a specific trail by its id.
def Retrieve_Trail_By_Id(Trail_ID):
    Retrieved_Trail = Trail.query.get(Trail_ID)
    if not Retrieved_Trail:
        abort(404, description=f"Trail with ID {Trail_ID} not found.")
    return Trail_schema.dump(Retrieved_Trail), 200

#A function to create a new trail into the database.
def Create_Trail():
    try:
        Trail_Data = request.get_json()
        Validated_Data = Trail_schema.load(Trail_Data)
        Created_Trail = Trail(**Validated_Data)
        Database.session.add(Created_Trail)
        Database.session.commit()
        return Trail_schema.dump(Created_Trail), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

#A function to update an existing trail. 
def Update_Trail(Trail_ID):
    try:
        Updated_Trail_Info = Trail.query.get(Trail_ID)
        if not Updated_Trail_Info:
            abort(404, description=f"Trail with ID {Trail_ID} not found.")
        Trail_Data = request.get_json()
        Validated_Data = Trail_schema.load(Trail_Data, partial=True)            #Deserializes and serializes the trail data. 
        for key, value in Validated_Data.items():   
            setattr(Updated_Trail_Info, key, value)                             #This will update the trails attributes.
        Database.session.commit()
        return Trail_schema.dump(Updated_Trail_Info), 200                       #This will return the updated trail.
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

#A function to delete an existing trail.
def Delete_Trail(Trail_ID):
    Deleted_Trail = Trail.query.get(Trail_ID)       #The query of the specified trail to be deleted.
    if not Deleted_Trail:
        abort(404, description=f"Trail with ID {Trail_ID} not found.")
    try:
        Database.session.execute(
            text("DELETE FROM [CW2].[Trail_Features_Link] WHERE Trail_ID = :trail_id"), #This will remove any related records from the trail feature link table.
            {"trail_id": Trail_ID}
        )
        Database.session.delete(Deleted_Trail)      #Deletes the trail from the database.
        Database.session.commit()                   #This will commit the session to save the changes made.           
        return '', 204
    except Exception as e:
        Database.session.rollback()                 #Rollback any changes if an error occurs throuhgout the process.
        abort(500, description=str(e))
