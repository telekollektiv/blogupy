from utils import write_article, strptime, strftime
from datetime import datetime


def _receive_article(form):
    article = {}
    article['title'] = form.title.data.encode('utf8')
    article['author'] = form.author.data.encode('utf8') or 'Anonymous'
    article['date'] = strftime(datetime.now())
    body = form.content.data.encode('utf8')

    return article, body


def receive_article(form):
    article, body = _receive_article(form)
    write_article('drafts/articles', form.title.data, article, body)
    return article


def _receive_event(form):
    event = {}
    event['title'] = form.title.data.encode('utf8')
    event['author'] = form.author.data.encode('utf8') or 'Anonymous'
    event['location'] = form.location.data.encode('utf8')
    event['date'] = strftime(form.date.data)
    event['stop'] = strftime(form.stop.data)
    body = form.content.data.encode('utf8')

    return event, body


def receive_event(form):
    event, body = _receive_event(form)
    write_article('drafts/events', form.title.data, event, body)
    return event
