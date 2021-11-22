from db import db

class LeadsModel(db.Model):

    __tablename__='Leads'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    status=db.Column(db.String,nullable=True)
    email=db.Column(db.String,nullable=True,unique=True)


    def __init__(self,name,status,email):
        self.name=name
        self.status=status
        self.email=email


    def json(self):
        return {"id":self.id,"name":self.name,"status":self.status,"email":self.email}


    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


