from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import feedparser
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list/<rss>')
def post_list(rss):
    full_link = "https://vnexpress.net/rss/" + rss
    NewsFeed = feedparser.parse(full_link)
    NewsFeed.feed['title'] = NewsFeed.feed['title'].split(' - ')[0]
    return render_template('post_list.html', NewsFeed=NewsFeed)


@app.route('/detail/<path:link>')
def detail(link):
    soup = BeautifulSoup(requests.get(link).content, 'lxml')
    title = soup.find(class_="title-detail").text
    paragraphs = soup.find("article")
    date = None
    try:
        date = soup.select_one('body > section.section.page-detail.top-detail > div > div.sidebar-1 > div.header-content.width_common > span').text
    except:
        pass
    return render_template('detail.html', title=title, date=date, paragraphs=(paragraphs))
