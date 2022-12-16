import pymongo
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

db_client = pymongo.MongoClient(MONGO_DETAILS)

database = db_client.collect
forms_collection = database.get_collection("forms")
form_owner = forms_collection.find_one(
    {"_id": ObjectId("6373ab40ef5e96e803bbb8d4")}, {"form_owner": 1, "_id": 0}
)
print(form_owner)
