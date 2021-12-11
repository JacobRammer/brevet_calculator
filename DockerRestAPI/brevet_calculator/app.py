import os
from flask import Flask, redirect, url_for, request, render_template, session, jsonify
import flask
import arrow
import acp_times
import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():

    return render_template('calc.html'), 200


# @app.route("/listAll", methods=["POST", "GET"])
@app.route("/<path:url>", methods=["POST", "GET"])
@app.route("/<path:url>/<path:file_type>/", methods=["POST", "GET"])
def list_all(url, file_type=None, limit=str(0)):

    if file_type is not None:  # if we specify json or csv format
        """
        This will parse the url correctly if we specify the file type
        and / or a top query. 
        http://localhost:5000/listClosedOnly/json/?top=4        
        """
        if request.args.get("top"):
            limit = request.args.get("top")
        resp = requests.get("http://api-service/" + url + "/" + file_type + "?top=" + limit)
        return resp.content, resp.status_code, resp.headers.items()

    # if we only do listAll, listClosedOnly, etc
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


@app.route('/new', methods=['POST', "GET"])
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

    if len(request.form['name']) == 0:
        return render_template('error.html'), "Form not filled out"

    item_doc = {
        'BrevetName': request.form['name'],  # name of the race
        "Distance": str(session["Distance"]),
        "StartDate": session["start_date"],
        "StartTime": session["start_time"],
        "Controls": controls

    }

    # print(item_doc)
    headers = {'Content-type': 'application/json'}
    resp = requests.post("http://api-service/new", json=item_doc)

    return redirect(url_for('index'))

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
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    app.run(host='0.0.0.0', debug=True)
