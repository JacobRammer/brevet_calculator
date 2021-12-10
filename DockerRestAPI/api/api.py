# Laptop Service

from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
# Instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
client = MongoClient("db", 27017)
db = client.tododb

mongo_limit = 10000


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
        limit = 1000
        try:
            top = int(request.args.get('top'))
            if top != 0:
                limit = top
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
            top = int(request.args.get('top'))
            if top != 0:
                lim = top
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
            if top != 0:
                limit = top
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
            if top != 0:
                limit = top
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
            if top != 0:
                limit = top
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


# Create routes
# Another way, without decorators
# api.add_resource(Laptop, '/')
api.add_resource(ListAll, '/listAll', "/", "/listAll/json")
api.add_resource(ListOpenOnly, "/listOpenOnly", "/listOpenOnly/json")
api.add_resource(ListCloseOnly, "/listCloseOnly", "/listCloseOnly/json", )
api.add_resource(ListAllCSV, "/listAll/csv")
api.add_resource(ListOpenOnlyCSV, "/listOpenOnly/csv")
api.add_resource(ListCloseOnlyCSV, "/listCloseOnly/csv")

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
