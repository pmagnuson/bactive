FROM python:3.7
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
VOLUME /app
ENV FLASK_ENV=development
CMD ["flask", "run","--host=0.0.0.0"]
