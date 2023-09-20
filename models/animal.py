from app import db

class Animal(db.Model):
    __tablename__ = "animals"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    species = db.Column(db.String(64))
    dob = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    phone = db.Column(db.String(64))
    notes = db.Column(db.Text())
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.id'))
    
    def __repr__(self):
        return f"<Animal {self.id}: {self.name}, {self.species}>"