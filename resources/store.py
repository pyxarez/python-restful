from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return {'message': 'Store already exists'}

        new_store = StoreModel(name)

        try:
            new_store.save_to_db()
        except:
            return {'message': 'Error occurred while creating the store'}, 500

        return new_store.json(), 201

    @jwt_required()
    def delete(self, name):
        StoreModel(name).delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}
