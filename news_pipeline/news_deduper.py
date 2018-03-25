# -*- coding: utf-8 -*-
import os
import sys
import datetime

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://mycayzfr:E4nnofIrEfvgW4oByDmkoBjvsmobCzFG@termite.rmq.cloudamqp.com/mycayzfr"
DEDUPE_NEWS_TASK_QUEUE_NAME = "top-new-dedup-news-task-queue"
SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news" # table name in mongodb

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return

    task = msg
    text = str(task['text'])
    if text is None:
        return

    # Get all recent news
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day - 1, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=2)

    db = mongodb_client.get_db()
    recent_news_list = list(db[NEWS_TABLE_NAME].find({
        'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}
    }))

    if recent_news_list is not None and len(recent_news_list) > 0:
        print 'num of recent news in mongo:', len(recent_news_list)

        documents = [str(news['text']) for news in recent_news_list]
        documents.insert(0, text)

        # cal tf-idf similarity
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        print pairwise_sim.A
        rows = pairwise_sim.shape[0]

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                # duplicate news, ignore
                print 'Duplicate news. Ignore'
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])
    # replace if exist, else insert
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if dedupe_news_queue_client is not None:
        msg = dedupe_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print 'handle_message error:', e
                pass
        dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
