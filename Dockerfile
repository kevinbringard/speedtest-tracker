# Multistage build setup
FROM debian:buster-slim as speedtest-builder

WORKDIR /usr/src/speedtest

ENV PACKAGES="\
    build-essential \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    cmake \
    git \
    "

RUN \
    apt-get update \
    && apt-get install -y ${PACKAGES} \
    && git clone https://github.com/taganaka/SpeedTest \
    && cd SpeedTest \
    && cmake -DCMAKE_BUILD_TYPE=Release . \
    && make install

# This is the target container
FROM debian:buster-slim
LABEL maintainer "Kevin Bringard <kevinbringard@gmail.com>"

ENV PACKAGES="\
    libcurl4 \
    libxml2 \
    "
COPY --from=speedtest-builder /usr/local/bin/SpeedTest /SpeedTest

COPY speedtest.sh /speedtest.sh

RUN \
    chmod +x /speedtest.sh \
    && apt-get update \
    && apt-get -y install ${PACKAGES} \
    && apt-get -y autoremove \
    && apt-get -y clean \
    &&  rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash

CMD ["/speedtest.sh"]
