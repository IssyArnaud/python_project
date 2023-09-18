from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.vet import Vet
from models.animal import Animal
from app import db

vets_blueprint = Blueprint("vets", __name__)

@vets_blueprint.route('/vets')
def show_all():
    vets = Vet.query.all()
    return render_template('vets/all.jinja', vets=vets)

@vets_blueprint.route('/vets/<id>')
def show(id):
    vet = Vet.query.get(id)
    cases = Animal.query.filter_by(vet_id = id)
    return render_template('/vets/details.jinja', vet=vet, cases=cases)

@vets_blueprint.route('/vets/<id>/edit')
def edit(id):
    vet = Vet.query.get(id)
    return render_template('vets/edit.jinja', vet=vet)

@vets_blueprint.route('/vets/<id>/edit', methods=["POST"])
def update(id):
    vet = Vet.query.get(id)
    name = request.form["name"]
    vet.name = name
    db.session.commit()
    return redirect ('/vets') 
##############################
# WANT TO RETURN TO ('/vets/<id>') but it won't let me, it's not happy about the input type of <id>
##############################

@vets_blueprint.route('/vets/new')
def new():
    return render_template('vets/new.jinja')

@vets_blueprint.route('/vets/new', methods=["POST"])
def add():
    name = request.form["name"]
    new_vet = Vet(name=name)
    db.session.add(new_vet)
    db.session.commit()
    return redirect ('/vets')