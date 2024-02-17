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

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({ "err_msg": "Internal Server Error" }), 500

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({ "err_msg": "Member not found" }), 404
    
@app.route('/member', methods=['POST'])
def add_member():
    try:
        member_data = request.json
        if not member_data:
            raise APIException("Request must be a valid JSON", status_code=400)
        if "first_name" not in member_data or "age" not in member_data or "lucky_numbers" not in member_data:
            raise APIException("Missing required data", status_code=400)

        jackson_family.add_member(member_data)
        return jsonify({ "msg": "Member successfully created" }), 201
    except Exception as e:
        print(e)
        return jsonify({ "err_msg": "Internal Server Error" }), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if deleted:
            return jsonify({ "done": True }), 200
        else:
            return jsonify({ "err_msg": "Member not found" }), 404
    except Exception as e:
        print(e)
        return jsonify({ "err_msg": "Internal Server Error" }), 500
    
@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        member_data = request.json
        if not member_data:
            raise APIException("Request must be a valid JSON", status_code=400)
        if "first_name" not in member_data or "age" not in member_data or "lucky_numbers" not in member_data:
            raise APIException("Missing required data", status_code=400)

        success = jackson_family.update_member(member_id, member_data)
        if success:
            return jsonify({ "msg": "Member updated successfully" }), 200
        else:
            return jsonify({ "err_msg": "Member not found" }), 404
    except Exception as e:
        print(e)
        return jsonify({ "err_msg": "Internal Server Error" }), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
