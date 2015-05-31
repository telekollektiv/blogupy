#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_flatpages import FlatPages
from flask.ext.mail import Message, Mail
from forms import ContactForm, BlogContributeForm, EventContributeForm
from datetime import datetime
from ghettodown import ghettodown
from utils import write_article, get_section, freeze_meta, unfreeze_meta, strptime
from contribute import receive_article, _receive_article, receive_event, _receive_event
import shutil
import logic
import yaml
import sys
import os
import re

mail = Mail()

app = Flask(__name__)
flatpages = FlatPages(app)

app.config.from_object('config')
app.config['FLATPAGES_HTML_RENDERER'] = ghettodown
app.secret_key = 'development key'
mail.init_app(app)


rt = render_template


def render_template(*args, **kwargs):
    return rt(*args, qs=request.query_string, **kwargs)


def notify(group, subject, body, template=None):
    try:
        recv = app.config[group]
        sender = app.config["MAIL_USERNAME"]
        msg = Message(subject, sender=sender, recipients=[recv])

        if body.startswith('/'):
            body = app.config['SELF'] + body

        if template:
            body = template % body

        msg.body = body
        mail.send(msg)
    except:
        pass


def prepare_article(article):
    article = {
        'meta': article.meta,
        'path': article.path,
        'html': article.html
    }
    return article


def get_articles(prefix=''):
    def f(a):
        if not a.path.startswith(prefix):
            return False

        stop = a.meta.get('stop')
        if stop and strptime(stop) < datetime.now():
            return False

        return True
    articles = [prepare_article(a) for a in flatpages if f(a)]
    articles.sort(key=lambda item: item['meta']['date'], reverse=True)
    return articles


@app.route('/')
def index():
    articles = get_articles('articles/')
    return render_template('index.html', posts=articles)


for url, template in app.config['CUSTOM_PAGES']:
    @app.route(url)
    def dynamic():
        return render_template(template)


@app.route('/<name>.html')
def post(name):
    post = flatpages.get_or_404('articles/' + name)
    return render_template('article.html', post=post)


@app.route('/termine/')
def events():
    events = get_articles('events/')
    return render_template('events.html', events=events)


@app.route('/contribute/', methods=['GET', 'POST'])
def contribute():
    return contribute_section('blog')


@app.route('/contribute/<section>', methods=['GET', 'POST'])
def contribute_section(section):
    form = logic.sections[section]['form'](**prepopulate)

    if request.method == 'POST':
        if not form.validate():
            if request.query_string:
                resp = jsonify({'status': 'error'})
                resp.status_code = 400
                return resp
            else:
                return render_template('contribute/' + section + '.html', section=section, form=form)
        else:
            if section == 'events':
                post = receive_event(form)
                notify('MAIL_RECV_MODERATE', 'Please unlock event: %s' % post['title'], '/moderate/')
            else:
                post = receive_article(form)
                notify('MAIL_RECV_MODERATE', 'Please unlock article: %s' % post['title'], '/moderate/')

            if request.query_string:
                return jsonify({'status': 'success'})
            else:
                return redirect('/contribute/done')
    else:
        return render_template('contribute/' + section + '.html', section=section, form=form)


@app.route('/contribute/done')
def contribute_done():
    return render_template('contribute.html', success=True)


@app.route('/moderate/')
def moderate():
    articles = get_articles()
    return render_template('moderate.html', posts=articles)


def load_content_for_moderation(path):
    if '..' in path:
        return ''
    section = get_section(path)
    content = flatpages.get_or_404(path)
    prepopulate = unfreeze_meta(dict(content.meta))
    prepopulate['content'] = content.body

    form = logic.sections[section]['form'](**prepopulate)

    return section, content, form


@app.route('/moderate/<path:path>')
def moderate_content(path):
    section, content, form = load_content_for_moderation(path)
    return render_template('moderate/' + section + '.html', form=form, post=content, path=path)


@app.route('/moderate/<path:path>', methods=['POST'])
def moderate_post_post(path):
    section, content, form = load_content_for_moderation(path)
    post = content

    if 'update' in request.form:
        if not form.validate():
            return moderate_content(path)

        directory = '/'.join(path.split('/')[:-1])

        if section == 'events':
            event, body = _receive_event(form)
            write_article(directory, form.title.data, event, body)
            notify('MAIL_RECV_MODERATE', 'Edited event: %s' % event['title'], 'It\'s 20% cooler now')
        else:
            article, body = _receive_article(form)
            write_article(directory, form.title.data, article, body)
            notify('MAIL_RECV_MODERATE', 'Edited article: %s' % post['title'], 'It\'s 20% cooler now')
    elif 'unlock' in request.form:
        dest = path[len('drafts/'):]
        shutil.move('content/%s.md' % path, 'content/%s.md' % dest)
        notify('MAIL_RECV_MODERATE', 'freigeschaltet: %s' % dest, '/%s.html' % dest)
    elif 'delete' in request.form:
        src = 'content/%s.md' % path
        if os.path.exists(src):
            shutil.move(src, 'content/depublicate/%s.md' % path)
        notify('MAIL_RECV_MODERATE', 'geloescht: %s' % path, ':\'(')
    else:
        return 'invalid action'
    return redirect('/moderate/')


@app.route('/kontakt/', methods=['GET', 'POST'])
def kontakt():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('kontakt.html', form=form)
        else:
            subject = form.subject.data
            body = 'From: %s <%s>\n\n%s' % (form.name.data, form.email.data, form.message.data)
            notify('MAIL_RECV_CONTACT', subject, body)
            return redirect('/kontakt/done')
    elif request.method == 'GET':
        return render_template('kontakt.html', form=form)


@app.route('/kontakt/done')
def kontakt_done():
    return render_template('kontakt.html', success=True)


if __name__ == "__main__":
    app.run(debug=True)
