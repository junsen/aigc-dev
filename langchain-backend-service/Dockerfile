FROM python:3.11-slim

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5566

CMD ["python", "main.py"]
