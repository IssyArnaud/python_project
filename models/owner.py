from app import db

class Owner(db.Model):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    def __repr__(self):
        return f"<Owner {self.id}: {self.name}>"