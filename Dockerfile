FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api
COPY ./chat /code/chat
COPY ./psychotype /code/psychotype
COPY ./machine_learning /code/machine_learning
COPY ./static /code/static

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
