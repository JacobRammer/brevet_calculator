# Laptop Service
import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import ast

# Instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


mongo_limit = 10000
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
# client = MongoClient("db", 27017)
client = MongoClient(os.getenv("ATLAS"))
# db = client.brevet
db = client.tododb


class ListOpenOnly(Resource):

    @staticmethod
    def assemble_dict(data):

        return_dict = ["Brevets"]
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                i.pop("close")
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            return_dict.append(temp)

        return return_dict

    def get(self):
        limit = 0
        try:
            top = int(request.args.get('top'))
            if top != 0 and top is not None:
                limit = int(top)
        except:
            pass
        _items = db.tododb.find().limit(limit)
        items = [item for item in _items]
        for item in items:
            item.pop("_id")
        # for item in items["Controls"]:
        #     item.pop("close")
        return self.assemble_dict(items)


class ListAll(Resource):
    """"
    Lists all brevet control points with their
    open / close time(s).
    """

    @staticmethod
    def build_dict(data):

        return_dict = {"Brevets": []}
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            # result = json.dumps(temp, default=set_default)
            return_dict["Brevets"].append(temp)

        return return_dict

    def get(self):
        _items = db.tododb.find().limit(mongo_limit)
        items = [item for item in _items]
        for item in items:
            item.pop("_id")
        return self.build_dict(items)
        # return json.dumps(temp)
        # return JSONEncoder().encode(items)


class ListCloseOnly(Resource):
    @staticmethod
    def build_dict(data):

        return_dict = ["Brevets"]
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                i.pop("open")
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            return_dict.append(temp)

        return return_dict

    def get(self):
        lim = 1000
        try:
            top = request.args.get('top')
            if top != 0 and top is not None and top is not None:
                lim = int(top)
        except:
            pass
        _items = db.tododb.find().limit(lim)
        items = [item for item in _items]
        for item in items:
            item.pop("_id")
        # for item in items["Controls"]:
        #     item.pop("close")
        return self.build_dict(items)


class ListAllCSV(Resource):
    """
    Lists all brevet control points with their
    open / close time(s).
    """

    @staticmethod
    def build_dict(data):

        return_dict = {"Brevets": []}
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            # result = json.dumps(temp, default=set_default)
            return_dict["Brevets"].append(temp)

        return return_dict

    @staticmethod
    def get():
        limit = 1000
        try:
            top = int(request.args.get('top'))
            if top != 0 and top is not None:
                limit = int(top)
        except:
            pass
        _items = db.tododb.find().limit(mongo_limit)
        items = [item for item in _items]
        return_str = "name, distance, start date, start time, km, open, close:"
        itter = 0
        for item in items:
            return_str += "new_entry:"
            if itter == limit:
                break

            item.pop("_id")
            return_str += item["BrevetName"] + ","
            return_str += item["Distance"] + ","
            return_str += item["StartDate"] + ","
            return_str += item["StartTime"] + ","
            for i in item["Controls"]:
                return_str += i["km"] + ","
                return_str += i["open"] + ","
                return_str += i["close"] + ","
            itter += 1
        return return_str.strip('"')


class ListOpenOnlyCSV(Resource):
    """
    Lists all brevet control points with their
    open / close time(s).
    """

    @staticmethod
    def build_dict(data):

        return_dict = {"Brevets": []}
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            # result = json.dumps(temp, default=set_default)
            return_dict["Brevets"].append(temp)

        return return_dict

    @staticmethod
    def get():
        limit = 1000
        try:
            top = int(request.args.get('top'))
            if top != 0 and top is not None:
                limit = int(top)
        except:
            pass
        _items = db.tododb.find().limit(mongo_limit)
        items = [item for item in _items]
        return_str = "name, distance, start date, start time, km, open, close:"
        itter = 0
        for item in items:

            if itter == limit:
                break
            return_str += "new_entry:"
            item.pop("_id")
            return_str += item["BrevetName"] + ","
            return_str += item["Distance"] + ","
            return_str += item["StartDate"] + ","
            return_str += item["StartTime"] + ","
            for i in item["Controls"]:
                i.pop("close")
                return_str += i["km"] + ","
                return_str += i["open"] + ","
            itter += 1
        return return_str.strip('"')


class ListCloseOnlyCSV(Resource):
    """"
    Lists all brevet control points with their
    open / close time(s).
    """

    @staticmethod
    def build_dict(data):

        return_dict = {"Brevets": []}
        for item in data:
            temp1 = item
            temp_dict = []
            for i in temp1["Controls"]:
                temp_dict.append(i)
            temp = {
                "1:BrevetName": temp1["BrevetName"],
                "2:BrevetDistance": temp1["Distance"],
                "3:BrevetStartDate": temp1["StartDate"],
                "4:BrevetStartTime": temp1["StartTime"],
                "5:BrevetControls": temp_dict
            }
            # result = json.dumps(temp, default=set_default)
            return_dict["Brevets"].append(temp)

        return return_dict

    @staticmethod
    def get():
        limit = 1000
        try:
            top = int(request.args.get('top'))
            if top != 0 and top is not None:
                limit = int(top)
        except:
            pass
        _items = db.tododb.find().limit(mongo_limit)
        items = [item for item in _items]
        return_str = "name, distance, start date, start time, km, open, close:"
        itter = 0
        for item in items:

            if itter == limit:
                break

            return_str += "new_entry:"
            item.pop("_id")
            return_str += item["BrevetName"] + ","
            return_str += item["Distance"] + ","
            return_str += item["StartDate"] + ","
            return_str += item["StartTime"] + ","
            for i in item["Controls"]:
                i.pop("open")
                return_str += i["km"] + ","
                return_str += i["close"] + ","
            itter += 1
        return return_str.strip('"')


class NewEntry(Resource):
    """
    Insert a new entry into the database
    """

    def __init__(self):
        self.post_args = reqparse.RequestParser()

    def post(self):
        json_to_str = request.data.decode("utf-8")  # json parameters to str
        str_to_dict = ast.literal_eval(
            json_to_str)  # convert back to dict for mongo
        db.tododb.insert_one(str_to_dict)
        return jsonify({"status": "successfully inserted doc"})


# Create routes
# Another way, without decorators
# api.add_resource(Laptop, '/')
api.add_resource(ListAll, '/listAll', "/", "/listAll/json")
api.add_resource(ListOpenOnly, "/listOpenOnly", "/listOpenOnly/json")
api.add_resource(ListCloseOnly, "/listClosedOnly", "/listClosedOnly/json", )
api.add_resource(ListAllCSV, "/listAll/csv")
api.add_resource(ListOpenOnlyCSV, "/listOpenOnly/csv")
api.add_resource(ListCloseOnlyCSV, "/listClosedOnly/csv")
api.add_resource(NewEntry, "/new")

# Run the application
if __name__ == '__main__':
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.run(host='0.0.0.0', port=80, debug=True)
