From python:3.6

ENV twitter_api_api_key ''
ENV twitter_api_api_secret ''
ENV twitter_api_token_key ''
ENV twitter_api_token_secret ''
ENV twitter_collection_hash_tag ''
ENV twitter_collection_count 100
ENV twitter_collection_interval 5
ENV time_zone Asia/Tokyo
ENV redis_host localhost
ENV redis_port 6379
ENV redis_db 0
ENV PATH /twecollcounter:$PATH

RUN apt-get update
RUN apt-get -y install redis
RUN mkdir /twecollcounter

ADD requirements.txt /twecollcounter
ADD src/twecollcounter/twecollcounter.py /twecollcounter
ADD config.ini /twecollcounter
RUN pip install -r /twecollcounter/requirements.txt

WORKDIR /twecollcounter

CMD redis-server /etc/redis/redis.conf && twecollcounter.py --config /twecollcounter/config.ini -c
