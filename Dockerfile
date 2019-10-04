FROM python:3.7
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./app app
WORKDIR /app

