#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):

    def get(self):

        campers_dict_list = [n.to_dict(only = ("id", "name", "age")) for n in Camper.query.all()]

        response = make_response(
            campers_dict_list,
            200,
        )

        return response
    
    def post(self):

        json_data = request.get_json()
        name = json_data.get("name")
        age = json_data.get("age")

        try:

            new_camper = Camper(
                name = name,
                age = age
            )

            db.session.add(new_camper)
            db.session.commit()

            response = make_response(
                new_camper.to_dict(),
                201
            )

            return response

        except:

            response = make_response(
                {
                    "errors": ["validation errors"]
                    },
                400
            )

            return response

class CampersByID(Resource):

    def get(self, id):
                         
        camper = Camper.query.filter_by(id = id).first()

        try:

            camper_dict = camper.to_dict(only = ("id", "name", "age", "signups"))

            response = make_response(
                camper_dict,
                200,
            )

            return response
        
        except:

            return {
                "error": "Camper not found"
                }, 404


    def patch(self, id):

        camper = Camper.query.filter_by(id = id).first()

        if camper:

            try: 

                json_data = request.get_json()
                name = json_data.get("name")
                age = json_data.get("age")

                camper_obj = {
                    "name": name,
                    "age": age
                }

                camper.name = name
                camper.age = age

                db.session.commit()

                response = make_response(
                    camper_obj,
                    202
                )

                return response
            
            except:

                response = make_response(
                    {
                        "errors": ["validation errors"]
                        },
                    400
                )

                return response
            
        else:

                response = make_response(
                    {
                        "error": "Camper not found"
                        },
                    404
                )

                return response
        
class Activities(Resource):

    def get(self):

        activities_dict_list = [n.to_dict(only = ("id", "name", "difficulty")) for n in Activity.query.all()]

        response = make_response(
            activities_dict_list,
            200,
        )

        return response
    
class ActivitiesByID(Resource):

    def delete(self, id):

        activity = Activity.query.filter_by(id = id).first()

        if activity:

            db.session.delete(activity)

            response = make_response(
                {},
                204,
            )

            return response
        
        else:

            response = make_response(
                {
                    "error": "Activity not found"
                    },
                    404
            )

            return response
        

class Signups(Resource):

    def post(self):

        json_data = request.get_json()
        camper_id = json_data.get("camper_id")
        activity_id = json_data.get("activity_id")
        time = json_data.get("time")

        try:
            
            new_signup = Signup(
                camper_id = camper_id,
                activity_id = activity_id,
                time = time
            )

            db.session.add(new_signup)
            db.session.commit()

            response = make_response(
                new_signup.to_dict(),
                201
            )

            return response

        except:

            response = make_response(
                {
                    "errors": ["validation errors"]
                    },
                400
            )

            return response


api.add_resource(Campers, '/campers')
api.add_resource(CampersByID, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(ActivitiesByID, '/activities/<int:id>')
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
