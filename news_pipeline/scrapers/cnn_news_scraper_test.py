import cnn_news_scraper as scraper

EXPECTED_NEWS = "It's interface is easy to use and eye catching."
CNN_NEWS_URL = "http://edition.cnn.com/travel/article/inflighto-airplane-tracking-app/index.html?iid=ob_article_footer_expansion"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    print(news)
    assert EXPECTED_NEWS in news
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
