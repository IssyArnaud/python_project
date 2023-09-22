from models.animal import Animal
from datetime import datetime

def handle_create_animal(form_dict):
    name = form_dict["name"]
    species = form_dict["species"]
    string_dob = form_dict["dob"]
    dob = datetime.strptime(string_dob, '%Y-%m-%d').date()
    phone = form_dict["phone"]
    notes = form_dict["notes"]
    vet_id = form_dict["vet.id"]

    return Animal(name=name, species=species, dob=dob, notes=notes, vet_id=vet_id, phone=phone)

def get_animal_id(phone_number):
    animals = Animal.query.all()
    for animal in animals:
        if phone_number == animal.phone:
            return animal.id
    return None
