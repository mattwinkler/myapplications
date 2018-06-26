

from pymongo import MongoClient


def create_connection(db_name, host='localhost', port=27017, username=None, password=None):
    # Make Mongo connection with/out authentication
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s/%s'%\
        (username, password, host, db_name)

        conn = MongoClient(mongo_uri)
        
    else:
        conn = MongoClient(host, port)

    return conn[db_name]


def insert_records(db, collection, records):
    coll = db[collection]
    try:
        coll.insert(records)

    except Exception as err:
        return err

    return None


def drop_collection(db, collection):
    try:
        db.drop_collection(collection)

    except Exception as err:
        return err

    return None


def fetch(db, collection, query={}):
    try:
        coll = db[collection]
        results = coll.find(query)
        results = list(results)
    except Exception as err:
        return err

    return results


def fetch_to_dict(db, collection, query={}, del_id=True, **kw):
    try: 
        coll = db[collection]
        results = coll.find(query)
        results = list(results)
        if del_id:
            for r in results:
                r.pop('_id')

    except Exception as err:
        return err
    
    return results
