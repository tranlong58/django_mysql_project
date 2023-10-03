FROM python:3

# RUN apt-get update && apt-get install -y rsync

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

# EXPOSE 8000

# CMD ["python","manage.py","runserver","0.0.0.0:8000"]
