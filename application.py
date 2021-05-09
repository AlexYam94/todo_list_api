from flask import Flask, request, render_template

from flask_cors import CORS, cross_origin

import csv

import json

# from firebase_admin import db, credentials

from firebase import firebase

import hashlib

application = Flask(__name__,

            static_url_path='/')

cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

csvFile = "todos/test.csv"

# cred = credentials.Certi

_firebase = firebase.FirebaseApplication("https://test-3a33b.firebaseio.com/todoList",None)

salt = "d04IY5GPSiK7H5ZQ9ndRm5wYzP9Sdn"


def test():

    return {"test":"test"}


@application.route("/")
def hello():

    button = "<p>Hello World</p>"

    return render_template("index.html")


@application.route("/test")
def test():
    return test()


@application.route("/save",methods=["POST"])
def save():

    data = request.json
    print(data)
    

    data["key"] = getHash(data["key"])


    # file = open(csvFile, 'a', newline='\n')

    # writer = csv.writer(file)

    # newLine = [data["id"],data["event"],data["create_date"],data["due_date"]]

    # writer.writerow(newLine)
    

    result = _firebase.patch("/todoList/todo"+str(data["id"]),data)
    print(result)
    return result



@application.route("/read",methods=["POST"])
def read():

    # file = open(csvFile)

    # reader = csv.DictReader(file)

    # data = {"data":[]}

    # for row in reader:

    #     data["data"].append(row)

    # print(json.dumps(data, indent=2))
    

    print(request.json["searchKey"])

    key = getHash(request.json["searchKey"])

    print(key)

    data = _firebase.get("/todoList/","")
    print(data)

    if data is None:

        result = {"error":"No Data Found"}

    else:

        result = {"data":list(data.values())}
    print(result)
    return result


@application.route("/delete")
def delete():

    id = request.args.get("id")
    print(id)

    _firebase.delete("/todoList","todo"+id)
    return "success"


@application.route("/update")
def update():
    return ""


def getHash(raw):

    print(raw.encode('utf-8'))

    md = hashlib.md5()

    md.update(raw.encode('utf-8'))

    key = md.digest()

    print(key.hex())

    return key.hex()


if __name__ == '__main__':
    application.run();