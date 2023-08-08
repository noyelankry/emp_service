from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
   id = db.Column('employeeID', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   country = db.Column(db.String(50))  
   salary = db.Column(db.Integer, default = 0)
   