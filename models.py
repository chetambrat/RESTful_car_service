from marshmallow import fields, validate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from create_app import db, ma


class Dealers(db.Model):
    __tablename__ = "dealers"
    dealer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=40), nullable=False)
    ogrn = db.Column(db.String(18), unique=True, nullable=False)
    address = db.Column(db.String(50))
    segment = db.Column(db.String(10))
    telephone = db.Column(db.String(12))
    url = db.Column(db.String(32))
    loans = db.Column(db.Boolean)
    loan_broker = db.Column(db.String(40))
    used_cars = db.Column(db.Boolean)
    relationship("Cars")

    def __init__(self, name, ogrn, address, segment,
                 telephone, url, loans, loan_broker, used_cars):
        self.name = name
        self.ogrn = ogrn
        self.address = address
        self.segment = segment
        self.telephone = telephone
        self.url = url
        self.loans = loans
        self.loan_broker = loan_broker
        self.used_cars = used_cars

    def __repr__(self):
        return f"{self.name}"

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class Cars(db.Model):
    __tablename__ = "cars"
    car_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(length=16), nullable=False)
    mileage = db.Column(db.Integer)
    manufacturer = db.Column(db.String(30), nullable=False)
    vin = db.Column(db.String(20), unique=True, nullable=False)
    gearbox = db.Column(db.String(10))
    price = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Integer)
    volume = db.Column(db.Float(4))
    dealer_id = db.Column(db.Integer, ForeignKey("dealers.dealer_id"), nullable=False)
    relationship("Dealers", foreign_keys=[dealer_id])

    def __init__(self, model, mileage, manufacturer, vin, gearbox,
                 price, power, volume, dealer_id):
        self.model = model
        self.mileage = mileage
        self.manufacturer = manufacturer
        self.vin = vin
        self.gearbox = gearbox
        self.price = price
        self.power = power
        self.volume = volume
        self.dealer_id = dealer_id

    def __repr__(self):
        return f"{self.vin}"

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class DealersSchema(ma.SQLAlchemySchema):
    name = fields.Str(required=True, validate=[validate.Length(min=3, max=40)])
    ogrn = fields.Str(required=True, validate=[validate.Length(max=18)])
    address = fields.Str(required=False, validate=[validate.Length(min=10, max=50)])
    segment = fields.Str(required=False, validate=[validate.OneOf(["cheap", "middle", "premium"],
                                                                  error="invalid segment")])
    telephone = fields.Str(required=False, validate=[validate.Regexp(r"\+79[0-9]{9}", error="invalid phone")])
    url = fields.Str(required=False, validate=[validate.URL(relative=False, require_tld=False, error="invalid URL")])
    loans = fields.Boolean()
    loan_broker = fields.Str(required=False, validate=[validate.Length(max=250)])
    used_cars = fields.Boolean()

    class Meta:
        model = Dealers
        include_fk = True
        sqla_session = db.session


class CarsSchema(ma.SQLAlchemySchema):
    model = fields.Str(required=True, validate=[validate.Length(min=3, max=16)])
    mileage = fields.Integer(validate=[validate.Range(1, 9999999)])
    manufacturer = fields.Str(required=False, validate=[validate.Length(min=3, max=30)])
    vin = fields.Str(required=True, validate=[validate.Length(min=10, max=20)])
    gearbox = fields.Str(required=False, validate=[validate.OneOf(["auto", "manual", "other"])])
    price = fields.Integer(required=False, validate=[validate.Range(10000, 999999999)])
    power = fields.Float(validate=[validate.Range(40, 100000)])
    volume = fields.Float(validate=[validate.Range(0.5, 100)])
    dealer_id = fields.Integer(required=True)

    class Meta:
        model = Cars
        include_fk = True
        sqla_session = db.session
