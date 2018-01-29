import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item need a store id."
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Items not found"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' alread exists.".format(name)}, 400
        request_data = Item.parser.parse_args()

        item = ItemModel(name, request_data['price'], request_data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500

        return {'message': "Item with name'{}' created.".format(name)}, 201




    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Item not found"}


    def put(self, name):

        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
            item = ItemModel(name, request_data['price'], request_data['item_id'])
        else:
            item.price = request_data['price']

        item.save_to_db()
        return updated_item.json()



class ItemList(Resource):
    def get(self):

        return {'items': [item.json() for item in ItemModel.query.all()]}
