FROM python:alpine

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps .pynacl_deps

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

COPY . /usr/src/app

CMD ["/usr/src/app/entrypoint.sh"]