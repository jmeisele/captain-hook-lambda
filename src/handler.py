import json
import logging
from typing import Any, Dict

import boto3
from pydantic import BaseModel, ValidationError, computed_field


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
            "body": json.dumps({"error": e}),
        }

    # If repo created event proceed, otherwise skip
    # Enrich event data?

    # Put enriched data into event bus
    # event_bridge_response = eventbridge_client.put_events(
    #     Entries=[
    #         {
    #             "Source": "github.com",
    #             "Resources": [""],
    #             "DetailType": event["detail-type"],
    #             "Detail": json.dumps(event),
    #             "EventBusName": "default",
    #         }
    #     ],
    # )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps("Hello from lambda"),
    }
