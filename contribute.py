from utils import write_article

def receive_article(form):
    post = {}
    post['title'] = form.title.data.encode('utf8')
    post['author'] = form.author.data.encode('utf8') or 'Anonymous'
    post['date'] = str(datetime.now())
    body = form.article.data.encode('utf8')

    write_article('drafts/articles', form.title.data, post, body)
    return post


def _receive_event(form):
    event = {}
    event['title'] = form.title.data.encode('utf8')
    event['author'] = form.author.data.encode('utf8') or 'Anonymous'
    event['location'] = form.location.data.encode('utf8')
    event['date'] = form.date.data.strftime('%Y-%m-%d %H:%M')
    event['stop'] = form.stop.data.strftime('%Y-%m-%d %H:%M')
    body = form.description.data.encode('utf8')

    return event, body


def receive_event(form):
    event, body = _receive_event(form)
    write_article('drafts/events', form.title.data, event, body)
    return event
