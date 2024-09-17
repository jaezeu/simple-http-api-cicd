import json
import os
import pytest
from unittest.mock import patch
from src.app import lambda_handler

@pytest.fixture
def setup_environment():
    os.environ['DDB_TABLE'] = 'test-table'
    yield
    del os.environ['DDB_TABLE']

@patch('boto3.client')
def test_lambda_handler_with_payload(mock_boto_client, setup_environment):
    mock_dynamodb = mock_boto_client.return_value
    event = {
        "body": json.dumps({"year": 2024, "title": "The New Era"})
    }
    context = {}

    response = lambda_function.lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert json.loads(response['body'])['message'] == "Successfully inserted data!"
    mock_dynamodb.put_item.assert_called_once_with(
        TableName='test-table',
        Item={"year": {'N': '2024'}, "title": {'S': 'The New Era'}}
    )

@patch('boto3.client')
def test_lambda_handler_without_payload(mock_boto_client, setup_environment):
    mock_dynamodb = mock_boto_client.return_value
    event = {
        "body": None
    }
    context = {}

    response = lambda_function.lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert json.loads(response['body'])['message'] == "Successfully inserted data!"
    mock_dynamodb.put_item.assert_called_once_with(
        TableName='test-table',
        Item={"year": {'N': '2012'}, "title": {'S': 'The Amazing Spider-Man 2'}}
    )
