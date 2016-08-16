FROM python:2.7-alpine
MAINTAINER Sang Han <jjangsangy@gmail.com>
ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt

RUN apk add --no-cache --virtual .build-deps \
        build-base \
        zlib \
        zlib-dev \
        curl \
        jpeg \
        jpeg-dev \
        libpng \
        libpng-dev \
        python-dev \
        libxml2-dev \
        libxslt-dev \
        py-pip \
    && CFLAGS="$CFLAGS -L/lib" pip install -r requirements.txt \
    && find /usr/local \( -type d -a -name test -o -name tests \) \
            -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            -exec rm -rf '{}' + \
    && runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u)" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

COPY . .

RUN python -m nltk.downloader punkt
CMD gunicorn -b 0.0.0.0:8000 ExplainToMe.wsgi:app
