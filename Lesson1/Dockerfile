# Dockerfile - this is a comment. Delete me if you want.

FROM python:3.7


WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN mkdir -p /app/static

ENTRYPOINT ["python"]

CMD ["app.py"]

