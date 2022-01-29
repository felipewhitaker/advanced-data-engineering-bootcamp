from os import environ
import os
import json
import boto3
from fake_web_events import Simulation

client = boto3.client("firehose")
deploy_env = os.environ.get("ENVIRONMENT", "local")

def put_record(event: list):
    global client, deploy_env
    data = json.dumps(event) + "\n"
    response = client.put_record(
        DeliveryStreamName=f"firehose-{deploy_env}-raw-delivery-stream", # from kinesis/stack.py
        record = {"Data": data}
    )
    print(event, end = "\r")
    return response

simulation = Simulation(user_pool_size = 100, sessions_per_day = 1_000)
events = simulation.run(duration_seconds = 3 * 60)

for event in events:
    put_record(event)