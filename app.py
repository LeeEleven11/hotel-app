from flask import Flask, render_template, request, jsonify
from config import Config
from aws_utils import AWSUtils
from database import Database

app = Flask(__name__)
app.config.from_object(Config)

aws_utils = AWSUtils(app.config['AWS_REGION'])


@app.route('/')
def index():
    return render_template('index.html', hotel_name=app.config['HOTEL_NAME'])


@app.route('/apprunner')
def apprunner_config():
    service_arn = app.config['APPRUNNER_SERVICE_ARN']
    if not service_arn:
        return render_template('apprunner.html', error="APPRUNNER_SERVICE_ARN environment variable not set")

    config = aws_utils.get_apprunner_service_config(service_arn)
    return render_template('apprunner.html', config=config)


@app.route('/rds')
def rds_list():
    instances = aws_utils.get_rds_instances()
    return render_template('rds_list.html', instances=instances)


@app.route('/database', methods=['GET', 'POST'])
def database():
    if request.method == 'POST':
        action = request.form.get('action')
        db_secret_arn = app.config['DB_SECRET_ARN']

        if not db_secret_arn:
            return jsonify({'error': 'DB_SECRET_ARN environment variable not set'}), 400

        credentials = aws_utils.get_db_credentials(db_secret_arn)
        if not credentials:
            return jsonify({'error': 'Failed to retrieve database credentials'}), 400

        db = Database(
            host=credentials['host'],
            user=credentials['username'],
            password=credentials['password'],
            database='hotel'  # 假设数据库名为hotel
        )

        if action == 'add':
            room_id = request.form.get('room_id')
            floor = request.form.get('floor')
            has_view = request.form.get('has_view') == 'on'
            occupied = request.form.get('occupied') == 'on'
            comment = request.form.get('comment')

            result = db.add_room(room_id, floor, has_view, occupied, comment)
            if result:
                return jsonify({'success': True, 'message': 'Room added successfully'})
            else:
                return jsonify({'success': False, 'message': 'Failed to add room'}), 500

        elif action == 'update':
            room_id = request.form.get('room_id')
            floor = request.form.get('floor')
            has_view = request.form.get('has_view') == 'on'
            occupied = request.form.get('occupied') == 'on'
            comment = request.form.get('comment')

            result = db.update_room(room_id, floor, has_view, occupied, comment)
            if result:
                return jsonify({'success': True, 'message': 'Room updated successfully'})
            else:
                return jsonify({'success': False, 'message': 'Failed to update room'}), 500

    # GET请求，显示数据库页面
    db_secret_arn = app.config['DB_SECRET_ARN']
    if not db_secret_arn:
        return render_template('database.html', error="DB_SECRET_ARN environment variable not set")

    credentials = aws_utils.get_db_credentials(db_secret_arn)
    if not credentials:
        return render_template('database.html', error="Failed to retrieve database credentials")

    db = Database(
        host=credentials['host'],
        user=credentials['username'],
        password=credentials['password'],
        database='hotel'  # 假设数据库名为hotel
    )

    rooms = db.get_all_rooms()
    return render_template('database.html', rooms=rooms)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=8080)