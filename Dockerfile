FROM python:3.9

WORKDIR /app

RUN pip3 install --upgrade pip

COPY requirements.txt /app/

RUN pip3 --no-cache install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3","app.py"]