# import boto3
# from botocore.exceptions import ClientError
# import json
#
#
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
#
# class AWSUtils:
#     def __init__(self, region_name):
#         self.region_name = region_name
#         self.apprunner_client = boto3.client('apprunner', region_name=region_name)
#         self.rds_client = boto3.client('rds', region_name=region_name)
#         self.secrets_manager = boto3.client('secretsmanager', region_name=region_name)
#
#     def get_apprunner_service_config(self, service_arn):
#         """获取AppRunner服务配置信息"""
#         try:
#             response = self.apprunner_client.describe_service(ServiceArn=service_arn)
#             service = response['Service']
#
#             # 获取环境变量
#             env_vars = {}
#             for env_config in service.get('Configuration', {}).get('EnvironmentVariables', []):
#                 env_vars[env_config['Name']] = env_config['Value']
#
#             return {
#                 'service_name': service['ServiceName'],
#                 'status': service['Status'],
#                 'create_time': str(service['CreatedAt']),
#                 'environment_variables': env_vars
#             }
#         except ClientError as e:
#             logging.debug(f"Error getting AppRunner service config: {e}")
#             return None
#
#     def get_rds_instances(self):
#         """获取RDS实例列表"""
#         try:
#             response = self.rds_client.describe_db_instances()
#             instances = []
#             for instance in response['DBInstances']:
#                 instances.append({
#                     'db_instance_identifier': instance['DBInstanceIdentifier'],
#                     'engine': instance['Engine'],
#                     'engine_version': instance['EngineVersion'],
#                     'db_instance_status': instance['DBInstanceStatus'],
#                     'endpoint': instance.get('Endpoint', {}).get('Address', 'N/A'),
#                     'port': instance.get('Endpoint', {}).get('Port', 'N/A')
#                 })
#             return instances
#         except ClientError as e:
#             logging.debug(f"Error getting RDS instances: {e}")
#             return []
#
#     def get_db_credentials(self, secret_arn):
#         """获取数据库凭证"""
#         try:
#             response = self.secrets_manager.get_secret_value(SecretId=secret_arn)
#             secret = json.loads(response['SecretString'])
#             return secret
#         except ClientError as e:
#             logging.debug(f"Error getting DB credentials: {e}")
#             return None