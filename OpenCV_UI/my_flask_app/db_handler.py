import io
import base64
import random
from datetime import datetime

from app_creator import db, app


class Table(db.Model):  # Таблица БД
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(50))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    result = db.Column(db.String(50))
    file = db.Column(db.LargeBinary)
    key = db.Column(db.String(32))


with app.app_context():
    db.create_all()


def save_to_db(image, result, counter):  # Сохранение картинки в БД

    key = random.getrandbits(128)
    key = "%032x" % key

    date_var = datetime.now()
    year = date_var.year
    month = date_var.month
    day = date_var.day

    image_name = f'{str(year)}_{str(month)}_{str(day)}_image_{counter}'

    current_date = f'{str(day)}.{str(month)}.{str(year)}'
    current_time = str(date_var.time())[:str(date_var.time()).find('.')]

    if result == 'to_cam':
        result = 'Камера'
    elif result == 'to_screen':
        result = 'Экран'
    try:
        t = Table(image_name=image_name, date=current_date, time=current_time, result=result, file=image, key=key)
        db.session.add(t)
        db.session.commit()
        db_success = 'true'
    except:
        db.session.rollback()
        # db_success = 'false'
    db_success = 'true'

    return db_success


def get_file(key):  # Возврат io.Bytes-файла по ключу
    file_temp = Table.query.filter(Table.key == key).all()
    file = file_temp[0].file
    file = base64.b64encode(file)
    file = str(file)[2:-1]
    file = io.BytesIO(base64.decodebytes(bytes(file, "utf-8")))
    return (file, file_temp[0].image_name)


def clean_db():  # Очистка БД
    db.session.query(Table).delete(synchronize_session="fetch")
    db.session.commit()


def get_some_strings(db_counter):  # Подгрузка строк из БД
    db_count = db.session.query(Table.id).count()
    viborka = Table.query.filter(Table.id <= db_count - db_counter).order_by(Table.id.desc()).limit(10).all()
    db.session.commit()
    return (viborka, db_count)
