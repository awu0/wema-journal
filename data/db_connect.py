import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

WEMA_DB = 'wemaDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://gcallah:{password}'
                                    + '@koukoumongo1.yud9b.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
    return client


def create(collection, doc, db=WEMA_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=WEMA_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


def del_one(collection, filt, db=WEMA_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def update_doc(collection, filters, update_dict, db=WEMA_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


def read(collection, db=WEMA_DB, no_id=True) -> list:
    """
    This will return a list from the db.
    """
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret

def fetch_all_as_dict(key, collection, db=WEMA_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def count_documents(collection, filt={}, db=WEMA_DB):
    """
    Count the number of documents in a collection that match the filter.
    Returns an integer count.
    """
    return client[db][collection].count_documents(filt)


def delete_many(collection, filt, db=WEMA_DB):
    """
    Delete multiple documents in the collection that match the filter.
    Returns the count of deleted documents.
    """
    result = client[db][collection].delete_many(filt)
    return result.deleted_count
