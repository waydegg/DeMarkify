from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
configure_uploads(app, photos)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze(request):

    # 1. call lambda function
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image





if __name__ == "__main__":
    app.run(debug=True)