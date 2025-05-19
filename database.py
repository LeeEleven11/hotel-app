# # database.py
# import pymysql
# import logging
#
#
# class Database:
#     def __init__(self, host, user, password, database):
#         self.host = host
#         self.user = user
#         self.password = password
#         self.database = database
#         self.connection = None
#         # 只有在指定数据库时才立即连接
#         if database:
#             self._connect()
#
#     def _connect(self):
#         """建立数据库连接"""
#         try:
#             # 如果没有指定数据库，连接时不包含 database 参数
#             connect_params = {
#                 'host': self.host,
#                 'user': self.user,
#                 'password': self.password,
#                 'cursorclass': pymysql.cursors.DictCursor,
#                 'connect_timeout': 10
#             }
#
#             if self.database:
#                 connect_params['database'] = self.database
#
#             self.connection = pymysql.connect(**connect_params)
#             logging.info(f"成功连接到数据库: {self.host}/{self.database or 'default'}")
#         except Exception as e:
#             logging.error(f"数据库连接失败: {str(e)}")
#             raise
#
#     def ensure_database_exists(self, db_name):
#         """创建数据库"""
#         if not self.connection:
#             self._connect()
#
#         try:
#             with self.connection.cursor() as cursor:
#                 cursor.execute(
#                     f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
#                 logging.info(f"成功创建数据库: {db_name}")
#
#         except Exception as e:
#             logging.error(f"创建数据库失败: {str(e)}")
#             raise
#
#     def ensure_table_exists(self):
#         """检查并创建rooms表"""
#         if not self.connection or self.connection.open is False:
#             self._connect()
#
#         try:
#             with self.connection.cursor() as cursor:
#                 # 检查表是否存在
#                 cursor.execute("SHOW TABLES LIKE 'rooms'")
#                 result = cursor.fetchone()
#
#                 if not result:
#                     # 创建rooms表
#                     sql = """
#                     CREATE TABLE IF NOT EXISTS rooms (
#                         id INT PRIMARY KEY AUTO_INCREMENT,
#                         room_id VARCHAR(50) NOT NULL UNIQUE,
#                         floor INT NOT NULL,
#                         has_view BOOLEAN NOT NULL DEFAULT 0,
#                         occupied BOOLEAN NOT NULL DEFAULT 0,
#                         comment TEXT,
#                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#                     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
#                     """
#                     cursor.execute(sql)
#                     logging.info("成功创建rooms表")
#                 else:
#                     logging.info("rooms表已存在")
#         except Exception as e:
#             logging.error(f"创建表失败: {str(e)}")
#             raise
#
#
#     def get_all_rooms(self):
#         """获取所有房间"""
#         if not self.connection or self.connection.open is False:
#             self._connect()
#
#         with self.connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM rooms")
#             return cursor.fetchall()
#
#     def add_room(self, room_id, floor, has_view, occupied, comment):
#         """添加房间"""
#         if not self.connection or self.connection.open is False:
#             self._connect()
#
#         try:
#             with self.connection.cursor() as cursor:
#                 sql = """
#                 INSERT INTO rooms (room_id, floor, has_view, occupied, comment)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(sql, (room_id, floor, has_view, occupied, comment))
#             self.connection.commit()
#             return True
#         except Exception as e:
#             logging.error(f"添加房间失败: {str(e)}")
#             self.connection.rollback()
#             return False
#
#     def update_room(self, room_id, floor, has_view, occupied, comment):
#         """更新房间信息"""
#         if not self.connection or self.connection.open is False:
#             self._connect()
#
#         try:
#             with self.connection.cursor() as cursor:
#                 sql = """
#                 UPDATE rooms
#                 SET floor=%s, has_view=%s, occupied=%s, comment=%s
#                 WHERE room_id=%s
#                 """
#                 cursor.execute(sql, (floor, has_view, occupied, comment, room_id))
#             self.connection.commit()
#             return cursor.rowcount > 0
#         except Exception as e:
#             logging.error(f"更新房间失败: {str(e)}")
#             self.connection.rollback()
#             return False