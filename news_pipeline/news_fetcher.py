# -*- coding: utf-8 -*-
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://mycayzfr:E4nnofIrEfvgW4oByDmkoBjvsmobCzFG@termite.rmq.cloudamqp.com/mycayzfr"
DEDUPE_NEWS_TASK_QUEUE_NAME = "top-new-dedup-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://oibmmghn:sKrkMTtm55KnbDfURC0ouVbuF06pQigw@termite.rmq.cloudamqp.com/oibmmghn"
SCRAPE_NEWS_TASK_QUEUE_NAME = "top-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    text = None

    # support CNN only now
    if task['source'] == 'cnn':
        print 'scraping CNN news'
        text = cnn_news_scraper.extract_news(task['url'])
        if len(text) == 0:
            print 'scraped zero text, skip the task...'
            return
    else:
        print 'news source [%s] is not supported.' % task['source']
        return

    task['text'] = text
    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print 'handle_message error:', e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
