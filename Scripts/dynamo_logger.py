import boto3
from datetime import datetime

# Crear recurso DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pipeline-config')

# Insertar un ítem en la tabla
table.put_item(
    Item={
        'id_pipeline': 'pipeline_001',
        'status': 'Success',
        'timestamp': datetime.utcnow().isoformat()
    }
)