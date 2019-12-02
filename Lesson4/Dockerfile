# Dockerfile - this is a comment. Delete me if you want.

FROM python:3.7


WORKDIR /app

COPY . /app

RUN pip3.7 install -r requirements.txt

RUN apt-get update && apt-get install -y \
    jq

ENTRYPOINT ["python"]

CMD ["app.py"]

