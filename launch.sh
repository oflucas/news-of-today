#!/bin/bash

#brew services start redis_6379
#brew services start mongodb

pip install -r requirements.txt

python news_pipeline/news_monitor.py > news_monitor.log &
python news_pipeline/news_fetcher.py > news_fetcher.log &
python news_pipeline/news_deduper.py > news_deduper.log &

echo "================"
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
