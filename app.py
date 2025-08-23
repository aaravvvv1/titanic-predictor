import streamlit as st
import joblib
import pandas as pd

# --- LOAD THE SAVED MODEL ---
# The model is loaded once when the app starts and stored in memory.
try:
    model = joblib.load('titanic_model.joblib')
except FileNotFoundError:
    st.error("Model file not found. Please run your notebook to generate the model first.")
    st.stop()

# --- WEB APP INTERFACE ---
st.title("Titanic Survival Prediction 🚢")
st.write("Enter passenger details to predict their chance of survival.")

# Create input fields for the user
# Use sliders, selectboxes, and number inputs for a better user experience.
pclass = st.selectbox("Passenger Class (Pclass)", [1, 2, 3])
sex = st.selectbox("Sex", ["male", "female"])
age = st.slider("Age", 0, 100, 29)
sibsp = st.number_input("Number of Siblings/Spouses Aboard (SibSp)", min_value=0, max_value=10, value=0)
parch = st.number_input("Number of Parents/Children Aboard (Parch)", min_value=0, max_value=10, value=0)
fare = st.number_input("Fare Paid (£)", min_value=0.0, max_value=600.0, value=32.0, step=1.0)
embarked = st.selectbox("Port of Embarkation", ["Cherbourg", "Queenstown", "Southampton"])

# --- PREDICTION LOGIC ---
if st.button("Predict Survival"):
    # Convert the categorical inputs into the same format the model expects
    # This involves creating the dummy variables manually.
    sex_male = 1 if sex == 'male' else 0
    embarked_Q = 1 if embarked == 'Queenstown' else 0
    embarked_S = 1 if embarked == 'Southampton' else 0

    # Create a DataFrame from the inputs with the correct column order
    # The column order MUST match the order used to train the model.
    input_data = pd.DataFrame(
        [[pclass, age, sibsp, parch, fare, sex_male, embarked_Q, embarked_S]],
        columns=['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_male', 'Embarked_Q', 'Embarked_S']
    )

    # Use the loaded model to make a prediction
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)

    # --- DISPLAY THE RESULT ---
    st.subheader("Prediction Result")
    if prediction[0] == 1:
        st.success(f"**This passenger would have likely SURVIVED!** 🎉")
        st.write(f"Confidence: {prediction_proba[0][1]*100:.2f}%")
    else:
        st.error(f"**This passenger would have likely NOT SURVIVED.** 😔")
        st.write(f"Confidence: {prediction_proba[0][0]*100:.2f}%")