from app import db, Date

# probably shouldn't have both our animals table and our owner both having a column for 'Phone'. We normally want to have a 'single source of truth' in our data structures, as currently having the phone number associated with an animal in two places allows them to become desynchronised which can cause problems in the future.  

# I see we can have a flow for adding a new 'unregistered' animal, I take it the owner is 'unregistered', we would still need to take contact details off someone even if they where not registered? It would probably be better to represent this with a boolean column in our 'owners' tables. 

class Animal(db.Model):
    __tablename__ = "animals"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    species = db.Column(db.String(64))
    dob = db.Column(Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    phone = db.Column(db.String(64))
    notes = db.Column(db.Text())
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'))
    appointments = db.relationship('Appointment', backref='animal')
    
    def __repr__(self):
        return f"<Animal {self.id}: {self.name}, {self.species}>"