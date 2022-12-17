import json

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('translations')
tables = list(dynamodb.tables.all())
print(tables)

# Read the JSON file
with open('groupedByTranslations.json') as json_data:
    items = json.load(json_data)

    with table.batch_writer() as batch:
        # Loop through the JSON objects
        for item in items:
            batch.put_item(Item=item)
