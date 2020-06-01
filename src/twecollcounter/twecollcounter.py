#!/usr/bin/env python
from datetime import datetime, timedelta
from configparser import ConfigParser
from urllib.parse import quote
from time import sleep
import pytz
import json
import oauth2
import redis
import threading
import argparse
import os
import sys


def options():
    parser = argparse.ArgumentParser(prog='twecollconter',
                                     add_help=True,
                                     description='This tool can collect a hash tag tweet from twitter, and aggregate each user tweet the number.')

    parser.add_argument('--collect', '-c',
                        action='store_true',
                        help='start collection hash tag tweet from twitter')

    parser.add_argument('--config',
                        type=str,
                        help='configuration file path')

    parser.add_argument('--aggregate',
                        action='store_true',
                        help='aggregate tweet results count each user')

    parser.add_argument('--all-delete',
                        action='store_true',
                        help='delete all data from Redis')

    if len(sys.argv) == 1:
        parser.print_help()

    args = parser.parse_args()

    return args


def oauth_req(url, api_key, api_secret, token_key, token_secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=api_key, secret=api_secret)
    token = oauth2.Token(key=token_key, secret=token_secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body.encode('utf-8'), headers=http_headers)
    return content


def collect_tweet(url, api_key, api_secret, token_key, token_secret, redis_cli, collection_interval):
    compare_time = datetime.now().replace(second=0, microsecond=0)
    compare_time = compare_time.astimezone(pytz.timezone(time_zone))
    data = json.loads(oauth_req(url, api_key, api_secret, token_key, token_secret))

    for t in data['statuses']:
        twitter_user = t['user']['screen_name']
        if 'retweeted_status' not in t:
            tweet_time = datetime.strptime(t['created_at'], '%a %b %d %H:%M:%S %z %Y')
            tweet_time = tweet_time.astimezone(pytz.timezone(time_zone))
            if tweet_time >= compare_time:
                redis_cli.set(str(tweet_time) + twitter_user, twitter_user)


if __name__ == "__main__":
    args = options()

    # Parse a config file.
    config = ConfigParser(os.environ)
    if args.config:
        config.read(args.config)
    else:
        config.read('config.ini')

    api_key = config.get('twitter_api', 'api_key')
    api_secret = config.get('twitter_api', 'api_secret')
    token_key = config.get('twitter_api', 'token_key')
    token_secret = config.get('twitter_api', 'token_secret')

    collection_hash_tag = quote(config.get('twitter_collection', 'hash_tag'))
    collection_count = config.get('twitter_collection', 'count')
    collection_interval = int(config.get('twitter_collection', 'interval'))

    time_zone = config.get('time', 'zone')

    # redis
    redis_host = config.get('redis', 'host')
    redis_port = config.get('redis', 'port')
    redis_db = config.get('redis', 'db')

    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
    redis_cli = redis.StrictRedis(connection_pool=pool)

    if args.collect:
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + collection_hash_tag + '&count=' + collection_count

        while True:
            t = threading.Thread(target=collect_tweet(url, api_key, api_secret, token_key, token_secret, redis_cli,
                                                      collection_interval))
            t.start()
            sleep(collection_interval)

    if args.aggregate:
        collection_results = {}
        keys = redis_cli.keys('*')

        for key in keys:
            twitter_user = redis_cli.get(key).decode('utf-8')
            if twitter_user in collection_results:
                collection_results[twitter_user] += 1
            else:
                collection_results[twitter_user] = 1

        sorted_collection_results = sorted(collection_results.items(), key=lambda x:x[1], reverse=True)
        for result in sorted_collection_results:
            print(result[0] + " : " + str(result[1]))

    if args.all_delete:
        keys = redis_cli.keys('*')

        for key in keys:
            redis_cli.delete(key)
