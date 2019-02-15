#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms import SelectField, FormField, FieldList
from wtforms.validators import Required 

blad1 = 'To pole jest wymagane!'

class KlasaForm(FlaskForm):
    id = HiddenField()
    klasa = StringField('Numer klasy: ', validators=[Required(message="blad_1")])
    rok_naboru = StringField('Rok matury: ', validators=[Required(message="blad_1")])
    rok_matury = StringField('Rok matury: ', validators=[ Required(message="blad_1")])


class UczenForm(FlaskForm):
    id = HiddenField()
    imie = StringField('Imie: ', validators=[ Required(message="blad_1")])
    nazwisko = StringField('Nazwisko: ', validators=[ Required(message="blad_1")])
    plec = SelectField('Płeć: ', coerce=int)
    klasa = SelectField('Klasa: ', coerce=int)
