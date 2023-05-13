#!/usr/bin/env python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """
    lists all documents in a collection

    :param mongo_collection: PyMongo collection object reps the collection
    :return: A cursor containing the result of the find operation
    """
    return mongo_collection.find()
