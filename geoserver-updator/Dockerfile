FROM python:3.9-slim

# Install curl
RUN apt-get update && apt-get install -y curl


RUN apt-get update \
    && apt-get install -y postgresql-client gdal-bin \
    && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY script.py script.py

CMD ["python", "script.py"]