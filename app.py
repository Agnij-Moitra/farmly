from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv(r'./Crop_recommendation.csv')
labelencoder = LabelEncoder()
df['label_cat'] = labelencoder.fit_transform(df['label'])
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        temp = request.form.get("temperature")
        hum = request.form.get("humidity")
        ph = request.form.get("ph")
        rain = request.form.get("rainfall")
        pred = recommend(temp, hum, ph, rain)
        crop = pred[0].capitalize()
        n = pred[1][0]
        p = pred[1][1]
        k = pred[1][2]

        return render_template("./out.html", crop=crop, n=n, p=p, k=k)
    return render_template("./index.html")


def recommend(temp, hum, ph, rain):
    with open('model_pickle', "rb") as f:
        model = pickle.load(f)
    npk = list(model.predict([[34, 7, 4, 5]])[0])[1:]

    crop_index = round(list(model.predict([[34, 7, 4, 5]])[0])[0])

    mapper = dict(zip(labelencoder.classes_,
                  range(len(labelencoder.classes_))))
    # The code for mapper is from https://stackoverflow.com/questions/42196589/any-way-to-get-mappings-of-a-label-encoder-in-python-pandas

    crop = list(mapper.keys())[list(mapper.values()).index(int(crop_index))]
    # The code for crop is from https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    return crop, npk


if __name__ == "__main__":
    app.run(debug=True)
