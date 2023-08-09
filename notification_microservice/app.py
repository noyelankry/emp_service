from kafka import KafkaConsumer
import signal

TOPIC_NAME = "new-employee"
consumer = None

def consume_notifications():
    global consumer
    consumer = KafkaConsumer(
        "new-employee",
        bootstrap_servers=["kafka1:9092"],
        api_version=(2, 0, 2),
        auto_offset_reset='earliest'
    )

    try:
        for message in consumer:
            print(f"Received message: {message.value.decode('utf-8')}", flush=True)
    except Exception as e:
        print(f"Consumer failed: {e}", flush=True)
    finally:
        consumer.close()
        print("Consumer closed", flush=True)


def handle_interrupt(signum, frame):
    global consumer
    print("Interrupt signal received. Closing consumer...", flush=True)
    if consumer:
        consumer.close()
        print("Consumer closed", flush=True)
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    print("Notification service is running", flush=True)
    consume_notifications()
