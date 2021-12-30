from db import db

class SalesModel(db.Model):

    __tablename__='Sales'

    id=db.Column(db.Integer,primary_key=True)
    proposed_amount=db.Column(db.Integer,nullable=False)
    finalized_amount=db.Column(db.Integer,nullable=True)
    status=db.Column(db.String)
    description=db.Column(db.Text)
    date=db.Column(db.Date)
    percentage_profit=db.Column(db.Integer)

    project_id=db.Column(db.Integer,db.ForeignKey('Projects.id'),unique=True)
    projects=db.relationship('ProjectModel')


    def __init__(self,proposed_amount,finalized_amount,status,description,date,percentage_profit,project_id):
        self.proposed_amount=proposed_amount
        self.finalized_amount=finalized_amount
        self.status=status
        self.description=description
        self.date=date
        self.percentage_profit=percentage_profit
        self.project_id=project_id


    def json(self):
        return {"id":self.id,"proposed_amount":self.proposed_amount,"finalized_amount":self.finalized_amount,"status":self.status,
                "description":self.description,"date":str(self.date),"percentage_profit":self.percentage_profit,"project_id":self.project_id}



    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_date(cls, date):
        query = cls.query.filter_by(date=date).all()
        sales = [sales.json() for sales in query]
        return sales

    @classmethod
    def find_by_finalized_amount(cls, amount):
        query = cls.query.filter(SalesModel.finalized_amount.like('%{}%'.format(amount))).all()
        names = [x.json() for x in query]
        return names


    @classmethod
    def find_by_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()