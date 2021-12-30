from flask_restful import Resource,reqparse
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_refresh_token_required,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_claims,
                                get_raw_jwt
                                )
from models.user import UserModel
from blacklist import BLACKLIST



_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
                    type=str,
                    required=True,
                    help="Enter a username")

_user_parser.add_argument("password",
                    type=str,
                    required=True,
                    help='Enter a password')

_user_parser.add_argument("role",
                    type=str,
                    required=True,
                    help='Enter a role')

_user_parser.add_argument("project_id",
                    type=int,
                    required=True,
                    help='Enter a project id')

class Admin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        roles=['Admin','admin']
        if data['role'] in roles:
            user = UserModel(data['username'], data['role'], data['password'],data['project_id'])
            user.save_to_db()
            return {"message": "admin created successfully"}, 201
        return {"message":"Invalid input for role!"},400


class UserRegister(Resource):
    @jwt_required
    def post(self):
        data = _user_parser.parse_args()
        user=UserModel.find_by_username(data['username'])
        claims=get_jwt_claims()
        if not claims['is_admin']:
            return {"message":"Admin privelege required"}
        if user:
            return{"message":"User already exits!"},400

        roles = ['Employee','employee']

        if data['role'] in roles:
            user=UserModel(data['username'],data['role'],data['password'],data['project_id'])
            user.save_to_db()
            return {"message":"USER CREATED SUCCESSFULLY"},201

        return {"message": "Invalid input for role!"}, 400




class User(Resource):
    @jwt_required
    def get(self, user_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {"message":"No user found"},400


    @jwt_required
    def delete(cls,user_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        user=UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"message":"User with id {} deleted".format(user_id)}
        return {"message":"No user found"},400



class UserLogin(Resource):

    @classmethod
    def post(cls,username,password):

        user=UserModel.find_by_username(username)
        if user and user.password == password:
            access_token=create_access_token(identity=user.role,fresh=True)
            refresh_token=create_refresh_token(user.role)
            return {"Access_token":access_token,
                    "Refreshing_token":refresh_token}
        return {"message":"Invalid credentials!"}

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti=get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message":"Successfully logged out"},200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user= get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        return {"Access_token":new_token}

