FROM python:3.8.3

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "webapp.py"]
