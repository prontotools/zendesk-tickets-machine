FROM python:3.6.0

RUN pip install Django==1.10.4 \
                psycopg2==2.6.2 \
                requests==2.12.3 \
                uWSGI==2.0.14

ENV APPLICATION_ROOT /app/

RUN mkdir $APPLICATION_ROOT
ADD . $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
