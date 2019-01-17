from flask import jsonify

class BaseModel:

    def find(self):
        """ finds an item in the database """
        pass
    
    def delete(self):
        """ deletes an item from the database """
        pass

    def get_all(self):
        """ gets all items in the datbase """
        pass

    def get_one(self):
        """ gets an item from the database """
        pass