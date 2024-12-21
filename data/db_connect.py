import os
from urllib.parse import quote_plus

import pymongo as pm
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()

LOCAL = "0"
CLOUD = "1"

client = None

MONGO_ID = '_id'

WEMA_DB = 'wemaDB'


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
            username = os.getenv("DB_USERNAME", "")
            password = os.getenv("DB_PASSWORD", "")
            cluster = os.getenv("DB_CLUSTER", "")
            options = os.getenv("DB_OPTIONS", "")

            if not username or not password or not cluster:
                raise ValueError(
                    "Missing required database credentials: "
                    "'DB_USERNAME', 'DB_PASSWORD', or 'DB_CLUSTER'."
                )

            # We needed to escape username and password since it didn't work for me without it
            escaped_username = quote_plus(username)
            escaped_password = quote_plus(password)

            # Build the MongoDB URI
            mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster}"
            if options:
                mongo_uri += f"/{options}"

            print(f"Connecting to MongoDB with URI: {mongo_uri}")
            client = pm.MongoClient(mongo_uri)
        else:
            print("Connecting to MongoDB locally...")
            local_port = os.environ.get("LOCAL_DB_PORT", "27017")
            client = pm.MongoClient(f"mongodb://localhost:{local_port}")

        try:
            client.admin.command('ping')
            print("MongoDB connection successful.")
        except ConnectionFailure:
            print("Failed connecting to MongoDB.")
            client = None

    return client


def create(collection, doc, db=WEMA_DB):
    """
    Insert a single doc into collection.
    """
    print(f'Inserted {doc} into {collection} for DB: {db}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=WEMA_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    doc = client[db][collection].find_one(filt)
    print(f"Fetched document: {doc}")  # Debug
    
    if doc and MONGO_ID in doc:
        print(f"Converting {MONGO_ID}: {doc[MONGO_ID]}, type: {type(doc[MONGO_ID])}")  # Debug
        doc[MONGO_ID] = str(doc[MONGO_ID])
        print(f"After conversion: {doc}")  # Debug
    return doc


def delete(collection: str, filt: dict, db=WEMA_DB):
    """
    Find with a filter and return on the first doc found.
    """
    print(f'{filt=}')
    result = client[db][collection].delete_one(filt)
    return result.deleted_count


def update_doc(collection, filters, update_dict, db=WEMA_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


def read(collection, db=WEMA_DB, no_id=True) -> list:
    """
    This will return a list from the db.
    """
    ret = []
    for doc in client[db][collection].find():
        if no_id:
            del doc[MONGO_ID]
        else:
            doc[MONGO_ID] = str(doc[MONGO_ID])
        ret.append(doc)
    return ret


def read_dict(collection, key, db=WEMA_DB, no_id=True) -> dict:
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict = {}
    for rec in recs:
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


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


if __name__ == '__main__':
    connect_db()
