from db import db

class ActivitiesModel(db.Model):
    __tablename__='Activities'

    id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.String,nullable=False)
    date=db.Column(db.Date)
    time=db.Column(db.Time)
    notes=db.Column(db.Text)
    client_id=db.Column(db.Integer,db.ForeignKey('Clients.id'))
    clients=db.relationship('ClientModel')


    def __init__(self,type,date,time,notes,client_id):
        self.type=type
        self.date=date
        self.time=time
        self.notes=notes
        self.client_id=client_id


    def json(self):
        return {"id":self.id,"type":self.type,"date":str(self.date),"time":str(self.time),"notes":self.notes,"client id":self.client_id}

    @classmethod
    def find_by_date(cls,date):
        query= cls.query.filter_by(date=date).all()
        data= [activity.json() for activity in query]
        return data

    @classmethod
    def find_by_id(cls, id):
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

