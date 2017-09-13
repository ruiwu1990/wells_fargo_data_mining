FROM ubuntu:14.04
MAINTAINER Rui Wu
LABEL description="Wells Fargo Data Mining."

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential cmake gdal-bin libgdal-dev



ENV PYTHONPATH /var/www/data_mining

#copy source code
COPY requirements.txt /var/www/data_mining/requirements.txt
WORKDIR /var/www/data_mining
RUN pip install -r requirements.txt
COPY . /var/www/data_mining



EXPOSE 5000
ENV DATA_MINING_PORT 80
ENV DATA_MINING_HOST 0.0.0.0
EXPOSE ${DATA_MINING_PORT}

CMD python views.py -p 5000 --threaded