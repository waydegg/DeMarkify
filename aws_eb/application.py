from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
configure_uploads(app, photos)

# @app.route("/upload", methods=["GET","POST"])
# def upload():
#     if request.method == "POST" and "photo" in request.files:
#         filename = photos.save(request.files["photo"])
#         return filename
#     return render_template("upload.html")

@app.route("/", methods=["GET","POST"])
def index():

    # if request.method == "POST":
    #     filename = photos.save(request.files["photo"])
    #     return filename
    


    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)