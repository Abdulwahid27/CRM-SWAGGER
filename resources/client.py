from flask_restful import Resource,reqparse
from models.client import ClientModel
import re
from flask_jwt_extended import jwt_required,get_jwt_claims



user_parser=reqparse.RequestParser()

user_parser.add_argument("name",
                         type=str,
                         required=True,
                         help="Enter name of client")


user_parser.add_argument("gender",
                         type=str,
                         required=True,
                         help="Enter Gender of client")

user_parser.add_argument("email",
                         type=str,
                         required=True,
                         help="Enter email of client")

user_parser.add_argument("country",
                         type=str,
                         required=True,
                         help="Enter country")


user_parser.add_argument("phone",
                         type=str,
                         required=False,
                         help="Enter Phone Number of client")


user_parser.add_argument("status",
                         type=str,
                         required=True,
                         help="Enter Status of client")

user_parser.add_argument("description",
                         type=str,
                         required=True,
                         help="Enter Description of client")


class Client(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        data=user_parser.parse_args()
        email_pattern='^[a-zA-z 0-9]+[\._]?[a-zA-z 0-9]+[@]\w+[.]\w{3,7}$'
        if re.search(email_pattern,data['email']):
            if ClientModel.find_by_email(data['email']):
                return {"Error":"That Email already Exists!"},400
        else:
            return {"ERROR":"Enter Correct Email Address"},400


        gender=['Male','Female','male','female','FEMALE','MALE']
        status=['active','Active','inactive','Inactive']

        if ClientModel.find_by_phone(data['phone']):
            return {"Error":"This Phone number is Occupied"},400

        if data['gender'] in gender:
            if data['status'] in status:
                client=ClientModel(data['name'],data['gender'],data['email'],data['country'],data['phone'],data['status'],data['description'])
                client.save_to_db()
                return client.json(),201

            return {"error":"Invalid input for status!"},400
        return {"error":"Invalid input for gender!"},400


    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        clients=[client.json() for client in ClientModel.find_by_all()]
        return {"Clients":clients}



class ClientName(Resource):
    @jwt_required
    def get(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        client=ClientModel.find_by_name(name)
        if client:
            return client
        return {"MESSAGE":"No client with name {} found".format(name)},400

class SpecificClient(Resource):
    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        client=ClientModel.find_by_id(id)
        if client:
            return client.json()
        return {"MESSAGE": "No client with id {}".format(id)},400

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        client=ClientModel.find_by_id(id)
        if client:
            client.delete_from_db()
            return {"MESSAGE":"client {} with id {} deleted".format(client.name,id)}
        return {"MESSAGE":"No client with id {}".format(id)},400

    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        data=user_parser.parse_args()
        client=ClientModel.find_by_id(id)
        email_pattern = '^[a-zA-z 0-9]+[\._]?[a-zA-z 0-9]+[@]\w+[.]\w{3,7}$'
        if client:
            client.name=data['name']
            if re.search(email_pattern, data['email']):
                client.email=data['email']
                client.gender=data['gender']
                client.phone=data['phone']
                client.country=data['country']
                client.status=data['status']
                client.save_to_db()
                return client.json()
            return {"error": "enter correct email"},400

        return {"MESSAGE": "No client with id {}".format(id)},400


class FilterByName(Resource):
    @jwt_required
    def get(self,name):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        client=ClientModel.filter_by_name(name)
        if client:
            return client
        return {"message":"no client with name {}".format(name)},400


class ClientStatus(Resource):
    @jwt_required
    def get(self,status):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        client=ClientModel.find_by_status(status)
        Status = ['active', 'Active', 'inactive', 'Inactive']
        if status in Status:
            if client:
                return client
            return {"message":"No client found with status specified"},400
        return {"message":"invalid input for status"},400
