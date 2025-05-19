# from flask import Flask, render_template, request, jsonify
# from config import Config
# from aws_utils import AWSUtils
# from database import Database
# import logging
# import json
#
# logging.basicConfig(level=logging.DEBUG)
#
# app = Flask(__name__)
# app.config.from_object(Config)
#
# aws_utils = AWSUtils(app.config['AWS_REGION'])
#
#
# def get_database_instance():
#
#
#     # host = '127.0.0.1'
#     # username = 'root'
#     # password = 'Bing246411!'
#     try:
#         db_secret_str = app.config['DB_SECRET_ARN']
#         if not db_secret_str:
#             return None, "DB_SECRET_ARN environment variable not set"
#         logging.info(f"get_database_instance db_secret_str:{db_secret_str}")
#         # 解析 JSON 字符串为 Python 字典
#         credentials = json.loads(db_secret_str)
#         logging.info(f"成功解析数据库凭证: {credentials}")
#
#         # 确保 JSON 中包含必要的连接信息
#         host = credentials['host']
#         username = credentials['username']
#         password = credentials['password']
#
#
#         # 1. 先连接到默认数据库 (通常是mysql)
#         default_db = Database(
#             host=host,
#             user=username,
#             password=password,
#             # database='mysql'  # 连接到默认数据库进行检查
#             database=None  # 连接到默认数据库进行检查
#         )
#
#         # 2. 检查并创建hotel数据库
#         default_db.ensure_database_exists('hotel')
#
#         # 创建数据库实例
#         db = Database(
#             host=host,
#             user=username,
#             password=password,
#             database='hotel'
#         )
#
#         # 4. 检查并创建rooms表
#         db.ensure_table_exists()
#
#         # 测试查询，验证连接是否成功
#         rooms = db.get_all_rooms()
#
#         if rooms is None:
#             return None, "Failed to retrieve data from database. Check credentials and connectivity."
#
#         return db, None
#
#     except json.JSONDecodeError as e:
#         return None, f"Failed to parse database credentials: {str(e)}"
#     except KeyError as e:
#         return None, f"Missing key in database credentials: {e}"
#     except Exception as e:
#         # 捕获其他可能的异常
#         logging.exception("Database connection error")
#         return None, f"Database connection error: {str(e)}"
#
#
# @app.route('/')
# def index():
#     return render_template('index.html', hotel_name=app.config['HOTEL_NAME'])
#
#
# @app.route('/apprunner')
# def apprunner_config():
#     service_arn = app.config['APPRUNNER_SERVICE_ARN']
#     if not service_arn:
#         return render_template('apprunner.html', error="APPRUNNER_SERVICE_ARN environment variable not set")
#
#     config = aws_utils.get_apprunner_service_config(service_arn)
#     return render_template('apprunner.html', config=config)
#
#
# @app.route('/rds')
# def rds_list():
#     instances = aws_utils.get_rds_instances()
#     return render_template('rds_list.html', instances=instances)
#
#
# @app.route('/database', methods=['GET', 'POST'])
# def database():
#     if request.method == 'POST':
#         action = request.form.get('action')
#         db, error = get_database_instance()
#         if error:
#             return jsonify({'error': error}), 400
#
#         if action == 'add':
#             room_id = request.form.get('room_id')
#             floor = request.form.get('floor')
#             has_view = request.form.get('has_view') == 'on'
#             occupied = request.form.get('occupied') == 'on'
#             comment = request.form.get('comment')
#             if not room_id or not floor:
#                 return jsonify({'error': 'Room ID and floor are required'}), 400
#
#             result = db.add_room(room_id, floor, has_view, occupied, comment)
#             if result:
#                 return jsonify({'success': True, 'message': 'Room added successfully'})
#             else:
#                 return jsonify({'success': False, 'message': 'Failed to add room'}), 500
#
#         elif action == 'update':
#             room_id = request.form.get('room_id')
#             floor = request.form.get('floor')
#             has_view = request.form.get('has_view') == 'on'
#             occupied = request.form.get('occupied') == 'on'
#             comment = request.form.get('comment')
#
#             result = db.update_room(room_id, floor, has_view, occupied, comment)
#             if result:
#                 return jsonify({'success': True, 'message': 'Room updated successfully'})
#             else:
#                 return jsonify({'success': False, 'message': 'Failed to update room'}), 500
#
#     # GET请求，显示数据库页面
#     db, error = get_database_instance()
#     if error:
#         return render_template('database.html', error=error)
#
#     # 关键修改：检查数据库查询结果
#     rooms = db.get_all_rooms()
#     if rooms is None:
#         return render_template('database.html', error="Failed to retrieve rooms from database")
#
#     return render_template('database.html', rooms=rooms)
#
#
# if __name__ == '__main__':
#     app.run(debug=app.config['DEBUG'], port=8080)



import os
import hashlib
from flask import Flask, jsonify, request

app = Flask(__name__)

# home page
@app.route('/')
def home():
    res = '''
        <pre>
        ___ _       _______    ____        _ __    __         
       /   | |     / / ___/   / __ )__  __(_) /___/ /__  _____
      / /| | | /| / /\__ \   / __  / / / / / / __  / _ \/ ___/
     / ___ | |/ |/ /___/ /  / /_/ / /_/ / / / /_/ /  __/ /    
    /_/  |_|__/|__//____/  /_____/\__,_/_/_/\__,_/\___/_/     Cloud Raiser 101
        </pre>
    '''
    return res

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 80
    app.run(host=host, port=port)