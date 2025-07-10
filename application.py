import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

# Load Titanic model
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        # Retrieve all numeric features
        pclass = float(request.form["num__Pclass"])
        sex = float(request.form["num__Sex"])
        age = float(request.form["num__Age"])
        fare = float(request.form["num__Fare"])
        embarked = float(request.form["num__Embarked"])
        familysize = float(request.form["num__Familysize"])
        isalone = float(request.form["num__Isalone"])
        hascabin = float(request.form["num__HasCabin"])
        title = float(request.form["num__Title"])
        pclass_fare = float(request.form["num__Pclass_Fare"])
        age_fare = float(request.form["num__Age_Fare"])

        # Combine into array in the correct order
        features = np.array([[pclass, sex, age, fare, embarked, familysize, isalone,
                              hascabin, title, pclass_fare, age_fare]])

        # Predict using the model
        prediction = loaded_model.predict(features)[0]

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
