FROM python:3.8.3

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "webapp.py"]
