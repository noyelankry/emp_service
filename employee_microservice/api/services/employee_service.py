from flask import Flask, request, jsonify
from ..models.employee import Employee, db
import requests
from .kafka_producer import publish_new_employee_msg


class EmployeeService:
    @staticmethod
    def create_employee():
        req = request.get_json()
        name = req.get("name")
        city = req.get("city")
        country = req.get("country")
        salary = req.get("salary")

        # salary should be converted but the API requires payment to access... - uncomment next line when fixed.
        # salary = convert_salary(req.get('salary'))
        # if salary == -1:
        #     return jsonify({"message": f"converter API error"}), 404

        new_employee = Employee(name=name, city=city, country=country, salary=salary)
        db.session.add(new_employee)
        db.session.commit()

        publish_new_employee_msg(new_employee)

        return (
            jsonify({"message": "Employee added successfully", "id": new_employee.id}),
            201,
        )

    @staticmethod
    def get_all_employees():
        employees = Employee.query.all()
        employees_data = [
            {"id": employee.id, "name": employee.name, "salary": employee.salary}
            for employee in employees
        ]
        return jsonify(employees_data)

    @staticmethod
    def convert_salary(salary):
        API_KEY = "hONs2dAEVpe7zk8_6MIXhSJ4JGGHXo4M"
        base_currency = "USD"
        target_currency = "ILS"
        BASE_URL = "https://api.polygon.io/v1/conversion"
        params = {
            "apiKey": API_KEY,
            "amount": salary,
            "from": base_currency,
            "to": target_currency,
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            return data["result"]
        else:
            return -1

    @staticmethod
    def get_employee(employeeID):
        employee_data = Employee.query.get(employeeID)
        return (
            jsonify(
                {
                    "id": employee_data.id,
                    "name": employee_data.name,
                    "salary": employee_data.salary,
                }
            ),
            201,
        )

    @staticmethod
    def remove_employee(employeeID):
        employee_to_delete = Employee.query.get(employeeID)
        db.session.delete(employee_to_delete)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Employee removed successfully",
                    "id": employee_to_delete.id,
                }
            ),
            201,
        )

    @staticmethod
    def update_employee(employeeID):
        employee_to_update = Employee.query.get(employeeID)

        req = request.get_json()
        employee_to_update.name = req.get("name")
        employee_to_update.city = req.get("city")
        employee_to_update.country = req.get("country")
        employee_to_update.salary = req.get("salary")

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Employee data updated successfully",
                    "id": employee_to_update.id,
                }
            ),
            201,
        )
