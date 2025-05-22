import os
import logging

logging.basicConfig(level=logging.DEBUG)

# 配置信息
class Config:
    DEBUG = True
    HOTEL_DB_HOST = os.environ.get('HOTEL_DB_HOST')
    APPRUNNER_SERVICE_ARN = os.environ.get('APPRUNNER_SERVICE_ARN')
    DB_SECRET_ARN = os.environ.get('DB_SECRET_ARN')
    HOTEL_NAME = os.environ.get('HOTEL_NAME', 'Cloud Raiser Hotel')

    logging.debug(f"APPRUNNER_SERVICE_ARN: {APPRUNNER_SERVICE_ARN}")
