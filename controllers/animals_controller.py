from flask import Flask, render_template, request, redirect
from flask import Blueprint
from datetime import datetime

from services.animals_services import handle_create_animal, get_animal_id
from models.animal import Animal
from models.vet import Vet
from models.owner import Owner
from models.appointment import Appointment
from app import db

# we can consider extracting out logic and extra verbosity from our controller functions into a separate file, we care more about _what_ are code is doing as opposed to _how_ its doing it. 
# see below for example
# this has the following benefits ..

# 1. Separation of concerns
# One of the core principles of software engineering is the separation of concerns. By moving business logic out of controllers and into separate components, you ensure that each component has a single responsibility. Controllers should primarily handle user input and orchestrate the flow of data, while logic related to data manipulation, validation, and business rules should be handled by other parts of the application.
# 2. Code Reusability (keeps us DRY)
# Extracting logic into separate modules or classes makes it more reusable. You can use the same logic in multiple controllers or even in different parts of your application. This reduces code duplication and leads to a more maintainable codebase.
# 3. Scalable 
# As your application grows, you may need to change or extend its functionality, if we have to do the same action several times, it helps if we have the logic to do that action central to one place if we suddenly need to change how we are doing that action we now need to just change the code in one place as apposed to every place we where doing that action.
# 4. Readability 
# Controllers are typically responsible for managing the flow of requests and responses. When logic is mixed with controller code, it can make controllers bulky and less readable. Extracting logic into separate files/folders leads to cleaner, more focused, and more readable code. This improves the overall maintainability of the application. 



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
    appointments = Appointment.query.filter_by(animal_id = id)
    for appointment in appointments:
        db.session.delete(appointment)
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
    string_dob = request.form["dob"]
    dob = datetime.strptime(string_dob, '%Y-%m-%d').date()
    notes = request.form["notes"]
    vet_id = request.form["vet.id"]
    animal.name = name
    animal.species = species
    animal.dob = dob
    animal.notes = notes
    animal.vet_id = vet_id
    if request.form["owner.id"]:
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
    string_dob = request.form["dob"]
    dob = datetime.strptime(string_dob, '%Y-%m-%d').date()
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

@animals_blueprint.route('/animals/new/unregistered', methods={"POST"}) # is this {"POST"} the right syntax? does this work? 
def add_unregistered():
    name = request.form["name"]
    species = request.form["species"]
    string_dob = request.form["dob"]
    dob = datetime.strptime(string_dob, '%Y-%m-%d').date()
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
    

##########################
# example of extracting logic 
##########################

# @animals_blueprint.route('/animals/new/unregistered', methods={"POST"})
# def add_unregistered():
    
#     id = get_animal_id(request.form["phone"]) 
#     if id != None:
#             return redirect(f'/animals/denied/{id}')
#     else:
#         new_animal = handle_create_animal(request.form)
#         db.session.add(new_animal)
#         db.session.commit()
#         return redirect ('/animals')

#Code reads _like_ english now, making it easier to process.