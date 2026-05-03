import boto3
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_table():
    table = dynamodb.create_table(
        TableName='guardrails-audit-log',
        KeySchema=[
            {'AttributeName': 'request_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'request_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print(f"Table created: {table.table_name}")
    return table

def log_request(message: str, layer1_result: str, layer2_result: dict, final_decision: str):
    table = dynamodb.Table('guardrails-audit-log')
    table.put_item(Item={
        'request_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'message': message[:500],
        'layer1_result': layer1_result,
        'layer2_risk_level': layer2_result.get('risk_level'),
        'layer2_attack_type': layer2_result.get('attack_type'),
        'layer2_confidence': str(layer2_result.get('confidence')),
        'layer2_latency_ms': str(layer2_result.get('latency_ms')),
        'final_decision': final_decision
    })

if __name__ == '__main__':
    create_table()
