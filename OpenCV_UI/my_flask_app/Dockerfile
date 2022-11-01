FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

CMD ["python3", "main_file.py"]