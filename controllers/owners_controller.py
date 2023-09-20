from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.vet import Vet
from models.animal import Animal
from models.owner import Owner
from app import db

owners_blueprint = Blueprint("owners", __name__)

@owners_blueprint.route('/owners')
def show_all():
    owners = Owner.query.all()
    return render_template('owners/all.jinja', owners=owners)

@owners_blueprint.route('/owners/<id>')
def show(id):
    owner = Owner.query.get(id)
    pets = Animal.query.filter_by(owner_id = id)
    return render_template('/owners/details.jinja', owner=owner, pets=pets)

@owners_blueprint.route('/owners/<id>/edit')
def edit(id):
    owner = Owner.query.get(id)
    return render_template('owners/edit.jinja', owner=owner)

@owners_blueprint.route('/owners/<id>/edit', methods=["POST"])
def update(id):
    owner = Owner.query.get(id)
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    owner.name = name
    owner.phone = phone
    owner.email = email
    db.session.commit()
    return redirect (f"/owners/{id}")

@owners_blueprint.route('/owners/new')
def new():
    return render_template('owners/new.jinja')

@owners_blueprint.route('/owners/new', methods=["POST"])
def add():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    new_owner = Owner(name=name, phone=phone, email=email)
    db.session.add(new_owner)
    db.session.commit()
    return redirect ('/owners')

@owners_blueprint.route('/owners/<id>', methods=["POST"])
def delete(id):
    owner = Owner.query.get(id)
    pets = Animal.query.filter_by(owner_id = id)
    for animal in pets:
        db.session.delete(animal)
    db.session.delete(owner)
    db.session.commit()
    return redirect ('/animals')