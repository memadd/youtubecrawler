# youtubecrawler
crawler for youtube channels or playlists and scheduling crawlers to run periodically
# Prerequisites

install docker and docker compose

# Installing

clone repo start all services using docker compose
# Technologies

- Scrapy: Crawling the playlist

- Splash: Handling pages with Javascript

- scrapyd: api for scrapy to start spiders remotly

- Mongodb: Storing saved items

- Celery: Scheduling the spiders instances to run periodically

- Rabbitmq: Message broker for celery .
