from flask import Flask, render_template, request, jsonify, make_response
import json
import base64
from requests_html import HTMLSession
import pdb

application = Flask(__name__)
session = HTMLSession()

IMGBB_KEY = '578ce2804a501d6c487ac83d34ad950f'
api_endpoint = "https://u97xxuvmpc.execute-api.us-east-2.amazonaws.com/Prod/invocations/"


@application.route("/")
@application.route("/index")
def index():
    return render_template("index.html")

@application.route("/analyze", methods=["POST"])
def analyze():

    # 1. upload image to imgbb
    image_bytes = request.get_data()
    upload_form = {
        "image": base64.b64encode(image_bytes)
    }
    req = session.post(f"https://api.imgbb.com/1/upload?key={IMGBB_KEY}", data=upload_form)


    # 2. call api endpoint
    endpoint_upload_form = {
        "url": req.json()["data"]["url"]
    }
    endpoint_req = session.post(api_endpoint, json=endpoint_upload_form)
    json_data = jsonify({"url": endpoint_req.json()["data"]["url"]})
    # pdb.set_trace()

    res = make_response(json_data, 200)

    print(f"Generated URL: {res}")
    return res


if __name__ == "__main__":
    application.run(debug=False)