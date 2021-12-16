from flask import Flask,jsonify
from flask_restful import Api
from models import user,client,projects,activities,sales,attendance,profit,leads,task
from resources.client import Client,ClientList,SpecificClient,ClientName,FilterByName,ClientStatus
from resources.projects import Projects,ProjectsList,ProjectDomain,SpecificProject,ProjectId,Filter,FilterProfit
from resources.user import User,UserLogin,UserLogout,UserRegister,TokenRefresh,Admin
from resources.leads import Leads,SpecificLead
from resources.activities import Activity,ActivitiesList,SpecificActivity,Activityid
from resources.profit import Profit
from resources.task import Task,SpecificTask,TaskByDate,filtername
from resources.sales import Sales,Sale,SpecificSale,FilterAmount
from resources.attendance import Attendance,specificAttendance,Attendance_by_date,AttendanceUpdation
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from flask_migrate import Migrate
from db import db





app=Flask(__name__)
api=Api(app)




app.secret_key='1234'

app.config['SQLALCHEMY_DATABASE_URI']='postgres://mqcrooqblxiyhl:556c8cb12388e61962159913868bde6b6c22d4f852d0e6b5cbf98a920dab1ce8@ec2-34-193-235-32.compute-1.amazonaws.com:5432/da6542lh56vtu3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']



jwt = JWTManager(app)


db.init_app(app)
migrate = Migrate(app, db)



@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.user_claims_loader
def add_claims_to_jwt(role):
    if role=="Admin" or "admin":
        return {'is_admin':True}
    return {'is_admin':False}



@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"Description":"Token has Expired",
                    "Error":"Token expired",
                    "Help":"Insert New Token"})

@jwt.invalid_token_loader
def Invalid_token_callback(error):
    return jsonify({"Description":"Signature verification failed",
                    "Error":"Invalid Token"})

@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return jsonify({"Description":"Request does not contain an access token",
                    "Error":"Authorization_required"})

@jwt.revoked_token_loader
def Revoked_token_callback():
    return jsonify({"Description":"Token as been revoked",
                    "Error":"Token_Revoked"})



api.add_resource(Client,'/clients')
api.add_resource(ClientList,'/clients')
api.add_resource(ClientName,'/clients/name/<string:name>')
api.add_resource(SpecificClient,'/clients/<int:id>')
api.add_resource(FilterByName,'/clients/search/<string:name>')
api.add_resource(ClientStatus,'/clients/status/<string:status>')

api.add_resource(Projects,'/projects/name/domain')
api.add_resource(ProjectDomain,'/projects/domain/<string:domain>')
api.add_resource(SpecificProject,'/projects/name/<string:name>')
api.add_resource(ProjectsList,'/projects')
api.add_resource(ProjectId,'/projects/<int:id>')
api.add_resource(Filter,'/projects/search/<string:name>')


api.add_resource(UserRegister,'/Register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login/<string:username>/<string:password>')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')
api.add_resource(Admin,'/Registeradmin')

api.add_resource(Activity,'/activity')
api.add_resource(ActivitiesList,'/activities')
api.add_resource(SpecificActivity,'/activity/<string:date>')
api.add_resource(Activityid,'/activity/<int:id>')


api.add_resource(Sales,'/sales')
api.add_resource(Sale,'/sales/<string:date>')
api.add_resource(SpecificSale,'/sales/<int:id>')
api.add_resource(FilterAmount,'/sales/search/<int:amount>')

api.add_resource(Attendance,'/attendance')
api.add_resource(specificAttendance,'/attendance/<int:id>')
api.add_resource(Attendance_by_date,'/attendance/<string:date>')
api.add_resource(AttendanceUpdation,'/attendance/<int:id>/<string:date>')
api.add_resource(FilterProfit,'/profit/<string:name>')


api.add_resource(SpecificLead,'/leads/<int:id>')
api.add_resource(Leads,'/leads')

api.add_resource(Task,'/tasks')
api.add_resource(SpecificTask,'/tasks/<int:id>')
api.add_resource(TaskByDate,'/tasks/<string:date>')
api.add_resource(filtername,'/task/<string:name>')


if __name__=='__main__':
    app.run(debug=True)