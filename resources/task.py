from flask_restful import Resource,reqparse
from models.task import TaskModel
from datetime import datetime

parser=reqparse.RequestParser()

parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Enter name of project")

parser.add_argument("status",
                    type=str,
                    required=False,
                    help="Enter status of task")

parser.add_argument("detail",
                    type=int,
                    required=False,
                    help="Enter detail of task")

parser.add_argument("deadline",
                    type=str,
                    required=True,
                    help="Enter deadline of task")

parser.add_argument("user_id",
                    type=int,
                    required=True,
                    help="Enter user id")

class Task(Resource):
    def post(self):
        data=parser.parse_args()
        try:
            date_obj=datetime.strptime(data['deadline'],'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"},400
        tasks=TaskModel(data['name'],data['status'],data['detail'],date_obj,data['user_id'])
        tasks.save_to_db()
        return tasks.json(),201

    def get(self):
        tasks=[x.json for x in TaskModel.find_by_all()]
        return tasks,200


class SpecificTask(Resource):
    def get(self,id):
        task=TaskModel.find_by_id(id)
        if task:
            return task.json(),200
        return {"error":"No task found with id {}".format(id)},400

    def delete(self,id):
        task=TaskModel.find_by_id(id)
        if task:
            task.delete_from_db()
            return {"message":"task with id {} deleted".format(id)},200
        return {"error":"no task found with id {}".format(id)},400

    def put(self,id):
        data=parser.parse_args()
        task=TaskModel.find_by_id(id)
        if task:
            task.name=data['name']
            task.status=data['status']
            task.detail=data['detail']
            try:
                date_obj = datetime.strptime(data['deadline'], '%m-%d-%Y').date()
            except:
                return {"message": "Enter correct date format"}, 400
            task.deadline=date_obj
            task.user_id=data['user_id']
            task.save_to_db()
            return task.json(),200


class TaskByDate(Resource):
    def get(self,date):
        try:
            date_obj=datetime.strptime(date,'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"},400
        task=TaskModel.find_by_date(date_obj)
        if task:
            return task
        return {"error":"no date {} found".format(date)},400


class filtername(Resource):
    def get(self,name):
        task=TaskModel.filter_by_name(name)
        if task:
            return task,200
        return {"error":"No task with name {}".format(name)},400






