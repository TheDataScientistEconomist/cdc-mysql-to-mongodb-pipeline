import pymongo
from pymongo import MongoClient


# make a connection
client = MongoClient("mongodb://localhost:27017")

# get database
db = client.pluto

# get collection
posts = db.posts


# write to posts collection
def write(stamps):
    for stamp in stamps:
        item = {
            "stamp": stamp
        }

        posts.update_one(
            {"stamp": stamp},
            {"$set": item},
            upsert=True
        )


# read posts collection
def read():
    stamps = []

    # get last 5 entries
    for post in posts.find().sort("stamp", pymongo.DESCENDING).limit(5):
        stamps.append(post["stamp"])

    return stamps


# delete posts collection data
def delete():
    posts.delete_many({})