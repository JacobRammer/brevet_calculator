import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
@app.route("/<path:url>")
def test(url="listAll"):
    # return "http://laptop-service/" + url
    resp = requests.get("http://laptop-service/" + url)
    return resp.content, resp.status_code, resp.headers.items()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
