import os
from flask import Flask, redirect, url_for, request, render_template, session
import flask
from pymongo import MongoClient
import arrow
import acp_times
import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

client = MongoClient("db", 27017)
db = client.tododb


# session["Distance"] = None
# session["start_time"] = None
# session["start_date"] = None


# def help():
#     print("help")
#     print(new())

@app.route('/')
def todo():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('calc.html', items=items), 200


# @app.route("/listAll", methods=["POST", "GET"])
@app.route("/<path:url>", methods=["POST", "GET"])
def list_all(url):
    resp = requests.get("http://api-service/" + url)
    return resp.content, resp.status_code, resp.headers.items()


def remove_empty(lst):
    temp = []
    for i in lst:
        if i != "":
            temp.append(i)
    return temp


def build_dict(km: list, open: list, close: list):
    return_dict = []
    for i in range(len(km)):
        # return_dict.append("KM": km[i]) = [open[i], close[i]]
        temp = {
            "km": km[i],
            "open": open[i],
            "close": close[i]
        }
        return_dict.append(temp)
    print(f"return dict: {return_dict}")
    return return_dict


@app.route('/new', methods=['POST'])
def new():
    # get form data as list
    open_time = request.form.getlist("open")
    close_time = request.form.getlist("close")
    km = request.form.getlist("km")

    # remove empty strings in each list
    km = remove_empty(km)
    close_time = remove_empty(close_time)
    open_time = remove_empty(open_time)

    controls = build_dict(km, open_time, close_time)
    # print("date " + request.args.get("start_date"))

    # print(f"km: {close_time}, {open_time}, {km}")
    # print(f"ffffff {f}")
    # print(f.getlist("km"))

    if len(request.form['name']) == 0:
        return render_template('error.html'), "Form not filled out"

    item_doc = {
        'BrevetName': request.form['name'],  # name of the race
        "Distance": str(session["Distance"]),
        "StartDate": session["start_date"],
        "StartTime": session["start_time"],
        "Controls": controls
        # 'description': request.form['description'],

    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    # app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    # app.logger.debug("km={}".format(km))
    # app.logger.debug("request.args: {}".format(request.args))
    distance = request.args.get("distance", 200, int)
    date = request.args.get("start_date")
    time = request.args.get("start_time")
    t = arrow.get(str(date) + " " + str(time),
                  "YYYY-MM-DD HH:mm")  # create str of date to convert
    open_time = acp_times.open_time(km, distance, t)
    close_time = acp_times.close_time(km, distance, t)
    result = {"open": open_time, "close": close_time}
    session["Distance"] = distance
    session["start_time"] = time
    session["start_date"] = date
    return flask.jsonify(result=result)


if __name__ == "__main__":
    app.secret_key = 'xlPbAQcpnHge2CVmtYG3t9pDYatJSkUTX'
    app.run(host='0.0.0.0', debug=True)
