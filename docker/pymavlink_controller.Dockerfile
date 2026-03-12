FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pymavlink \
    numpy

WORKDIR /app

CMD ["python3", "controller.py"]
