import sklearn
from PIL import Image
import pickle
import warnings
from sklearn.linear_model import LogisticRegression
import joblib
from flask import Flask, render_template, request

warnings.filterwarnings('ignore')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index_tumor.html")


@app.route('/tumor_data')
def tumor():
    return render_template("index_tumor.html")


@app.route('/predict_tumor', methods=["POST", "GET"])
def predict_tumor():
    image = request.files['tumor_image']
    dec = {0: 'no tumor', 1: 'yes tumor'}
    i = open('tumor_detection.pkl', "rb")
    model = pickle.load(i)
    img = Image.open(image)
    img1 = img.resize((200, 200))
    img1 = img1.reshape(1, -1) / 255
    p = model.predict(img1)
    res = dec[p[0]]
    print(res)

    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)



