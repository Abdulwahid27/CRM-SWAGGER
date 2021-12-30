from db import db

class ProjectModel(db.Model):

    __tablename__='Projects'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False,unique=True)
    domain=db.Column(db.String,nullable=False)
    description=db.Column(db.Text)

    client_id=db.Column(db.Integer,db.ForeignKey('Clients.id'))
    clients=db.relationship('ClientModel')

    users=db.relationship('UserModel',lazy='dynamic')
    sales=db.relationship('SalesModel',lazy='dynamic')


    def __init__(self,name,domain,description,client_id):
        self.name=name
        self.domain=domain
        self.description=description
        self.client_id=client_id



    def json(self):
        return {"id":self.id,"name":self.name,"domain":self.domain,
                "description":self.description,"client_id":self.client_id,"Cost":[sale.json() for sale in self.sales],
                "users":[user.json() for user in self.users]}


    @classmethod
    def find_by_project_domain(cls,domain):
        query= cls.query.filter_by(domain=domain).all()
        names = [x.json() for x in query]
        return names


    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def find_by_project_name(cls,name):
        query= cls.query.filter_by(name=name).first()
        return query


    @classmethod
    def find_by_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_name(cls, name):
        query = cls.query.filter(ProjectModel.name.like('%{}%'.format(name))).all()
        names = [x.json() for x in query]
        return names


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()