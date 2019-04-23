from redis import Redis
from rq.decorators import job
import requests
import time
import json

connection=Redis(host="some-redis", port=6379)
MAILGUN_DOMAIN_NAME="sandbox9d95d40e03da4f6b949e22a5b6259f26.mailgun.org"
MAILGUN_API_KEY="key-a47b29224335121b5591e4beb9bce80c"

@job('default', connection=connection)
def send_email(send_to, subject, text):

    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': 'Me <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
        'to': send_to,
        'subject': subject,
        'text': text,
    }

    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()

@job('default', connection=connection)
def get_synonym_words(url):
    resp = requests.get(url)
    array = [l['word'] for l in json.loads(resp.text)[:10]]
    return array
