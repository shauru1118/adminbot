FROM python:3.13-slim-buster

WORKDIR /adminbot

COPY requirements.txt requirements.txt

RUN python3 -m venv /venv
RUN /venv/bin/python3 -m pip install --upgrade pip
RUN /venv/bin/pip3 install --upgrade pip setuptools
RUN /venv/bin/pip3 install -r requirements.txt

COPY main.py .
COPY .env .

ENV PATH="/venv/bin:$PATH"

CMD [ "python3", "main.py" ]
