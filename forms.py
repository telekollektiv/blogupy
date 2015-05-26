# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, TextAreaField, DateTimeField, SubmitField,
                     validators, ValidationError)


# Mail contact form
class ContactForm(Form):
    name = TextField("Dein Name", [validators.Required("Bitte trage Deinen Namen ein")])
    email = TextField("Deine E-Mail Adresse", [
                      validators.Required("Bitte trage eine E-Mail Adresse ein!"),
                      validators.Email("Die E-Mail Adresse ist nicht gültig!")])
    subject = TextField("Betreff", [
                        validators.Required("Bitte gib einen Betreff ein!.")])
    message = TextAreaField("Nachricht", [
                            validators.Required("Bitte trage eine Nachricht ein!")])
    submit = SubmitField("Senden")


# äöü ÄÖÜ

# Contribute Form
class BlogContributeForm(Form):
    author = TextField("Author")
    title = TextField("Titel", [validators.Required("Bitte gib einen Titel an!")])
    article = TextAreaField("Artikel", [validators.Required("Bitte schreibe einen Artikel")])
    submit = SubmitField("Senden")


class EventContributeForm(Form):
    title = TextField('Titel', [validators.Required('required')])
    author = TextField('Wer')
    location = TextField('Wo', [validators.Required('required')])
    date = DateTimeField('Wann', [validators.Required('required')], format='%Y-%m-%d %H:%M')
    stop = DateTimeField('Bis', [validators.Required('required')], format='%Y-%m-%d %H:%M')
    description = TextAreaField('Beschreibung', [validators.Required('required')])
    submit = SubmitField('Senden')
