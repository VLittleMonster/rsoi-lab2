FROM python:3.10-alpine

#Change working directory
WORKDIR /code
COPY . /code
RUN pip3.10 install -r requirements.txt

EXPOSE 8050

CMD ["python3", "app/main.py"]
