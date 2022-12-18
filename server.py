from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

test = {}

Diseases = {}


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/receive_data', methods=["POST", "GET"])
def receive_data():
    Diseases["Heart_Disease"] = {"details": {
        "age": request.form["Age"], "gender": request.form["Gender"], "angina": request.form["Angina"],
        "chest_pain": request.form["ChestPain"], "blood_pressure": request.form["BloodPressure"], "cholesterol": request.form["Cholesterol"],
        "blood_sugar": request.form["BloodSugar"], "electrocardiography": request.form["Electrocardiography"],
        "heart_rate": request.form["HeartRate"], "old_peak": request.form["OldPeak"], "slope": request.form["Slope"]
    }}

    age = int(request.form["Age"])
    gender = request.form["Gender"]
    angina = request.form["Angina"]

    chest_pain = request.form["ChestPain"]

    if gender == "Male":
        gender = 1
    else:
        gender = 0

    if angina == "Yes":
        angina = 1
    else:
        angina = 0

    if chest_pain == "Typical Angina":
        chest_pain = 0
    elif chest_pain == "Atypical angina":
        chest_pain = 1
    elif chest_pain == "Non-Anginal pain":
        chest_pain = 2
    else:
        chest_pain = 3
    blood_pressure = int(request.form["BloodPressure"])
    cholesterol = int(request.form["Cholesterol"])
    blood_sugar = int(request.form["BloodSugar"])

    if blood_sugar > 120:
        blood_sugar = 1
    else:
        blood_sugar = 0

    electrocardiography = request.form["Electrocardiography"]
    if electrocardiography == "Normal":
        electrocardiography = 0
    elif electrocardiography == "Having ST-T wave abnormality":
        electrocardiography = 1
    else:
        electrocardiography = 2
    heart_rate = int(request.form["HeartRate"])
    old_peak = float(request.form["OldPeak"])
    slope = int(request.form["Slope"])

    print(f"Age: {age}")
    print(f"Gender: {gender}")
    print(f"angina: {angina}")
    print(f"chest_pain: {chest_pain}")
    print(f"blood_pressure: {blood_pressure}")
    print(f"cholesterol: {cholesterol}")
    print(f"blood_sugar: {blood_sugar}")
    print(f"electrocardiography: {electrocardiography}")
    print(f"heart_rate: {heart_rate}")
    print(f"OldPeak: {old_peak}")
    print(f"Slope: {slope}")

    model = joblib.load("heart_attack_model.sav")
    predictions = model.predict([[age, gender, chest_pain, blood_pressure, cholesterol, blood_sugar,
                                  electrocardiography, heart_rate, angina, old_peak, slope, 2, 1]])

    print(predictions[0])

    test["Heart_Disease"] = predictions[0]
    if test["Heart_Disease"] == 1:
        test["Heart_Disease"] = "The model predicted that you are likely to have a heart attack."
    else:
        test["Heart_Disease"] = "The model predicted that you are likely to not have have a heart attack."

    return render_template("stroke.html", testing=test, diseasesData=Diseases)


@app.route('/receive_stroke_prediction_data', methods=["POST", "GET"])
def receive_stroke_prediction_data():
    Diseases["Stroke"] = {"details": {"gender": request.form["Gender"], "age": request.form["Age"],
                                      "hypertension": request.form["hypertension"],
                                      "heart_disease": request.form["heart_disease"],
                                      "ever_married": request.form["ever_married"],
                                      "work_type": request.form["work_type"],
                                      "Residence_type": request.form["Residence_type"],
                                      "smoking_status": request.form["smoking_status"].lower()}}

    age = int(request.form["Age"])
    gender = 0 if request.form["Gender"] == "Female" else 1
    hypertension = 1 if request.form["hypertension"] == "Yes" else 0
    heart_disease = 1 if request.form["heart_disease"] == "Yes" else 0
    ever_married = 1 if request.form["ever_married"] == "Yes" else 0

    work_type = request.form["work_type"]
    if work_type == "Children":
        work_type = 0
    elif work_type == "Govt_job":
        work_type = 1
    elif work_type == "Private":
        work_type = 2
    elif work_type == "Self-employed":
        work_type = 3
    else:
        work_type = 4

    residence_type = request.form["Residence_type"]
    if residence_type == "Rural":
        residence_type = 0
    else:
        residence_type = 1

    avg_glucose_level = float(request.form["avg_glucose_level"])
    bmi = float(request.form["bmi"])

    smoking_status = request.form["smoking_status"].lower()
    if smoking_status == "Formerly Smoked":
        smoking_status = 0
    elif smoking_status == "Never Smoked":
        smoking_status = 1
    elif smoking_status == "Smokes":
        smoking_status = 2
    else:
        smoking_status = 3

    print(f"Age: {age}")
    print(f"Gender: {gender}")
    print(f"hypertension: {hypertension}")
    print(f"heart_disease: {heart_disease}")
    print(f"ever_married: {ever_married}")
    print(f"work_type: {work_type}")
    print(f"Residence_type: {residence_type}")
    print(f"avg_glucose_level: {avg_glucose_level}")
    print(f"bmi: {bmi}")
    print(f"smoking_status: {smoking_status}")

    model = joblib.load("stroke_Predictor_RF.sav")

    predictions = model.predict([[gender, age, hypertension, hypertension, ever_married, work_type,
                                  residence_type, avg_glucose_level, bmi, smoking_status]])

    print(f"Stroke Prediction: {predictions[0]}")

    test["Stroke"] = predictions[0]

    if test["Stroke"] == 1:
        test["Stroke"] = "The model predicted that you are likely to have a Stroke."
    else:
        test["Stroke"] = "The model predicted that you are likely to not have a stroke."

    return render_template("diabetes.html", testing=test, diseasesData=Diseases)


@app.route('/receive_diabetes_data', methods=["POST", "GET"])
def receive_diabetes_data():
    Diseases["Diabetes"] = {"details": {"pregnancies": request.form["Pregnancies"],
                                        "glucose": request.form["Glucose"],
                                        "blood_pressure": request.form["BloodPressure"],
                                        "skin_thickness": request.form["SkinThickness"],
                                        "insulin": request.form["Insulin"],
                                        "bmi": request.form["BMI"], "dpf": request.form["DPF"],
                                        "age": request.form["Age"]}}

    Pregnancies = int(request.form["Pregnancies"])
    Glucose = int(request.form["Glucose"])
    BloodPressure = int(request.form["BloodPressure"])
    SkinThickness = int(request.form["SkinThickness"])
    Insulin = int(request.form["Insulin"])
    BMI = float(request.form["BMI"])
    DPF = float(request.form["DPF"])
    Age = int(request.form["Age"])

    print(f"Pregnancies: {Pregnancies}")
    print(f"Glucose: {Glucose}")
    print(f"BloodPressure: {BloodPressure}")
    print(f"SkinThickness: {SkinThickness}")
    print(f"Insulin: {Insulin}")
    print(f"BMI: {BMI}")
    print(f"Diabetes Pedigree Function: {DPF}")
    print(f"Age: {Age}")
    model = joblib.load("diabetes.sav")
    predictions = model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness,
                                  Insulin, BMI, DPF, Age]])

    print(predictions[0])

    test["Diabetes"] = predictions[0]

    if test["Diabetes"] == 1:
        test["Diabetes"] = "The model predicted that you are likely to have Diabetes."
    else:
        test["Diabetes"] = "The model predicted that you are likely to not have Diabetes."

    return render_template("result.html", testing=test, diseasesData=Diseases)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
