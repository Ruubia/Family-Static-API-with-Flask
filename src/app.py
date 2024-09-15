"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def create_member():
    
    body = request.get_json()

    member = {
        "id": body["id"],
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]

    }
    members = jackson_family.add_member(member)

    response_body = {
        
        "msg": "Added successfully",
        "family": members
        
    }


    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member():
    
    members = jackson_family.delete_member(member_id)


    if members: 
        response_body = {      
        "msg": "member deleted",
        "family": members        
    }

        return jsonify(response_body), 200

    return {"msg":"bad request, member does not exist so can not be deleted"}, 400


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):

    member = jackson_family.get_member(member_id)

    if member is None:
        return jsonify({"msg": "Bad request, member does not exist"}), 400

    return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
