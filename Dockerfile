# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers nano bash
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
COPY . /data
CMD ["python", "/data/main.py"]
