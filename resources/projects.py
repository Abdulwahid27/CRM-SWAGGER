from flask_restful import Resource,reqparse
from models.projects import ProjectModel

from flask_jwt_extended import jwt_required,get_jwt_claims


parser=reqparse.RequestParser()

parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Enter name of project")

parser.add_argument("domain",
                    type=str,
                    required=True,
                    help="Enter domain of project")

parser.add_argument("client_id",
                    type=int,
                    required=True,
                    help="Enter id of client")

parser.add_argument("description",
                    type=str,
                    required=True,
                    help="Enter Description of client")



class Projects(Resource):
    def post(self):
        data=parser.parse_args()


        project=ProjectModel(data['name'],data['domain'],data['description'],data['client_id'])
        project.save_to_db()
        return project.json(), 201

class ProjectsList(Resource):
    @jwt_required
    def get(self):
        projects=[project.json() for project in ProjectModel.find_by_all()]
        return {"projects":projects}

class SpecificProject(Resource):
    @jwt_required
    def get(self,name):
        projects=ProjectModel.find_by_project_name(name)
        if projects:
            return projects
        return {"message":"no project found with name {} ".format(name)},400

    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        projects = ProjectModel.find_by_project_name(name)
        if projects:
            projects.delete_from_db()
            return {"message":"project with name {} deleted".format(name)}

        return {"message": "no project found with name {} ".format(name)},400



class ProjectDomain(Resource):
    @jwt_required
    def get(self,domain):
        projects=ProjectModel.find_by_project_domain(domain)
        if projects:
            return projects
        return {"message":"no project found with domain {} ".format(domain)},400


class ProjectId(Resource):

    @jwt_required
    def get(self,id):
        projects=ProjectModel.find_by_id(id)
        if projects:
            return projects.json()
        return {"message": "No project found with id {}".format(id)},400


    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        projects = ProjectModel.find_by_id(id)
        if projects:
            projects.delete_from_db()
            return {"message":"project with name {} deleted".format(projects.name)}

        return {"message":"No project found with id {}".format(id)},400

    @jwt_required
    def put(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        data=parser.parse_args()
        projects = ProjectModel.find_by_id(id)
        if projects:
            projects.name=data['name']
            projects.domain=data['domain']
            projects.client_id=data['client_id']
            projects.description=data['description']
            projects.save_to_db()
            return projects.json()
        return {"message": "no project found with id {} ".format(id)},400


class Filter(Resource):

    @jwt_required
    def get(self,name):
        client=ProjectModel.filter_by_name(name)
        if client:
            return client
        return {"message":"no client with name {}".format(name)},400


class FilterProfit(Resource):
    def get(self,name):
        profit=ProjectModel.profit_by_name(name)
        if profit:
            calculation = [x.json() for x in profit.sales]

            c = [(x['finalized_amount'] * y['percentage_profit'] / 100, x['finalized_amount'],y['percentage_profit']) for x, y in zip(calculation, calculation)]

            return {"Info":c}
        return {"Message":"No project found with name {}".format(name)}



