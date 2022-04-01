FROM python:3.9

RUN pip install pip -U

WORKDIR /var/api
COPY ./app /var/api/app
COPY requirements.txt /var/api

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "-c"]

CMD ["python -m uvicorn app.main:app"]
