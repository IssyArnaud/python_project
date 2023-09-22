from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.vet import Vet
from models.owner import Owner
from models.appointment import Appointment
from models.animal import Animal
from models.treatment import Treatment
from app import db

appointments_blueprint = Blueprint("appointments", __name__)

@appointments_blueprint.route('/appointments')
def show_all():
    appointments = Appointment.query.all()
    return render_template('appointments/all.jinja', appointments=appointments)

@appointments_blueprint.route('/appointments/<id>')
def show(id):
    appointment = Appointment.query.get(id)
    animal = Animal.query.get(appointment.animal_id)
    vet = Vet.query.get(animal.vet_id)
    owner = Owner.query.get(animal.owner_id)
    treatment = Treatment.query.get(appointment.treatment_id)
    return render_template('/appointments/details.jinja', appointment=appointment, animal=animal, vet=vet, 
    owner=owner, treatment=treatment)

@appointments_blueprint.route('/appointments/<id>', methods=["POST"])
def delete(id):
    appointment = Appointment.query.get(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect ('/appointments')

@appointments_blueprint.route('/appointments/<id>/edit')
def edit(id):
    appointment = Appointment.query.get(id)
    animals = Animal.query.all()
    treatments = Treatment.query.all()
    return render_template('appointments/edit.jinja', appointment=appointment, animals=animals,
    treatments=treatments)

@appointments_blueprint.route('/appointments/<id>/edit', methods=["POST"])
def update(id):
    appointment = Appointment.query.get(id)
    animal_id = request.form["animal_id"]
    treatment_id = request.form["treatment_id"]
    notes = request.form["notes"]
    appointment.animal_id = animal_id
    appointment.treatment_id = treatment_id
    appointment.notes = notes
    db.session.commit()
    return redirect (f"/appointments/{id}")

@appointments_blueprint.route('/appointments/new')
def new():
    animals = Animal.query.all()
    treatments = Treatment.query.all()
    return render_template('appointments/new.jinja', animals=animals, treatments=treatments)

@appointments_blueprint.route('/appointments/new', methods=["POST"]) #It would follow the restful routing convention better to have this route named '/appointments' 
#we don't need to have '/new' as the fact it's a post request implies we are creating a new appointment.  
def add():
    animal_id = request.form["animal_id"]
    treatment_id = request.form["treatment_id"]
    notes = request.form["notes"]
    new_appointment = Appointment(animal_id = animal_id, treatment_id=treatment_id, notes=notes)
    db.session.add(new_appointment)
    db.session.commit()
    return redirect ('/appointments')