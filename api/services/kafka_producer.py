from kafka import KafkaProducer
from json import dumps
import json

TOPIC_NAME = "new-employee"


def publish_new_employee_msg(employee_data):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        api_version=(7, 3, 2),
    )
    message = {
        "content": "new employee added",
        "employee data": {
            "id": employee_data.id,
            "name": employee_data.name,
            "city": employee_data.city,
            "country": employee_data.country,
            "salary": employee_data.salary,
        },
    }

    data_json = json.dumps(message)
    producer.send(TOPIC_NAME, value=data_json.encode("utf-8"))
    producer.close()
