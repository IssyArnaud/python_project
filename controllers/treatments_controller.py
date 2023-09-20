from flask import Flask, render_template, request, redirect
from flask import Blueprint

from app import db
from models.treatment import Treatment
from models.appointment import Appointment

treatments_blueprint = Blueprint("treatments", __name__)

@treatments_blueprint.route('/treatments')
def show_all():
    treatments = Treatment.query.all()
    return render_template('treatments/all.jinja', treatments=treatments)

@treatments_blueprint.route('/treatments/<id>')
def show(id):
    treatment = Treatment.query.get(id)
    return render_template('/treatments/details.jinja', treatment=treatment)

@treatments_blueprint.route('/treatments/<id>', methods=["POST"])
def delete(id):
    treatment = Treatment.query.get(id)
    appointments = Appointment.query.filter_by(treatment_id = id)
    for appointment in appointments:
        db.session.delete(appointment)
    db.session.delete(treatment)
    db.session.commit()
    return redirect ('/treatments')

@treatments_blueprint.route('/treatments/<id>/edit')
def edit(id):
    treatment = Treatment.query.get(id)
    return render_template('treatments/edit.jinja', treatment=treatment)

@treatments_blueprint.route('/treatments/<id>/edit', methods=["POST"])
def update(id):
    treatment = Treatment.query.get(id)
    title = request.form["title"]
    price = request.form["price"]
    in_patient = "in_patient" in request.form
    treatment.title = title
    treatment.price = price
    treatment.in_patient = in_patient
    db.session.commit()
    return redirect (f"/treatments/{id}") 

@treatments_blueprint.route('/treatments/new')
def new():
    return render_template('treatments/new.jinja')

@treatments_blueprint.route('/treatments/new', methods=["POST"])
def add():
    title = request.form["title"]
    price = request.form["price"]
    in_patient = "in_patient" in request.form
    new_treatment = Treatment(title=title, price=price, in_patient=in_patient)
    db.session.add(new_treatment)
    db.session.commit()
    return redirect ('/treatments')