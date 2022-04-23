import pickle

import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

df = pd.read_csv('./crop.csv')
labelencoder = LabelEncoder()
df['label_cat'] = labelencoder.fit_transform(df['label'])
with open('model_pickle', "rb") as f:
    model = pickle.load(f)


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
    # if request.method == "POST":
    #     temp = float(request.form.get("temperature"))
    #     hum = float(request.form.get("humidity"))
    #     ph = float(request.form.get("ph"))
    #     rain = float(request.form.get("rainfall"))
    #     pred = recommend(temp, hum, ph, rain)
    #     crop = pred[0].capitalize()
    #     n = pred[1][0]
    #     p = pred[1][1]
    #     k = pred[1][2]

    #     return render_template("./out.html", crop=crop, n=n, p=p, k=k)
    # return render_template("./index.html")
    return render_template("./Disease-Detection.html")


def recommend(temp, hum, ph, rain):
    preds = list(model.predict([[temp, hum, ph, rain]])[0])
    npk = preds[1:]
    crop_index = round(preds[0])

    mapper = dict(zip(labelencoder.classes_,
                  range(len(labelencoder.classes_))))
    # The code for mapper is from https://stackoverflow.com/questions/42196589/any-way-to-get-mappings-of-a-label-encoder-in-python-pandas

    crop = list(mapper.keys())[list(mapper.values()).index(int(crop_index))]
    # The code for crop is from https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    return crop, npk


if __name__ == "__main__":
    app.run(debug=True)


