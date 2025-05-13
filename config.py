import os

# 配置信息
class Config:
    DEBUG = True
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    APPRUNNER_SERVICE_ARN = os.environ.get('APPRUNNER_SERVICE_ARN')
    DB_SECRET_ARN = os.environ.get('DB_SECRET_ARN')
    HOTEL_NAME = os.environ.get('HOTEL_NAME', 'My Hotel')