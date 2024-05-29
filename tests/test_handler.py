import json

from src.handler import lambda_handler


def test_lambda_handler() -> None:
    event = {}
    context = {}
    result = lambda_handler(event, context)
    expected = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps("Hello from lambda"),
    }
    assert result == expected
