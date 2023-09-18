from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.animal import Animal
from models.vet import Vet
from app import db

animals_blueprint = Blueprint("animals", __name__)

@animals_blueprint.route('/animals')
def show_all():
    animals = Animal.query.all()
    return render_template('animals/all.jinja', animals=animals)

@animals_blueprint.route('/animals/<id>')
def show(id):
    animal = Animal.query.get(id)
    vet = Vet.query.get(animal.vet_id)
    return render_template('animals/details.jinja', animal=animal, vet=vet)

@animals_blueprint.route('/animals/<id>/edit')
def edit(id):
    animal = Animal.query.get(id)
    vets = Vet.query.all()
    return render_template('animals/edit.jinja', animal=animal, vets=vets)

@animals_blueprint.route('/animals/<id>/edit', methods=["POST"])
def update(id):
    animal = Animal.query.get(id)
    name = request.form["name"]
    species = request.form["species"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    animal.name = name
    animal.species = species
    animal.dob = dob
    animal.phone = phone
    animal.notes = notes
    animal.vet_id = vet_id
    db.session.commit()
    return redirect ('/animals') 
##############################
# WANT TO RETURN TO ('/animals/<id>') but it won't let me, it's not happy about the input type of <id>
##############################

@animals_blueprint.route('/animals/new')
def new():
    vets = Vet.query.all()
    return render_template('animals/new.jinja', vets=vets)

@animals_blueprint.route('/animals/new', methods=["POST"])
def add_new():
    name = request.form["name"]
    species = request.form["species"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    new_animal = Animal(name=name, species=species, dob=dob, phone=phone, notes=notes, vet_id = vet_id)
    db.session.add(new_animal)
    db.session.commit()
    return redirect ('/animals')
