#!/usr/bin/env python
import re
from pymongo import MongoClient

key = "field"
value = "tags"

field_list = ["Software", "Hardware", "Internet", "Technical_Other", "Medical"]
Technical_Set = {"Software", "Hardware", "Internet", "Technical_Other"}

def connect_database():
    client = MongoClient()
    db = client.category_db
    coll = db.docs
    return coll

def get_field_by_term(term, coll):
    term = term.lower()
    for doc in coll.find({value: term}):
        return doc[key]
    return None

def get_fields_by_term(term, coll):
    term = term.lower()
    fields = []
    for doc in coll.find({value: {'$regex': term}}):
        fields.append(doc[key])
    return fields

def get_field_by_tf(tf_dict):
    coll = connect_database()
    score = {}
    for field in field_list:
        score[field] = 0.0
    for tf in tf_dict.items():
        #print tf[0] + "-------"
        field = get_field_by_term(tf[0], coll)
        if field == None:
            fields = get_fields_by_term(tf[0], coll)
            for field in fields:
                score[field] += (0.707 / len(fields)) * tf[1]
        else:
            score[field] += 1.0 * tf[1]
        #print score
    return max(score, key = score.get)

def get_field_by_query(query):
    coll = connect_database()
    score = {}
    for field in field_list:
        score[field] = 0.0
    for term in query.split():
        field = get_field_by_term(term, coll)
        if field == None:
            fields = get_fields_by_term(term, coll)
            for field in fields:
                score[field] += 0.707 / len(fields)
        else:
            score[field] += 1.0
    return max(score, key = score.get)

def get_relavance(f1, f2):
    if f1 == f2:
        return 1.0
    elif (f1 in Technical_Set) and (f2 in Technical_Set):
        return 0.5
    else:
        return 0.0

if __name__ == '__main__':
    tf_dict = {"Software": 1.2, "Hardware": 0.6, "Back": 1.0, "Bitmap": 50.0}
    print get_field_by_tf(tf_dict)
    print get_field_by_query("Internet overflow")



