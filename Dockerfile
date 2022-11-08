FROM python:3.8.15-slim-buster

ADD ./ /service/

WORKDIR /service

RUN pip install google-play-scraper

RUN pip install flatdict

RUN pip install google-search-results

RUN pip install beautifulsoup4

RUN pip install cloudscraper

RUN pip install fake-useragent

RUN pip install parsel

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["Controller.py" ]
