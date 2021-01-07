# Pull base image
FROM python:3.7
# Set environment varibles
# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# DEBUG=True;DB_URL=sqlite:///./core/db/src/sql_app.db
#ENV DEBUG True
ENV DOCKER_RUN True
#ENV SERVER_URL_ "192.168.31.19"
ENV DB_URL sqlite:///./core/db/src/sql_app.db

#WORKDIR /server/

# Install dependencies
#RUN pip install pipenv
#COPY Pipfile Pipfile.lock /code/
#RUN pipenv install --system --dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./config/ /config
COPY ./core/ /core
COPY ./processing/ /processing
COPY ./static/ /static
COPY ./templates/ /templates
COPY ./app.py /app.py


EXPOSE 5002
#EXPOSE 22
CMD ["python", "app.py"]

# docker build -t server_pi_beacon .
# docker run -p 5002:5002 --env DEBUG=True --env SERVER_URL=192.168.31.19 --name server_pi_beacon server_pi_beacon:latest
