# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import os
from pathlib import Path
from dotenv import load_dotenv
import translation
import random

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def connect_db(Domain, PORT):
    '''
    Connect database
    '''
    try:
        conn = pymongo.MongoClient(Domain, PORT)

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to server: %s" % e)
    return conn


def connect_db_url(url):
    '''
    Connect database URL
    '''
    try:
        conn = pymongo.MongoClient(url)

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to server: %s" % e)
    return conn


def insert_db(message: dict):
    '''
    INSERT QUERY
    '''
    conn = connect_db(os.environ['host'], int(os.environ['port']))
    if conn is not None and message is not None:
        mydb = conn[os.environ['Database_db']]
        mycol = mydb[os.environ['Database_Col']]
        x = mycol.insert_one(message)
        print("Inserting in database : ", message)
        return (x.acknowledged)
    else:
        raise ValueError("Parameters error")


def insert_message(comment: dict):
    if comment is None:
        raise ValueError("Empty Parameter")
    else:
        txt = comment.get("event")
        if (txt.get("thread_ts")) is not None:
            target = int(float(txt.get("thread_ts")))
        else:
            target = None
        qr = {
            "id": "Comment-" + str(random.randint(0, 1200)),
            "textFr": translation.translate(txt.get("text"), "fr"),
            "textEn": translation.translate(txt.get("text"), "en"),
            "publishedAt": str(comment.get("event_time")),
            "authorId": txt.get("user"),
            "targetId": str(target)
        }
        return insert_db(qr)


# NEED TO WORK HERE
def insert_comment(comment: dict):
    if comment is None:
        raise ValueError("Empty Parameter")
    else:
        new_comment = {
            "id": comment.get("id"),
            "textFr": comment.get("textFr"),
            "textEn": comment.get(("textEn")),
            "publishedAt": comment.get("publishedAt"),
            "authorId": comment.get("authorId"),
            "targetId": comment.get("targetId")
            }
    return insert_db(new_comment)


def select_query(query: dict):
    conn = connect_db(os.environ['host'], int(os.environ['port']))
    if conn is not None and query is not None:
        res = []
        mydb = conn[os.environ['Database_db']]
        mycol = mydb[os.environ['Database_Col']]
        result = mycol.find(query)
        for data in result:
            res.append(data)
        conn.close()
        return res
    else:
        raise ValueError("parameters error")


def get_id(query):
    conn = connect_db(os.environ['host'], int(os.environ['port']))
    if conn is not None and query is not None:
        res = []
        mydb = conn[os.environ['Database_db']]
        mycol = mydb[os.environ['Database_Col']]
        result = mycol.find(query)
        for data in result:
            res.append(data)
        conn.close()
        return res[0].get('id')


print(get_id({"id": "1354888"}))
