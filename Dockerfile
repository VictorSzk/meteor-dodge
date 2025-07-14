FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

# Install your dependencies here, for example:
# RUN pip install -requirements.txt



CMD ["python"]