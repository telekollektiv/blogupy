# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, TextAreaField, SubmitField,
                     validators, ValidationError)


# Mail contact form
class ContactForm(Form):
    name = TextField("Dein Name", [validators.Required("Bitte trage Deinen Namen ein")])
    email = TextField("E-Mail Adresse", [
                      validators.Required("Bitte trage eine E-Mail Adresse ein!"),
                      validators.Email("Die E-Mail Adresse ist nicht gültig!")])
    subject = TextField("Subject", [
                        validators.Required("Bitte gib einen Betreff ein!.")])
    message = TextAreaField("Message", [
                            validators.Required("Bitte trage eine Nachricht ein!")])
    submit = SubmitField("Senden")


# äöü ÄÖÜ

# Contribute Form
class ContributeForm(Form):
    author = TextField("Author")
    title = TextField("Titel", [validators.Required("Bitte gib einen Titel an!")])
    article = TextAreaField("Artikel", [validators.Required("Bitte schreibe einen Artikel")])
    submit = SubmitField("Senden")
