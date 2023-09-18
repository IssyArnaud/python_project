from app import db

class Vet(db.Model):
    __tablename__ = "vets"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    def __repr__(self):
        return f"<Vet {self.id}: {self.name}>"
    
    # def caseload(self):
    #     cases = []
    #     for animal in animals:
    #         if animal.vet_id == vet.id:
    #             cases.append(animal)
    #     return cases