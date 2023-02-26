FROM python:3.8.5-slim

RUN mkdir -p /app/src
WORKDIR /app/src

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src /app/src
RUN chmod 755 /app/src/*py

CMD ["python", "app.py"]