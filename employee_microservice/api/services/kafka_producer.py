from kafka import KafkaProducer
import json

TOPIC_NAME = "new-employee"


def publish_new_employee_msg(employee_data):
    producer = KafkaProducer(
        bootstrap_servers=["kafka1:9092"],
        api_version=(2, 0, 2),
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

    try:
        future = producer.send(TOPIC_NAME, value=data_json.encode("utf-8"))
        record_data = future.get(timeout=60)
        print(f"Message sent to topic {record_data.topic}  at partition {record_data.partition} offset {record_data.offset}")
    except Exception as e:
        print(f"failed to send a message: {e}", flush=True)
    finally:
        producer.close()
        print("Producer closed", flush=True)