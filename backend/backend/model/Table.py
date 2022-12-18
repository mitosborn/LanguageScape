import boto3


class Table:
    table: boto3.dynamodb.Table = None

    def __init__(self, table_name: str, ddb_resource: boto3.resource):
        self.table = ddb_resource.Table(table_name)

    def put_item(self, item: dict, condition_expression: str = ''):
        self.table.put_item(Item=item, ConditionExpression=condition_expression)

