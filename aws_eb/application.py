from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    print("The Request:")
    print(json.dumps(request.form["input"]))

    return jsonify({"result":"TEST RESULT"})
    # if request.method == 'POST':
    #     return jsonify("TEST RESULT")
    
    
    # 1. load image
    # img_data = request.form()
    # img_bytes = (img_data["file"].read())
    # img = open_image(BytesIO(image_bytes))
    
    # return jsonify({'result': 'TEST RESULT'})
    # return JSONResponse({'result': "TEST RESULT"})
    # return "NOTHING"

    


    





if __name__ == "__main__":
    app.run(debug=True)