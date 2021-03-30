from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc

from models import Cars, CarsSchema, Dealers, DealersSchema, db

car_schema = CarsSchema()
dealer_schema = DealersSchema()


class DealerManager(Resource):
    @staticmethod
    def get():
        response = request.get_json(force=True, silent=False)
        dealer_id = response["dealer_id"]
        dealer = Dealers.query.get(dealer_id)
        if dealer:
            return dealer_schema.dump(dealer)
        else:
            return {"message": "No dealer found"}, 404

    @staticmethod
    def post():
        response = request.get_json(force=True)
        try:
            data = dealer_schema.load(response)
        except ValidationError as err:
            return {"Error": f"{err}"}, 400
        dealer = Dealers(**data)
        try:
            db.session.add(dealer)
            db.session.commit()
        except exc.IntegrityError:
            return {"Error": "Database specific error occured. The dealer is already presented in system"}, 409
        else:
            result = dealer_schema.dump(Dealers.query.get(dealer.dealer_id))
            return {"message": "Created new dealer.", "dealer": result}, 200

    @staticmethod
    def put():
        response = request.get_json(force=True)
        dealer_id = response['dealer_id']
        response.pop("dealer_id")
        try:
            dealer_schema.load(response)
        except ValidationError as err:
            return {"Error": f"{err}"}, 400
        dealer = Dealers.query.get(dealer_id)
        if dealer:
            dealer.name = response['name']
            dealer.ogrn = response['ogrn']
            dealer.address = response['address']
            dealer.segment = response['segment']
            dealer.telephone = response['telephone']
            dealer.url = response['url']
            dealer.loans = bool(response['loans'])
            dealer.loan_broker = response['loan_broker']
            dealer.used_cars = bool(response['used_cars'])

            try:
                dealer.save_to_db()
            except exc.IntegrityError:
                return {"Error": f"Database specific error occured. The dealer with ogrn {response['ogrn']} is already"
                                 f"presented in system"}, 400
            else:
                result = dealer_schema.dump(Dealers.query.get(dealer.dealer_id))
                return {"message": "Edited new dealer.", "dealer": result}
        else:
            return {"message": f"Error occured. This dealer {response['ogrn']} doesn't exist"}, 404

    @staticmethod
    def delete():
        response = request.get_json(force=True)
        dealer_id = response["dealer_id"]
        dealer = Dealers.query.get(dealer_id)
        if dealer:
            dealer.delete_from_db()
            return {"message": "Deleted dealer.", "dealer": dealer_schema.dump(dealer)}
        else:
            return {"message": f"Error occured. This dealer {response['dealer_id']} doesn't exist"}, 404


class CarManager(Resource):
    @staticmethod
    def get():
        response = request.get_json(force=True, silent=False)
        car_id = response["car_id"]
        car = Cars.query.get(car_id)
        if car:
            return car_schema.dump(car), 200
        else:
            return {"message": "No car found"}, 404

    @staticmethod
    def post():
        response = request.get_json(force=True)
        try:
            data = car_schema.load(response)
        except ValidationError as err:
            return {"Error": f"{err}"}, 400
        car = Cars(**data)
        try:
            db.session.add(car)
            db.session.commit()
        except exc.IntegrityError as err:
            return {"Error": "Database specific error occured. The car is already presented in system"}, 409
        else:
            result = car_schema.dump(Cars.query.get(car.car_id))
            return {"message": "Created new car.", "car": result}, 200

    @staticmethod
    def put():
        response = request.get_json(force=True)
        car_id = response['car_id']
        response.pop("car_id")
        try:
            car_schema.load(response)
        except ValidationError as err:
            return {"Error": f"{err}"}, 400
        car = Cars.query.get(car_id)
        if car:
            existing_dealers = db.session.query(Dealers.dealer_id).all()
            car.vin = response["vin"]
            car.price = response["price"]
            car.power = response["power"]
            car.model = response["model"]
            car.manufacturer = response["manufacturer"]
            car.mileage = response["mileage"]
            car.gearbox = response['gearbox']
            car.volume = response['volume']
            if int(response['dealer_id']) in [dealer[0] for dealer in existing_dealers]:
                car.dealer_id = response['dealer_id']
            else:
                return {"Error": f"No such dealer with id = {response['dealer_id']}"}
            try:
                car.save_to_db()
            except exc.IntegrityError:
                return {
                           "Error": f"Database specific error occured. The car {response['vin']} is already presented in system"}, 400
            else:
                result = car_schema.dump(Cars.query.get(car.car_id))
                return {"message": "Edited new car.", "car": result}
        else:
            return {"message": f"Error occured. This car {response['vin']} doesn't exist"}, 404

    @staticmethod
    def delete():
        response = request.get_json(force=True)
        car_id = response["car_id"]
        car = Cars.query.get(car_id)
        if car:
            car.delete_from_db()
            return {"message": "Deleted car.", "car": car_schema.dump(car)}
        else:
            return {"message": f"Error occured. This car {response['car_id']} doesn't exist"}, 404
