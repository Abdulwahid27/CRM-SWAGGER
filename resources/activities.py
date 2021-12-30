from flask_restful import Resource,reqparse
from models.activities import ActivitiesModel
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt_claims


parser=reqparse.RequestParser()


parser.add_argument("type",
                    type=str,
                    required=True,
                    help="Enter type of activity")

parser.add_argument("date",
                    type=str,
                    required=True,
                    help="Enter date for activity")

parser.add_argument("time",
                    type=str,
                    required=True,
                    help="Enter time of activity")

parser.add_argument("notes",
                    type=str,
                    required=True,
                    help="Enter notes of activity")

parser.add_argument("client_id",
                    type=int,
                    required=True,
                    help="Enter client id ")


class Activity(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        data=parser.parse_args()
        try:
            date_obj=datetime.strptime(data['date'],'%m-%d-%Y').date()
            time_obj=datetime.strptime(data['time'],'%H:%M:%S').time()
        except:
            return {"message":"Enter correct datetime format"},400

        activity=ActivitiesModel(data['type'],date_obj,time_obj,data['notes'],data['client_id'])
        activity.save_to_db()
        return activity.json()


class ActivitiesList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}

        activity=[activities.json() for activities in ActivitiesModel.find_by_all()]
        return {"Activities":activity}


class SpecificActivity(Resource):
    @jwt_required
    def get(self,date):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        try:
            date_obj=datetime.strptime(date,'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"},400

        activity=ActivitiesModel.find_by_date(date_obj)
        if activity:
            return activity
        return {"message":"no activity found on date {}".format(date_obj)},400

class Activityid(Resource):
    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        activity=ActivitiesModel.find_by_id(id)
        if activity:
            return activity.json()
        return {"message":"no acitvity with id {}".format(id)},400

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        activity = ActivitiesModel.find_by_id(id)
        if activity:
            activity.delete_from_db()
            return {"message":"activity with id {} deleted".format(id)}
        return {"message": "no acitvity with id {}".format(id)}, 400

    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        data=parser.parse_args()
        activity = ActivitiesModel.find_by_id(id)
        if activity:
            try:
                date_obj = datetime.strptime(data['date'], '%m-%d-%Y').date()
                time_obj = datetime.strptime(data['time'], '%H:%M:%S').time()
            except:
                return {"message": "Enter correct datetime format"}, 400
            activity.type=data['type']
            activity.date=date_obj
            activity.time=time_obj
            activity.notes=data['notes']
            activity.client_id=data['client_id']
            activity.save_to_db()
            return activity.json()
        return {"message": "no acitvity with id {}".format(id)}, 400

