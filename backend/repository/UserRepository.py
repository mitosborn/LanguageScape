# from model.Table import Table
# import boto3
#
#
# class UserRepository:
#     user_table: Table = None
#
#     def __init__(self, ddb_resource: boto3.resource):
#         self.user_table = Table(table_name='user_table', ddb_resource=ddb_resource)
#
#     def create_user(self):
#         pass
#
#     def update_user(self):
#         pass
