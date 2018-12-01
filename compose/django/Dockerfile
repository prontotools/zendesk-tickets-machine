FROM python:3.6.0

RUN pip install Django==1.11a1 \
    dj-database-url==0.4.2 \
    django-tables2==1.3.0 \
    psycopg2==2.7.1 \
    raven==5.32.0 \
    requests==2.20.1 \
    uWSGI==2.0.17.1

ENV APPLICATION_ROOT /app/

RUN mkdir $APPLICATION_ROOT
COPY . $APPLICATION_ROOT
COPY ./compose/django/entrypoint.sh /entrypoint.sh
COPY ./compose/django/ztm.ini $APPLICATION_ROOT\ztm.ini
RUN chmod +x /entrypoint.sh
WORKDIR $APPLICATION_ROOT
RUN pip install -r requirements.txt
