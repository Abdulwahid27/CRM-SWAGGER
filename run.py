from app import app
from flask_migrate import Migrate
from db import db

db.init_app(app)

migrate=Migrate(app,db)