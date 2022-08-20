FROM postgres:latest

RUN apt update \
    && apt install -y libpq5 python3 python3-pip
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install "psycopg[binary,pool]"
