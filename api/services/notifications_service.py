from kafka import KafkaConsumer

TOPIC_NAME = "new-employee"


def consume_notifications():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=["localhost:9092"],
        api_version=(7, 3, 2),
    )

    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")


if __name__ == "__main__":
    consume_notifications()
