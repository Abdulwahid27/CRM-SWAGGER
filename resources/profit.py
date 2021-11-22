from flask_restful import Resource,reqparse
from models.profit import ProfitModel
from resources.sales import SalesModel



class Profit(Resource):
    def get(self,name):

        result=(SalesModel.profit * SalesModel.finalized_amount)/100
        info=ProfitModel(name,profit=result)

        info.save_to_db()
        return info.json()



