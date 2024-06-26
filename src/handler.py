import json
import logging
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel, ValidationError, computed_field, validator


class GitHubEvent(BaseModel):
    action: str
    repository: dict
    organization: dict
    sender: dict


class AWSEvent(BaseModel):
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    headers: dict
    requestContext: dict
    body: GitHubEvent
    isBase64Encoded: bool

    @validator("body", pre=True)
    def parse_body(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value


logger = logging.getLogger()
logger.setLevel(logging.INFO)

eventbridge_client = boto3.client("events")


def lambda_handler(event: Dict, context: Dict) -> Dict[str, Any]:
    print(f"Event: {event}:")
    print(f"Context: {context}:")

    # Input validation via pydantic model
    try:
        event_data = AWSEvent.model_validate(event)
    except ValidationError as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": e.errors()}),
        }

    # If repo created event proceed, otherwise skip
    if json.loads(event["body"])["action"] != "created":
        print("repo not created skipping")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps("repo not created skipping"),
        }

    headers = event.get("headers")
    detail_type = headers.get("x-github-event", "github-webhook-lambda")

    # Put data into event bus
    try:
        event_bridge_response = eventbridge_client.put_events(
            Entries=[
                {
                    "Source": "github.com",
                    "DetailType": detail_type,
                    "Detail": json.dumps(event),
                    "EventBusName": "default",
                }
            ],
        )
        print(f"Eventbridge Response: {event_bridge_response}")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps("Event published in default event bus"),
        }
    except ClientError as e:
        print(f"{e}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(f"Client Error: {e}"),
        }
