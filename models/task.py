from db import db

class TaskModel(db.Model):

    __tablename__='Tasks'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    status=db.Column(db.String)
    detail=db.Column(db.Text)
    deadline=db.Column(db.Date)

    user_id=db.Column(db.Integer,db.ForeignKey('Users.id'))
    users=db.relationship('UserModel')



    def __init__(self,name,status,detail,deadline,user_id):
        self.name=name
        self.status=status
        self.detail=detail
        self.deadline=deadline
        self.user_id=user_id


    def json(self):
        return {"id":self.id,"name":self.name,"status":self.status,"detail":self.detail,"deadline":str(self.deadline),"user_id":self.user_id}

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def filter_by_name(cls, name):
        query = cls.query.filter(TaskModel.name.like('%{}%'.format(name))).all()
        names = [name.json() for name in query]
        return names


    @classmethod
    def find_by_date(cls,date):
        query=cls.query.filter_by(deadline=date).all()
        result=[x.json() for x in query]
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