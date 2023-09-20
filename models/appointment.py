from app import db

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'))
    notes = db.Column(db.Text())
    def __repr__(self):
        return f"<Appointment: {self.id}: {self.animal_id}, {self.treatment_id}>"