from ast import Try
import pickle
import os
from flask import Flask, jsonify, render_template, request, request_started
from werkzeug.utils import secure_filename
from supplementary import get_disease, recommend
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        temp = float(request.form.get("temperature"))
        hum = float(request.form.get("humidity"))
        ph = float(request.form.get("ph"))
        rain = float(request.form.get("rainfall"))
        pred = recommend(temp, hum, ph, rain)
        crop = pred[0].capitalize()
        n = pred[1][0]
        p = pred[1][1]
        k = pred[1][2]

        return render_template("./out.html", crop=crop, n=n, p=p, k=k)
    return render_template("./index.html")


@app.route("/Disease-Detection", methods=["GET", "POST"])
def disease_detection():
    if request.method == "POST":
        f = request.files['plantDiseaseImg']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, secure_filename(f.filename))
        try:
            f.save(secure_filename(f.filename))
        except FileNotFoundError:
            return render_template("./Disease-Detection-Out.html", is_plant=False, text="FILE NOT FOUND")

        
        disease_info = get_disease(file_path)
        if disease_info == True:
            os.remove(file_path)
            return render_template("./Disease-Detection-Out.html", is_plant=False, text="PLANT NOT FOUND")
        os.remove(file_path)
        return render_template("./Disease-Detection-Out.html", is_plant=True, 
                               title=disease_info["title"],
                               meta_des=disease_info["meta_des"],
                               des=disease_info["des"], 
                               meta_treat=disease_info["meta_treat"], 
                               treat=disease_info["treat"])

    return render_template("./Disease-Detection.html")


if __name__ == "__main__":
    app.run(debug=True)
