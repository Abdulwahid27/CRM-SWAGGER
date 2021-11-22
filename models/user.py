from db import db

class UserModel(db.Model):
    __tablename__='Users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    role=db.Column(db.String)
    password=db.Column(db.String(50))

    project_id=db.Column(db.Integer,db.ForeignKey('Projects.id'))
    projects=db.relationship('ProjectModel')

    attendance=db.relationship('AttendanceModel',lazy='dynamic')
    tasks=db.relationship('TaskModel',lazy='dynamic')

    def __init__(self,username,role,password,project_id):
        self.username = username
        self.role=role
        self.password = password
        self.project_id=project_id

    def json(self):
        return {"id":self.id,
                "username":self.username,
                "role":self.role,
                "project_id":self.project_id,
                "attendance":[attendance.json() for attendance in self.attendance],
                "tasks":[task.json() for task in self.tasks]}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()