FROM sequenceiq/hadoop-docker:2.7.0
MAINTAINER Rui Wu
LABEL description="Wells Fargo Data Mining."

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential cmake gdal-bin libgdal-dev

#copy source code
COPY . /data_mining
WORKDIR /data_mining
RUN pip install -r requirements.txt
ENV PYTHONPATH /data_mining

EXPOSE 5000
ENV DATA_MINING_PORT 80
ENV DATA_MINING_HOST 0.0.0.0
EXPOSE ${DATA_MINING_PORT}

CMD python views.py -p ${DATA_MINING_PORT} --threaded