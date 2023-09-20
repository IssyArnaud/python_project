from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.animal import Animal
from models.vet import Vet
from models.owner import Owner
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
    owner = Owner.query.get(animal.owner_id)
    return render_template('animals/details.jinja', animal=animal, vet=vet, owner=owner)

@animals_blueprint.route('/animals/<id>', methods=["POST"])
def delete(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    return redirect ('/animals')

@animals_blueprint.route('/animals/<id>/edit')
def edit(id):
    animal = Animal.query.get(id)
    owner = Owner.query.get(animal.owner_id)
    vet = Vet.query.get(animal.vet_id)
    vets = Vet.query.all()
    owners = Owner.query.all()
    return render_template('animals/edit.jinja', animal=animal, vets=vets, owners=owners, owner=owner, vet=vet)

@animals_blueprint.route('/animals/<id>/edit', methods=["POST"])
def update(id):
    animal = Animal.query.get(id)
    name = request.form["name"]
    species = request.form["species"]
    dob = request.form["dob"]
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    animal.name = name
    animal.species = species
    animal.dob = dob
    animal.notes = notes
    animal.vet_id = vet_id
    if animal.owner_id:
        owner_id = request.form["owner.id"]
        animal.owner_id = owner_id
        db.session.commit()
    else:
        phone = request.form["phone"]
        animal.phone = phone
        db.session.commit()
    return redirect (f'/animals/{id}')

@animals_blueprint.route('/animals/new')
def new():
    vets = Vet.query.all()
    owners = Owner.query.all()
    return render_template('animals/new.jinja', vets=vets, owners=owners)

@animals_blueprint.route('/animals/new', methods=["POST"])
def add_new():
    name = request.form["name"]
    species = request.form["species"]
    dob = request.form["dob"]
    owner_id = request.form["owner.id"]
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    new_animal = Animal(name=name, species=species, dob=dob, notes=notes, vet_id=vet_id, owner_id=owner_id)
    db.session.add(new_animal)
    db.session.commit()
    return redirect ('/animals')

@animals_blueprint.route('/animals/new/unregistered')
def unregistered():
    vets = Vet.query.all()
    return render_template('animals/unregistered.jinja', vets=vets)

@animals_blueprint.route('/animals/denied/<id>')
def denied(id):
    animal = Animal.query.get(id)
    vet = Vet.query.get(animal.vet_id)
    return render_template('animals/denied.jinja', animal=animal, vet=vet)

@animals_blueprint.route('/animals/new/unregistered', methods={"POST"})
def add_unregistered():
    name = request.form["name"]
    species = request.form["species"]
    dob = request.form["dob"]
    phone = request.form["phone"]
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    animals = Animal.query.all()
    for animal in animals:
        if phone == animal.phone:
            id = animal.id
            return redirect(f'/animals/denied/{id}')
    else:
        new_animal = Animal(name=name, species=species, dob=dob, notes=notes, vet_id=vet_id, phone=phone)
        db.session.add(new_animal)
        db.session.commit()
        return redirect ('/animals')