from app import db

class Treatment(db.Model):
    __tablename__ = "treatments"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    price = db.Column(db.Integer)
    in_patient = db.Column(db.Boolean)
    appointments = db.relationship('Appointment', backref='treatment')

    def __repr__(self):
        return f"<Treatment {self.id}: {self.title}>"