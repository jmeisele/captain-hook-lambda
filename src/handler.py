import json
import logging
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict, context: Dict) -> Dict[str, Any]:
    print(f"Event: {event}:")
    print(f"Context: {context}:")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps("Hello from lambda"),
    }