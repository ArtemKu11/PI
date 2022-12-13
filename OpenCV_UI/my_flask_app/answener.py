import base64
import cv2
import numpy as np
from flask import send_file, render_template
from tensorflow.keras.models import load_model

from db_handler import get_some_strings, save_to_db, clean_db, get_file
from magic import for_flask

model = load_model('neuroset_full.h5')  # Нейросеть для определения направления взгляда
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')  # Штука для определения глаз


def kind_of_request(request, key, refresh):  # Классификатор запросов
    if request.method == 'POST':
        return Answer_A(request)  # Основной запрос
    if request.method == 'GET':
        if refresh == 'true':
            return Answer_B()  # Очистить БД
        if key != None:
            return Answer_C(key)  # Скачать файл
        else:
            return Answer_D(request)  # Подгрузить ДБ


class Answer_A():  # Основной запрос на обработку изображения с возможностью сохранения его в БД

    def __init__(self, req):
        self.json_dict = {}
        self.json_dict['to_screen_counter'] = int(req.form.get('to_screen_counter'))
        self.json_dict['to_cam_counter'] = int(req.form.get('to_cam_counter'))
        self.json_dict['coord_x'] = int(req.form.get('coord_x'))
        self.json_dict['coord_y'] = int(req.form.get('coord_y'))
        self.json_dict['coord_w'] = int(req.form.get('coord_w'))
        self.json_dict['coord_h'] = int(req.form.get('coord_h'))
        self.json_dict['save_to_db'] = req.form.get('save_to_db')
        self.json_dict['save_counter'] = req.form.get('save_counter')

        self.imgg = req.form.get('image')
        self.shapka = self.imgg[:22]
        self.imgg = self.imgg[22:]

    def make_answer(self):
        image = base64.b64decode(self.imgg)
        xz_chto = np.fromstring(image, np.uint8)
        xz_chto = cv2.imdecode(xz_chto, cv2.IMREAD_UNCHANGED)

        xz_chto, self.json_dict = for_flask(xz_chto, eyeCascade, model, self.json_dict)

        if self.json_dict['save_to_db'] == 'true':
            self.json_dict['db_success'] = save_to_db(image, self.json_dict['result'], self.json_dict['save_counter'])
        else:
            self.json_dict['db_success'] = 'false'

        retval, buffer = cv2.imencode('.png', xz_chto)
        img_str = base64.b64encode(buffer)

        return {"text": self.shapka + str(img_str)[2:-1],
                "text2": "Загружено успешно",
                'to_screen_counter': self.json_dict['to_screen_counter'],
                'to_cam_counter': self.json_dict['to_cam_counter'],
                'coord_x': self.json_dict['coord_x'],
                'coord_y': self.json_dict['coord_y'],
                'coord_h': self.json_dict['coord_h'],
                'coord_w': self.json_dict['coord_w'],
                'result': self.json_dict['result'],
                'db_success': self.json_dict['db_success'],
                "type": "success"}

    def __repr__(self):
        return f"request for image detection with save_to_db flag = {self.json_dict['save_to_db']}"


class Answer_B():  # Запрос на очистку базы данных

    def make_answer(self):
        clean_db()
        return {"text": "Успешно"}

    def __repr__(self):
        return f"request to clean database"


class Answer_C():  # Запрос на ссылку для скачивания

    def __init__(self, key):
        self.key = key

    def __repr__(self):
        return f"request to download link, key = {self.key}"

    def make_answer(self):
        file = get_file(self.key)
        return send_file(file[0], download_name=file[1], mimetype='image/png', as_attachment=True)


class Answer_D():  # Подгрузить 10 позиций ДБ

    def __init__(self, req):
        self.db_counter = int(req.args['db_counter'])

    def __repr__(self):
        return f"request to get some database positions, db_counter = {self.db_counter}"

    def make_answer(self):
        viborka, db_count = get_some_strings(self.db_counter)
        if len(viborka) > 0:
            first_in_table = viborka[0].id
        else:
            first_in_table = 'none'
        return {'text': render_template('db_page.html', db_count=db_count - self.db_counter, viborka=viborka),
                'total': db_count,
                'first_in_table': first_in_table}
