from flask_restful import Resource,reqparse
from models.sales import SalesModel
from datetime import datetime
from flask import Blueprint


from flask_jwt_extended import jwt_required,get_jwt_claims


parser=reqparse.RequestParser()

parser.add_argument("proposed_amount",
                    type=int,
                    required=True,
                    help="Enter proposed amount of project")

parser.add_argument("finalized_amount",
                    type=int,
                    required=True,
                    help="Enter finalized amount of project")

parser.add_argument("description",
                    type=str,
                    required=True,
                    help="Enter Description of sale")


parser.add_argument("status",
                    type=str,
                    required=True,
                    help="Enter Status of sale")

parser.add_argument("date",
                    type=str,
                    required=True,
                    help="Enter date of sale")

parser.add_argument("percentage_profit",
                    type=int,
                    required=True,
                    help="Enter profit of project")

parser.add_argument("project_id",
                    type=int,
                    required=True,
                    help="Enter project id of sale")


class Sales(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        data=parser.parse_args()
        try:
            date_obj=datetime.strptime(data['date'],'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"},400
        sale=SalesModel(data['proposed_amount'],data['finalized_amount'],data['status'],data['description'],
                        date_obj,data['percentage_profit'],data['project_id'])
        sale.save_to_db()
        return sale.json()

    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        sales = [sale.json() for sale in SalesModel.find_by_all()]
        return {"Sales":sales}


class Sale(Resource):

    @jwt_required
    def get(self,date):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        try:
            date_obj=datetime.strptime(date,'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"},400
        sales=SalesModel.find_by_date(date_obj)
        if sales:
            return sales
        return {"message":"no sale found on date {}".format(date)},400


class SpecificSale(Resource):

    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        sale=SalesModel.find_by_id(id)
        if sale:
            return sale.json()
        return {"message":"no sale found with id {}".format(id)},400

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        sale=SalesModel.find_by_id(id)
        if sale:
            sale.delete_from_db()
            return {"message":"sale deleted with id {}".format(id)}
        return {"message":"no sale found with id {}".format(id)},400

    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        data=parser.parse_args()
        sale=SalesModel.find_by_id(id)
        if sale:
            sale.proposed_amount=data['proposed_amount']
            sale.finalized_amount=data['finalized_amount']
            try:
                date_obj = datetime.strptime(data['date'], '%m-%d-%Y').date()
            except:
                return {"message": "Enter correct date format"}, 400
            sale.date=date_obj
            sale.status=data['status']
            sale.project_id=data['project_id']
            sale.description=data['description']
            sale.percentage_profit=data['percentage_profit']
            sale.save_to_db()
            return sale.json()
        return {"message":"no sale with id {}".format(id)},400



class FilterAmount(Resource):

    @jwt_required
    def get(self, amount):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        sale = SalesModel.find_by_finalized_amount(amount)
        if sale:
            return sale
        return {"message": "no sale found with {}".format(amount)}, 400
















