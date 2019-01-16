FROM python:3.6-alpine

WORKDIR /home/checks_and_balances

COPY requirements.txt requirements.txt
RUN python -m venv flask

RUN flask/bin/pip install --upgrade pip
RUN flask/bin/pip install -r requirements.txt

COPY app.py ./
RUN chmod +x app.py

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./app.py"]
