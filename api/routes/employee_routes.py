from flask import Blueprint
from ..services.employee_service import EmployeeService
from ..schemas.employee_schema import EmployeeSchema

employee_bp = Blueprint('employee', __name__)
employee_schema = EmployeeSchema()

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    return EmployeeService.get_all_employees()

@employee_bp.route('/employees/<int:employeeID>', methods=['GET'])
def get_employee(employeeID):
    return EmployeeService.get_employee(employeeID)

@employee_bp.route('/employees', methods=['POST'])
def create_new_employee():
    return EmployeeService.create_employee()

@employee_bp.route('/employees/<int:employeeID>', methods=["PUT"])
def update_employee(employeeID):
    return EmployeeService.update_employee(employeeID)

@employee_bp.route('/employees/<int:employeeID>', methods = ['DELETE'])
def remove_employee(employeeID):
    return EmployeeService.remove_employee(employeeID)