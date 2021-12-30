from flask_restful import Resource,reqparse
from models.attendance import AttendanceModel
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt_claims



parser=reqparse.RequestParser()

parser.add_argument("attendance",
                    type=str,
                    required=True,
                    help="Enter attendance")

parser.add_argument("status",
                    type=bool,
                    required=True,
                    help="Enter status ")

parser.add_argument("user_id",
                    type=int,
                    required=True,
                    help="Enter user id for attendance")


class Attendance(Resource):
    @jwt_required
    def post(self):
        data=parser.parse_args()
        try:
            current_date = datetime.now()
            date_obj = current_date.date().strftime('%m-%d-%Y')
            converted_date = datetime.strptime(date_obj, '%m-%d-%Y').date()
            time_obj = current_date.time().strftime("%H:%M %S")
            converted_time = datetime.strptime(time_obj, "%H:%M %S").time()

        except:
            return {"Syntax Error": "Enter correct datetime format"},400
        attend=['present','absent','Present','Absent']

        attendance = AttendanceModel.specific_user_attendance(data['user_id'], converted_date)


        if data['attendance'] in attend:

            if attendance:
                return {"message":"Attendance marked already"},400


            attendance=AttendanceModel(data['attendance'],data['status'],converted_date,converted_time,data['user_id'])

            attendance.save_to_db()
            return attendance.json(),201
        return {"message":"Invalid input for attendance"}

    @jwt_required
    def get(self):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        attendance=[attend.json() for attend in AttendanceModel.find_by_all()]
        return {"Attendance":attendance}


class specificAttendance(Resource):
    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        attend=AttendanceModel.find_by_user_id(id)
        if attend:
            return attend
        return {"error":"No attendance found of user {}".format(id)},400

    @jwt_required
    def delete(self,id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        attend=AttendanceModel.find_by_id(id)
        if attend:
            attend.delete_from_db()
            return {"message":"attendance with id {} deleted".format(id)}
        return {"message":"No user found"},400



class Attendance_by_date(Resource):
    @jwt_required
    def get(self,date):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        try:
            converted_date = datetime.strptime(date,'%m-%d-%Y').date()
        except:
            return {"message":"Enter correct date format"}
        attend = AttendanceModel.find_by_date(converted_date)
        if attend:
            return attend
        return {"message":"no attendance on date {}".format(converted_date)},400


class AttendanceUpdation(Resource):
    @jwt_required
    def put(self,id,date):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {"message": "Admin privelege required"}
        data=parser.parse_args()
        try:
            current_date = datetime.now()
            converted_date = datetime.strptime(date, '%m-%d-%Y').date()
            time_obj = current_date.time().strftime("%H:%M %S")
            converted_time = datetime.strptime(time_obj, "%H:%M %S").time()

        except:
            return {"Syntax Error": "Enter correct datetime format"}, 400
        attendance = AttendanceModel.specific_user_attendance(id,converted_date)
        syntax_of_attend = ['present', 'absent', 'Present', 'Absent']
        if attendance:


            if data['attendance'] in syntax_of_attend:
                attendance.attendance=data['attendance']

                attendance.time=converted_time
                attendance.save_to_db()
                return attendance.json()

            return {"message":"Invalid input for attendance"},400
        return {"message":"no attendance found"},400

