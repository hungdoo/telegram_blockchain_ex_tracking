from pymongo import MongoClient
from bson.objectid import ObjectId

db_doc = MongoClient('mongodb://localhost:27017/').btcdb.info

def get_document(query_dict):
    return db_doc.find_one(query_dict)

def create_document(new_dict):
    db_doc.insert_one(new_dict)

def update_document(query_dict, update_data):
    return db_doc.update_one(query_dict, {"$set":update_data}).modified_count != 0

def main():
    # Testing
    query = {"title":"None"}
    new_data = {"title":"testtest"}
    print(f"DEBUG get_document: {get_document(query)}")
    create_document(query)
    print(f"DEBUG get_document: {get_document(query)}")
    print(f"DEBUG update_document: {update_document(query, new_data)}")
    print(f"DEBUG get_document: {get_document(query)}")
    print(f"DEBUG get_document: {get_document(new_data)}")
    print(f"DEBUG update_document: {update_document(query, new_data)}")


if __name__ == "__main__":
    main()