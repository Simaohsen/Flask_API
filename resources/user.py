import sqlite3
from flask_restful import Resource, reqparse
from flask import request
from models.user import UserModel



class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required= True, help="This field is needed!")
    parser.add_argument('password', type=str, required= True, help="This field is needed!")


    def post(self):


        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that name already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': "User created succesfully"}, 201

    # def get(self, name):
    #     with sqlite3.connect('data.db') as conn:
    #         cursor = conn.cursor()
    #
    #         query = "SELECT * FROM users WHERE username=?"
    #         data = cursor.execute(query, name)
    #         if data:
    #             return data, 200
    #
    #         else:
    #             return 404
