from db import db

class AttendanceModel(db.Model):

    __tablename__='Attendance'

    id=db.Column(db.Integer,primary_key=True)
    attendance=db.Column(db.String)
    status=db.Column(db.Boolean,nullable=False)
    date=db.Column(db.Date)
    time=db.Column(db.Time)

    user_id=db.Column(db.Integer,db.ForeignKey('Users.id'))
    users=db.relationship('UserModel')


    def __init__(self,attendance,status,date,time,user_id):
        self.attendance=attendance
        self.status=status
        self.date=date
        self.time=time
        self.user_id=user_id


    def json(self):
        return {"id":self.id,"attendance":self.attendance,"status":self.status,"date":str(self.date),"time":str(self.time),"user_id":self.user_id}


    @classmethod
    def find_by_id(cls,int):
        return cls.query.filter_by(id=int).first()

    @classmethod
    def find_by_user_id(cls,id):
        query= cls.query.filter_by(user_id=id).all()
        result=[attend.json() for attend in query]
        return result

    @classmethod
    def specific_user_attendance(cls,id,date):
        return cls.query.filter_by(user_id=id,date=date).first()

    @classmethod
    def find_by_date(cls,date):
        query=cls.query.filter_by(date=date).all()
        result=[dates.json() for dates in query]
        return result


    @classmethod
    def find_by_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()







