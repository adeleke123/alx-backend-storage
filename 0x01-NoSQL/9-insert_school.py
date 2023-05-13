#!/usr/bin/env python3
"""Insert a document in Python"""


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document in a collection based on kwargs

    :param mongo_collection: PyMongo collection object representing
    the collection
    :param kwargs: keyword arguments representing the fields & values
    of the new document
    :return: _id of the newly inserted document
    """
    new_docs = mongo_collection.insert_one(kwargs)
    return new_docs.inserted_id
