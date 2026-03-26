import json
from google.cloud import pubsub_v1
PROJECT_ID=os.getenv("GCP_PROJECT_ID")
publisher=pubsub_v1.PublisherClient()
EXTRACTION_TOPIC = f"projects/{PROJECT_ID}/topics/extraction-topic"
RESEARCH_TOPIC = f"projects/{PROJECT_ID}/topics/research-topic"

def publish_message(topic, message: dict):
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic, data)
    return future.result()
