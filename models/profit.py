from db import db

class ProfitModel(db.Model):

    __tablename__='profits'

    id=db.Column(db.Integer,primary_key=True)
    project_name=db.Column(db.String,unique=True)
    profit=db.Column(db.Integer)


    def __init__(self,project_name,profit):
        self.project_name=project_name
        self.profit=profit


    def json(self):
        return {"id":self.id,"project_name":self.project_name,"profit":self.profit}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(project_name=name).first()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

