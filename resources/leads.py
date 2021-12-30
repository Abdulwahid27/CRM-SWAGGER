from flask_restful import Resource,reqparse
from models.leads import LeadsModel
import re
from flask_jwt_extended import jwt_required,get_jwt_claims

parser=reqparse.RequestParser()

parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Enter name of client")

parser.add_argument("status",
                    type=str,
                    required=False,
                    help="Enter status of client")

parser.add_argument("email",
                    type=str,
                    required=False,
                    help="Enter email of client")


class Leads(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}


        data=parser.parse_args()
        email_pattern = '^[a-zA-z 0-9]+[\._]?[a-zA-z 0-9]+[@]\w+[.]\w{3,7}$'
        lead=LeadsModel(data['name'],data['status'],data['email'])
        if lead.email ==None or re.search(email_pattern, data['email']):
            lead.save_to_db()
            return lead.json(),201
        return {"error":"enter correct email format"},400

    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        leads = [lead.json() for lead in LeadsModel.find_by_all()]
        return {"Leads": leads}

class SpecificLead(Resource):
    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        lead=LeadsModel.find_by_id(id)
        if lead:
            return lead.json()
        return {"error":"No lead found with id {}".format(id)}

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        lead=LeadsModel.find_by_id(id)
        if lead:
            lead.delete_from_db()
            return {"message":"lead {} deleted".format(id)},200
        return {"message":"no lead found with id {}".format(id)},400

    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        data=parser.parse_args()
        lead=LeadsModel.find_by_id(id)
        if lead:
            lead.name=data['name']
            lead.status=data['status']
            email_pattern = '^[a-zA-z 0-9]+[\._]?[a-zA-z 0-9]+[@]\w+[.]\w{3,7}$'
            if re.search(email_pattern,data['email']):
                lead.email=data['email']
                return lead.json(),200
            return {"error":"enter correct email format"},400
        return {"error":"no lead found with id {}".format(id)},400
