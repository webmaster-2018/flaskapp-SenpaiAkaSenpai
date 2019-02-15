#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, request
from flask import redirect, url_for, flash, abort
from modele import *
from forms import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/lista_kl")
def lista_kl():
    return render_template('lista_kl.html')

@app.route("/lista_ucz")
def lista_ucz():
    return render_template('lista_ucz.html')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            if type(error) is list:
                error = error[0]
            flash("Błąd: {}. Pole: {}".format(
                error,
                getattr(form, field).label.text))


@app.route("/dodaj_ucz", methods=['GET', 'POST'])
def dodaj():
    form = UczenForm()
    form.kategoria.choices = [(k.id, k.kategoria) for k in Kategoria.select()]
    
    if form.validate_on_submit():
        print(form.data)
        k = klasa(pytanie=form.klasa.data, rok_naboru=form.kategoria.data, rok_matury=form.rok_matury.data)
        k.save()
        for o in form.odpowiedzi.data:
            odp = Odpowiedz(odpowiedz=o['odpowiedz'],
                            pytanie=p.id,
                            odpok=int(o['odpok']))
            odp.save()
        flash('Dodano pytanie: {}'.format(form.pytanie.data))
        return redirect(url_for('lista'))
    elif request.method == 'POST':
        flash_errors(form)
    
    return render_template('dodaj.html', form=form)

@app.route("/dodaj_kl", methods=['GET', 'POST'])
def dodaj():
    form = KlasaForm()
    form.kategoria.choices = [(k.id, k.kategoria) for k in Kategoria.select()]
    
    if form.validate_on_submit():
        print(form.data)
        p = Pytanie(pytanie=form.pytanie.data, kategoria=form.kategoria.data)
        p.save()
        for o in form.odpowiedzi.data:
            odp = Odpowiedz(odpowiedz=o['odpowiedz'],
                            pytanie=p.id,
                            odpok=int(o['odpok']))
            odp.save()
        flash('Dodano pytanie: {}'.format(form.pytanie.data))
        return redirect(url_for('lista'))
    elif request.method == 'POST':
        flash_errors(form)
    
    return render_template('dodaj.html', form=form)


def get_or_404(pid):
    try:
        p = Pytanie.get_by_id(pid)
        return p
    except Pytanie.DoesNotExist:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/edytuj/<int:pid>", methods=['GET', 'POST'])
def edytuj(pid):
    p = get_or_404(pid)
    form = PytanieForm(obj=p)
    form.kategoria.choices = [(k.id, k.kategoria) for k in Kategoria.select()]
    form.kategoria.data = p.kategoria.id
    
    if form.validate_on_submit():
        print(form.data)
        p.pytanie = form.pytanie.data
        p.kategoria = form.kategoria.data
        p.save()
        for o in form.odpowiedzi.data:
            odp = Odpowiedz.get_by_id(o['id'])
            odp.odpowiedz = o['odpowiedz']
            odp.odpok = int(o['odpok'])
            odp.save()
        flash("Zaktualizowano pytanie: {}".format(form.pytanie.data))
        return redirect(url_for('lista_ucz'))
    elif request.method == 'POST':
        flash_errors(form)
    
    
    odpowiedzi = []
    for o in Odpowiedz.select().where(Odpowiedz.pytanie == p.id).dicts():
        odpowiedzi.append(o)
        
    print(odpowiedzi)
    
    return render_template("edytuj.html", form=form)

@app.route("/usun/<int:pid>", methods=['GET', 'POST'])
def usun(pid):
    p = get_or_404(pid)
    if request.method == 'POST':
        flash('Usunięto pytanie {}'.format(p.pytanie), 'sukces')
        for o in Odpowiedz.select().where(Odpowiedz.pytanie == p.id):
            o.delete_instance()
        p.delete_instance()
        return redirect(url_for('lista_ucz'))   
         
        return render_template("pytanie_usun.html", pytanie = p)
