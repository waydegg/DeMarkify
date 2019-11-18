from flask import Flask, render_template, request, jsonify
# from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

# photos = UploadSet('photos', IMAGES)

# app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
# configure_uploads(app, photos)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    jsdata = request.form['result']
    return jsdata

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