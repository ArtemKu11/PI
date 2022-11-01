import os
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def neuron(img0, model): # Распознавание изображения глаз нейросетью

    img0 = img0 / 255


    img0 = np.expand_dims(img0, axis=0)
    img0 = np.expand_dims(img0, axis=3)


    prediction = model.predict(img0, verbose = 0)
    

    # first_digit = prediction[0, 0]
    second_digit = prediction[0, 1]
    # print(first_digit, second_digit)
    if second_digit > 0.98: 
        return 'to_cam'
    else:
        return 'to_screen'


def damper(text, to_screen_counter, to_cam_counter): # Дэмпфер в 2 кадра для переключения направления взгляда
    if text == 'to_screen':
        to_screen_counter += 1
        if to_screen_counter > 2:
            to_cam_counter = 0
            color = (0, 0, 255)
            text = 'to_screen'
            return (text, color, to_screen_counter, to_cam_counter)
        else:
            color = (0, 255, 0)
            text = 'to_cam'
            return (text, color, to_screen_counter, to_cam_counter)
    else:
        to_cam_counter += 1
        if to_cam_counter > 1:
            to_screen_counter = 0
            color = (0, 255, 0)
            text = 'to_cam'
            return (text, color, to_screen_counter, to_cam_counter)
        else:
            color = (0, 0, 255)
            text = 'to_screen'
            return (text, color, to_screen_counter, to_cam_counter)


def for_flask(img, eyeCascade, model, json_dict): # Подготовка изображения для НС и последующая обработка по рез. распознавания

    to_screen_counter = json_dict['to_screen_counter'] 
    to_cam_counter = json_dict['to_cam_counter']
    coord_x = json_dict['coord_x']
    coord_y = json_dict['coord_y']
    coord_w = json_dict['coord_w']
    coord_h = json_dict['coord_h']
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    eyes = eyeCascade.detectMultiScale( # Поиск глаз
        img_gray,              
        scaleFactor=1.2,       
        minNeighbors=10,
        # minSize=(5, 5),
    )
    
    if (len(eyes) == 2) and abs(eyes[0][1] - eyes[1][1]) < 10: # Если глаза два и расстояние по y < 10px

        min_y = min(eyes[0][1], eyes[1][1])
        max_h = max(eyes[0][3], eyes[1][3])
        min_x = min(eyes[0][0], eyes[1][0])
        max_x = max(eyes[0][0], eyes[1][0])
        max_w = max(eyes[0][2], eyes[1][2])

        coord_x = min_x
        coord_y = min_y
        coord_w = max_x + max_w
        coord_h = min_y + max_h

        img2 = img_gray[min_y:min_y + max_h, min_x:max_x + max_w] # Подготовка изображения для нейросети
        img2 = cv2.resize(img2, (145, 60))
        
        text = neuron(img2, model) # Нейросеть
        text, color, to_screen_counter, to_cam_counter = damper(text, to_screen_counter, to_cam_counter) # Демпфер в 1-2 кадра


    else: # Если глаза не распознались, то принимается прежний результат распознавания
        if max(to_screen_counter, to_cam_counter) == to_screen_counter: 
            text = 'to_screen'
            color = (0, 0, 255)
        else:
            text = 'to_cam'
            color = (0, 255, 0)
        

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # Отрисовка квадратика и текста
    cv2.putText(img, text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA, False)
    cv2.rectangle(img, (coord_x, coord_y), (coord_w, coord_h), color, 1)

    json_dict['to_screen_counter'] = str(to_screen_counter)
    json_dict['to_cam_counter'] = str(to_cam_counter)
    json_dict['coord_x'] = str(coord_x)
    json_dict['coord_y'] = str(coord_y)
    json_dict['coord_w'] = str(coord_w)
    json_dict['coord_h'] = str(coord_h)
    json_dict['result'] = text

    
    return img, json_dict