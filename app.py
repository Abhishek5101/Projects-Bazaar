from flask import Flask, render_template, url_for, flash
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://abhi:intensive472@intensive-lsw6x.gcp.mongodb.net/test?retryWrites=true&w=majority")
test_db = cluster["test_db"]
test_collection = test_db["test_collection"]

post = {"name": "tim"}

test_collection.insert_one(post)
