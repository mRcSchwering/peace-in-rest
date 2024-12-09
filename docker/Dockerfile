FROM python:3.11

LABEL purpose="REST API app"
LABEL maintainer="schweringmarc01@gmail.com"

# requirements layer
COPY app/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# app layer
COPY ./app /app

EXPOSE 80

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
