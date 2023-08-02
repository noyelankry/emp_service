from flask import Flask
from api.models.employee import db
from api.routes.employee_routes import employee_bp
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SECRET_KEY'] = config('SECRET_KEY')

db.init_app(app)

app.register_blueprint(employee_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run()