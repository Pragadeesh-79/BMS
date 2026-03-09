import os
from db import db

def give_1000_to_all():
    users_collection = db['users']
    result = users_collection.update_many(
        {'balance': {'$lt': 1000}}, 
        {'$set': {'balance': 1000.0}}
    )
    print(f"Updated {result.modified_count} users to have $1000.")

if __name__ == '__main__':
    give_1000_to_all()
