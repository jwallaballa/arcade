FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=src.app

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

