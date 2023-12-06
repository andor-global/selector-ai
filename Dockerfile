FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y gcc

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./api .
COPY ./chat .
COPY ./psychotype .
COPY ./machine_learning .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
