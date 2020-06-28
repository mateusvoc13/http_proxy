FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-docker
WORKDIR /django-docker
COPY requirements.txt /django-docker/
RUN pip install -r requirements.txt
COPY . /django-docker/

COPY Makefile /Makefile
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]