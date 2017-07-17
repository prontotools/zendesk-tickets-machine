FROM nginx:1.11.4-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY uwsgi_params /etc/nginx/uwsgi_params
COPY ztm.conf /etc/nginx/conf.d/ztm.conf

CMD /usr/sbin/nginx -g "daemon off;"
