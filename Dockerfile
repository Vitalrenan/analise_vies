FROM python:3.7-slim

COPY ./requirements.txt /usr/requirements.txt
WORKDIR /usr
RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models
COPY ./main.py /usr/main.py

ENTRYPOINT [ "python3" ]

CMD [ "src/main/main.py" ]