from flask import Blueprint, render_template
from database import rds

bp = Blueprint('create', __name__)


@bp.route('/create')
def create():
    pool, rds_url = rds()
    try:
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS hotel;')
        cursor.execute('USE hotel;')
        cursor.execute('CREATE TABLE IF NOT EXISTS rooms(id int NOT NULL, floor int, hasView boolean, occupied boolean, comment varchar(60), PRIMARY KEY(id));')
        connection.commit()
        cursor.close()
        connection.close()
        print("Create table in database if not exists!")
    except Exception as e:
        print(f"Error creating database or table: {e}")

    return render_template('create.html', menuTitle=config['app']['hotel_name'], url=rds_url)