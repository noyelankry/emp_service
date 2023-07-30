from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'random string'

db = SQLAlchemy(app)

class employee(db.Model):
   id = db.Column('employeeID', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   country = db.Column(db.String(50))  
   salary = db.Column(db.Integer, default = 0)

@app.route("/")
def home():
    return "Employee microservice!"

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = employee.query.all()
    employees_data = [{"id": employee.id, 
                       "name": employee.name, 
                       "salary": employee.salary} for employee in employees]
    return jsonify(employees_data)

@app.route('/employees/<int:employeeID>', methods=['GET'])
def get_employee(employeeID):
    employee_data = employee.query.get(employeeID)
    return jsonify({"id": employee_data.id, "name": employee_data.name, "salary": employee_data.salary}), 201

@app.route('/employees', methods=['POST'])
def add_new_employee():
    req = request.get_json()
    name = req.get('name')
    city = req.get('city')
    country = req.get('country')
    salary = req.get('salary') 
    
    # salary should be converted but the API requires payment to access... - uncomment next line when fixed.
    # salary = convert_salary(req.get('salary'))
    # if salary == -1:
    #     return jsonify({"message": f"converter API error"}), 404

    new_employee = employee(name = name, city = city, country = country, salary = salary)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully", "id": new_employee.id}), 201

def convert_salary(salary):
    API_KEY = 'hONs2dAEVpe7zk8_6MIXhSJ4JGGHXo4M'
    base_currency = 'USD'
    target_currency = 'ILS'
    BASE_URL = 'https://api.polygon.io/v1/conversion'
    params = {
            'apiKey': API_KEY,
            'amount': salary,
            'from': base_currency,
            'to': target_currency }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['result']
    else:
        return -1

@app.route('/employees/<int:employeeID>', methods = ['DELETE'])
def remove_employee(employeeID):
    employee_to_delete = employee.query.get(employeeID)
    db.session.delete(employee_to_delete)
    db.session.commit()

    return jsonify({"message": "Employee removed successfully", "id": employee_to_delete.id}), 201

@app.route('/employees/<int:employeeID>', methods=["PUT"])
def update_employee(employeeID):

    employee_to_update = employee.query.get(employeeID)

    req = request.get_json()
    employee_to_update.name = req.get('name')
    employee_to_update.city = req.get('city')
    employee_to_update.country = req.get('country')
    employee_to_update.salary = req.get('salary')
    
    db.session.commit()
    return jsonify({"message": "Employee data updated successfully", "id": employee_to_update.id}), 201

with app.app_context():
    db.create_all()
