# -*- coding: utf-8 -*-
import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = '''
    //p[contains(@class, 'zn-body__paragraph')]//text()
    | //div[contains(@class, 'zn-body__paragraph')]//text()
    | //div[@class='Paragraph__component']//text()
    | //p[@class='d-body-copy']//text()
    | //div[@class='zn-body__paragraph']//text()
    '''

# Load user agents for disguising http header
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []
with open(USER_AGENTS_FILE, 'r') as f:
    for ua in f.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1]) # get xxx in "xxx"
random.shuffle(USER_AGENTS)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection": "close",
        "User-Agent": ua
    }
    return headers

def extract_news(news_url):
    # download html
    # create session is more human
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeaders())

    # parse html
    news = ''
    try:
        tree = html.fromstring(response.content)
        # extract infomation
        news = tree.xpath(GET_CNN_NEWS_XPATH) # return a list of paragraphs
        news = ''.join(news) # gets a string for a news
        if len(news) == 0:
            print 'scraped nothing, url =', news_url
    except Exception as e:
        print e;
        return ''

    return news
