from flask import render_template, url_for, request

from app_creator import app # Создает приложение и БД
from answener import kind_of_request # Классификатор запросов



menu = [{"name": "Начать работу", "url": "/"},
        {"name": "База данных", "url": "none"}]



@app.route("/")
def main_page():
    return render_template('index.html', temp="Начать работу", menu=menu)



@app.route("/download/<key>", methods = ['GET'])
@app.route("/download/refresh=<refresh>", methods = ['GET'])
@app.route("/download", methods = ['POST', 'GET'])
def download(key=None, refresh=None):

    req = kind_of_request(request, key, refresh) # Присвоение req класса запроса (answener.py)
    return req.make_answer() # Вызов метода этого класса, который формирует ответ
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 
