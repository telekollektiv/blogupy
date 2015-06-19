# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, TextAreaField, DateTimeField, SubmitField,
                     validators, ValidationError)


# Mail contact form
class ContactForm(Form):
    name = TextField("Your name:", [validators.Required("Name required!")])
    email = TextField("Your mail address", [
                      validators.Required("Valid mail address required!!"),
                      validators.Email("Not a valid mail address!")])
    subject = TextField("Subject:", [
                        validators.Required("Pleas enter a subject!")])
    message = TextAreaField("Message", [
                            validators.Required("Please enter a message!")])
    submit = SubmitField("Submit")


# äöü ÄÖÜ

# Contribute Form
class BlogContributeForm(Form):
    author = TextField("Author")
    title = TextField("Title", [validators.Required("Please enter a title!")])
    article = TextAreaField("Article", [validators.Required("Please write an article!")])
    submit = SubmitField("Submit")


class EventContributeForm(Form):
    title = TextField('Event name', [validators.Required('required')])
    author = TextField('Who')
    location = TextField('Where', [validators.Required('required')])
    date = DateTimeField('From', [validators.Required('required')], format='%Y-%m-%d %H:%M')
    stop = DateTimeField('To', [validators.Required('required')], format='%Y-%m-%d %H:%M')
    description = TextAreaField('Description', [validators.Required('required')])
    submit = SubmitField('Submit')
