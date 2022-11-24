FROM python:3.9

WORKDIR /app

RUN pip3 install --upgrade pip

COPY requirements.txt /app/

RUN pip3 --no-cache install -r requirements.txt

COPY . .

EXPOSE 5000 465

RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

CMD ["python3","app.py"]