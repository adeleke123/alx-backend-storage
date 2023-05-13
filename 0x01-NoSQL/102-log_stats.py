#!/usr/bin/env python3
"""Log stats - new version"""

from pymongo import MongoClient


def log_stats():
    """Retrieve and print statistics from the 'nginx' logs collection."""
    # Connect to the MongoDB instance
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Access the 'nginx' logs collection
    logs_collection = client.logs.nginx

    # Retrieve the total number of logs
    total = logs_collection.count_documents({})

    # Retrieve the count for each HTTP method
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})

    # Retrieve the count for a specific method and path
    path = logs_collection.count_documents({"method": "GET", "path": "/status"})

    # Retrieve the top 10 most present IPs
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print the retrieved statistics
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")
    for ip_data in top_ips:
        print(f"\t{ip_data['_id']}: {ip_data['count']}")


if __name__ == "__main__":
    log_stats()
