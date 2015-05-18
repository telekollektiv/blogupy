# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, PasswordField, TextAreaField, SubmitField,
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


# have some free umlauts
# äöü ÄÖÜ

# Contribute Form
class ContributeForm(Form):
    author = TextField("Author")
    title = TextField("Titel", [validators.Required("Bitte gib einen Titel an!")])
    article = TextAreaField("Artikel", [validators.Required("Bitte schreibe einen Artikel")])
    submit = SubmitField("Senden")


class LoginForm(Form):
    username = TextField('Username', [validators.Required('Bitte gib einen Usernamen ein')])
    password = PasswordField('Password', [validators.Required('Bitte gib ein Passwort ein')])
    submit = SubmitField('Login')
