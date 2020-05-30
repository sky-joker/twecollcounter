# twecollcounter

[![Bulid Status](https://img.shields.io/travis/sky-joker/twecollcounter/master?style=for-the-badge)](https://travis-ci.org/sky-joker/twecollcounter)
[![](https://img.shields.io/github/license/sky-joker/twecollcounter?style=for-the-badge)](https://github.com/sky-joker/twecollcounter/blob/master/LICENSE.txt)
[![](https://img.shields.io/docker/image-size/skyjokerxx/twecollcounter?sort=date&style=for-the-badge)](https://hub.docker.com/repository/docker/skyjokerxx/twecollcounter)

This tool can collect a hash tag tweet from twitter, and aggregate each user tweet the number.

## Requirements

* Python 3.x
* pytz
* oauth2
* redis
* Twitter API
    * api key
    * api secret
    * token key
    * token secret

If you don't have Twitter API code, please issue it in the following site.

[https://developer.twitter.com/en](https://developer.twitter.com/en)

**How to generate a Bearer Token**

[https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0/bearer-tokens](https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0/bearer-tokens)

## Usage

### Install

Clone this repository and install the required python packages.

```
# git clone https://github.com/sky-joker/twecollcounter
# cd twecollcounter
# pip install -r requirements.txt
```

### Configuration

Please change the values in a configuration file.

```
# vi config.ini
```

By default, settings are read from environment variables.

```
[twitter_api]
api_key = %(twitter_api_api_key)s
api_secret = %(twitter_api_api_secret)s
token_key = %(twitter_api_token_key)s
token_secret = %(twitter_api_token_secret)s

[twitter_collection]
hash_tag = %(twitter_collection_hash_tag)s
count = %(twitter_collection_count)s
interval = %(twitter_collection_interval)s

[time]
zone = %(time_zone)s

[redis]
host = %(redis_host)s
port = %(redis_port)s
db = %(redis_db)s
```

**config value**

|    value     |                   description                   |
|--------------|-------------------------------------------------|
| api_key      | generated twitter api key                       |
| api_secret   | generated twitter api secret key                |
| token_key    | generated twitter token key                     |
| token_secret | generated twitter token secret                  |
| hash_tag     | hash tag to search(e.g #hashtag)                |
| count        | number of tweets to get at a time(max 100)      |
| interval     | interval of fetch tweets                        |
| zone         | time zone(e.g Asia/Tokyo)                       |
| host         | redis host to connect                           |
| port         | redis port to connect                           |
| db           | [redis logical database index][redis_index_ref] |

[redis_index_ref]:https://redis.io/commands/select

**environment variable**

The following is a correspondence table of setting values and environment variables.

| config value |     environment valiable    |
|--------------|-----------------------------|
| api_key      | twitter_api_api_key         |
| api_secret   | twitter_api_api_secret      |
| token_key    | twitter_api_token_key       |
| token_secret | twitter_api_token_secret    |
| hash_tag     | twitter_collection_hash_tag |
| count        | twitter_collection_count    |
| interval     | twitter_collection_interval |
| zone         | time_zone                   |
| host         | redis_host                  |
| port         | redis_port                  |
| db           | redis_db                    |

### Execution

Set config values to a configuration file or environment variables.  
For example, the following is set config values to environment variables.

```
# export twitter_api_api_key='XXXXXXXXXXXXXX'
# export twitter_api_api_secret='XXXXXXXXXXXXXX'
# export twitter_api_token_key='XXXXXXXXXXXXXX'
# export twitter_api_token_secret='XXXXXXXXXXXXXX'
# export twitter_collection_hash_tag='#popular_hashtag'
# export twitter_collection_count='100'
# export twitter_collection_interval='5'
# export time_zone='Asia/Tokyo'
# export redis_host='localhost'
# export redis_port='6379'
# export redis_db='0'
```

Execute this tool.

```
# ./src/twecollcounter/twecollcounter.py -c
```

### Aggregate

Aggregate tweets number of each user.

```
# ./src/twecollcounter/twecollcounter.py --aggregate
user_a : 10
user_b : 8
user_c : 5
(snip)
```

### If use Docker

If you use the prepared [container image](https://hub.docker.com/repository/docker/skyjokerxx/twecollcounter), execute the following command after set config values to environment variables.

```
docker run -itd --name twecollcounter --rm \
    -e twitter_api_api_key=$twitter_api_api_key \
    -e twitter_api_api_secret=$twitter_api_api_secret \
    -e twitter_api_token_key=$twitter_api_token_key \
    -e twitter_api_token_secret=$twitter_api_token_secret \
    -e twitter_collection_hash_tag=$twitter_collection_hash_tag \
    skyjokerxx/twecollcounter:latest
```

If you use an env file, execute the docker run command after changing the value in the env file.

```
# vi env.list
# docker run -itd --name test --rm --env-file env.list skyjokerxx/twecollcounter:latest
```

Checks whether the container has started.

```
# docker ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS               NAMES
e7db441e334f        skyjokerxx/twecollcounter:latest   "/bin/sh -c 'redis-s…"   54 minutes ago      Up 54 minutes                           twecollcounter
```

Aggregate tweets number of each user via container.

```
# docker exec -it twecollcounter twecollcounter.py --aggregate
user_a : 10
user_b : 8
user_c : 5
(snip)
```

## License

[MIT](https://github.com/sky-joker/twecollcounter/blob/master/LICENSE.txt)
