from db import db

class ClientModel(db.Model):

    __tablename__='Clients'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    gender=db.Column(db.String)
    email=db.Column(db.String)
    country=db.Column(db.String)
    phone=db.Column(db.String,nullable=True)
    status=db.Column(db.String)
    description=db.Column(db.Text)

    projects = db.relationship('ProjectModel', lazy='dynamic')
    activities=db.relationship('ActivitiesModel',lazy='dynamic')


    def __init__(self,name,gender,email,country,phone,status,description):
        self.name=name
        self.gender=gender
        self.email=email
        self.country=country
        self.phone=phone
        self.status=status
        self.description=description


    def json(self):
        return {"id":self.id,"name":self.name,"gender":self.gender,"email":self.email,"country":self.country,
                "phone":self.phone,"status":self.status,"description":self.description,
                "projects":[project.json() for project in self.projects],"Activites":[activity.json() for activity in self.activities]}



    @classmethod
    def find_by_name(cls,name):
       querying= cls.query.filter_by(name=name).all()
       names = [x.json() for x in querying]
       return names

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_country(cls,country_name):
        return cls.query.filter_by(country=country_name).all()

    @classmethod
    def find_by_phone(cls,phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_status(cls,status):
        query=cls.query.filter_by(status=status).all()
        Statuses = [status.json() for status in query]
        return Statuses

    @classmethod
    def find_by_all(cls):
        return cls.query.all()


    @classmethod
    def filter_by_name(cls,name):
            query=cls.query.filter(ClientModel.name.like('%{}%'.format(name))).all()
            names = [x.json() for x in query]
            return names

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
