#!/usr/bin/env python
from flask import Flask, render_template, request, flash, redirect
from flask_flatpages import FlatPages
#from flask_frozen import Freezer
from flask.ext.mail import Message, Mail
#from flask.ext.pagedown import PageDown
from forms import ContactForm, ContributeForm
from datetime import datetime
from ghettodown import ghettodown
from uuid import uuid4 as uuid
import yaml
import sys

mail = Mail()

app = Flask(__name__)
flatpages = FlatPages(app)
#freezer = Freezer(app)
#pagedown = PageDown(app)

app.config.from_object('config')
app.secret_key = 'development key'
mail.init_app(app)


@app.route('/')
def posts():
    postdir = app.config['POST_DIR']
    posts = [p for p in flatpages if p.path.startswith(postdir)]
    posts.sort(key=lambda item: item['date'], reverse=False)
    return render_template('index.html', posts=posts)


@app.route('/projekt')
def projekt():
    return render_template('projekt.html')


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
        # print (type(form.title.data))
        if not form.validate():
            return render_template('contribute.html', form=form)
        else:
            post = {}
            post['title'] = str(form.title.data)
            post['author'] = str(form.author.data) or 'Anonymous'
            post['date'] = datetime.now().strftime('%d.%m.%Y')
            body = str(form.article.data)
            output = yaml.dump(post, default_flow_style=False) + '\n' + body

            id = str(uuid())

            with open('content/drafts/%s.md' % id, 'w') as f:
                f.write(output)

            # TODO: send email with unlock code=id

            return redirect('/contribute/done')
            # return ghettodown(form.article.data)
    else:
        return render_template('contribute.html', form=form)


@app.route('/contribute/done')
def contribute_done():
    return render_template('contribute.html', success=True)


@app.route('/moderate/')
def moderate():
    return render_template('moderate.html', posts=flatpages)


@app.route('/moderate/', methods=['POST'])
def moderate_post():
    return '\\(-_-)/'


@app.route('/kontakt/', methods=['GET', 'POST'])
def kontakt():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('kontakt.html', form=form)
        else:
            user = app.config["MAIL_USERNAME"]
            msg = Message(form.subject.data, sender=user, recipients=[user])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return redirect('/kontakt/done')
    elif request.method == 'GET':
        return render_template('kontakt.html', form=form)


@app.route('/kontakt/done')
def kontakt_done():
    return render_template('kontakt.html', success=True)


if __name__ == "__main__":
    '''
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
    '''

    app.config['FLATPAGES_HTML_RENDERER'] = ghettodown
    app.run(debug=True)
