FROM python

COPY . /app
WORKDIR /app

RUN mkdir -p /results

ENV PATH_TO_PORTS_FILE=data/storage_asof_20200101.parquet
ENV PATH_TO_EVENT_FILE=data/cargo_movements.parquet
ENV USE_MULTIPROCESSING=True
ENV LOG_LEVEL=INFO
ENV MAX_DATETIME='14/01/2020 00:00:00'

RUN pip3 install -r requirements.txt

CMD python3 ./app.py
