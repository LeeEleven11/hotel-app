import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"Connected to {self.database} database")
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        """执行SQL查询"""
        try:
            if not self.connect():
                return None

            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)

            if query.lower().startswith("select"):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount

            cursor.close()
            self.disconnect()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            self.disconnect()
            return None

    def get_all_rooms(self):
        """获取所有房间信息"""
        query = "SELECT * FROM rooms"
        return self.execute_query(query)

    def add_room(self, room_id, floor, has_view, occupied, comment):
        """添加房间"""
        query = """
        INSERT INTO rooms (id, floor, hasView, occupied, comment) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (room_id, floor, has_view, occupied, comment)
        return self.execute_query(query, params)

    def update_room(self, room_id, floor, has_view, occupied, comment):
        """更新房间信息"""
        query = """
        UPDATE rooms 
        SET floor = %s, hasView = %s, occupied = %s, comment = %s 
        WHERE id = %s
        """
        params = (floor, has_view, occupied, comment, room_id)
        return self.execute_query(query, params)