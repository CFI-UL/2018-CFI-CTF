FROM python:3.7

RUN apt-get update -y && apt-get install -y ghc

WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ .

CMD [ "python", "app.py" ]
