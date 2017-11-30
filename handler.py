import imp
import json
import os
import sys

sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
import requests

MAILGUN_DOMAIN_NAME = os.environ['MAILGUN_DOMAIN_NAME']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
EMAIL = os.environ["EMAIL"] # Emails will be sent to this address


def run(event, context):
    items = []

    def add_item(item):
        items.append(item)

    # Create and run the crawler, scrapy stuff
    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler('broken_link_spider')
    crawler.signals.connect(add_item, signals.item_passed) # Intercept the results
    process.crawl(crawler)
    process.start()

    # Convert results to json and send email
    json_string = json.dumps([ob.__dict__ for ob in items])
    print("Found broken links:", json_string)
    send_simple_message(EMAIL, json_string)


def send_simple_message(to, content):
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': 'Link Checker <noreply@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': to,
        'subject': 'Results of Broken Links',
        'text': content,
    }
    print(data)
    response = requests.post(url, auth=auth, data=data)
    print(response.content)
    response.raise_for_status()
