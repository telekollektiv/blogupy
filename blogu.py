#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_flatpages import FlatPages
from flask.ext.mail import Message, Mail
from forms import ContactForm, ContributeForm
from datetime import datetime
from ghettodown import ghettodown
import shutil
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
    article['meta']['date'] = article['meta']['date'][:19]
    return article


def get_articles(prefix=''):
    articles = [prepare_article(a) for a in flatpages if a.path.startswith(prefix)]
    articles.sort(key=lambda item: item['meta']['date'], reverse=True)
    return articles

def write_article(diretory, title, article, body):
    output = yaml.dump(article, default_flow_style=False, allow_unicode=True) + '\n' + body
    output = output.replace('!!python/str ', '')

    path = re.sub('[^a-z0-9]', '_', title.lower())
    with open('content/drafts/%s.md' % path, 'w') as f:
        f.write(output)


@app.route('/')
def index():
    articles = get_articles(app.config['POST_DIR'])
    return render_template('index.html', posts=articles)


@app.route('/index.json')
def json_articles():
    articles = get_articles(app.config['POST_DIR'])
    return jsonify({'articles': articles})


for url, template in app.config['CUSTOM_PAGES']:
    @app.route(url)
    def dynamic():
        return render_template(template)


@app.route('/<name>.html')
def post(name):
    postdir = app.config['POST_DIR']
    path = '{}/{}'.format(postdir, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/contribute/', methods=['GET', 'POST'])
def contribute():
    form = ContributeForm()
    if request.method == 'POST':
        if not form.validate():
            if request.query_string:
                resp = jsonify({'status': 'error'})
                resp.status_code = 400
                return resp
            else:
                return render_template('contribute.html', form=form)
        else:
            post = {}
            post['title'] = form.title.data.encode('utf8')
            post['author'] = form.author.data.encode('utf8') or 'Anonymous'
            post['date'] = str(datetime.now())
            body = form.article.data.encode('utf8')

            write_article('drafts', form.title.data, post, body)
            notify('MAIL_RECV_MODERATE', 'Please unlock post: %s' % post['title'], '/moderate/')

            if request.query_string:
                return jsonify({'status': 'success'})
            else:
                return redirect('/contribute/done')
    else:
        return render_template('contribute.html', form=form)


@app.route('/contribute/done')
def contribute_done():
    return render_template('contribute.html', success=True)


@app.route('/moderate/')
def moderate():
    articles = get_articles()
    return render_template('moderate.html', posts=articles)


@app.route('/moderate/<name>')
def moderate_post(name):
    for postdir in [app.config['POST_DIR'], 'drafts']:  # TODO: don't hardcode drafts/
        path = '{}/{}'.format(postdir, name)
        if os.path.exists('content/%s.md' % path):
            break
    post = flatpages.get_or_404(path)
    return render_template('moderate_article.html', post=post)


@app.route('/moderate/<post>', methods=['POST'])
def moderate_post_post(post):
    if 'update' in request.form:
        for postdir in [app.config['POST_DIR'], 'drafts']:  # TODO: don't hardcode drafts/
            path = '{}/{}'.format(postdir, post)
            if os.path.exists('content/%s.md' % path):
                break
        post = flatpages.get_or_404(path)
        body = request.form['body']
        print(repr(body))

        diretory = post.path.split('/')[0]
        write_article(diretory, post.meta['title'], post.meta, body)
        notify('MAIL_RECV_MODERATE', 'Edited post: %s' % post['title'], 'It\'s 20% cooler now')
    elif 'unlock' in request.form:
        shutil.move('content/drafts/%s.md' % post, 'content/posts/%s.md' % post)
        notify('MAIL_RECV_MODERATE', 'freigeschaltet: %s' % post, '/%s.html' % post)
    elif 'delete' in request.form:
        for path in ['content/drafts/%s.md', 'content/posts/%s.md']:
            if os.path.exists(path % post):
                shutil.move('content/drafts/%s.md' % post, 'content/depublicate/%s.md' % post)
        notify('MAIL_RECV_MODERATE', 'geloescht: %s' % post, ':\'(')
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
            body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            notify('MAIL_RECV_CONTACT', subject, body)
            return redirect('/kontakt/done')
    elif request.method == 'GET':
        return render_template('kontakt.html', form=form)


@app.route('/kontakt/done')
def kontakt_done():
    return render_template('kontakt.html', success=True)


if __name__ == "__main__":
    app.run(debug=True)
