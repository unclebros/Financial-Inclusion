from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pandas as pd
import joblib


# Define the login page
def login_page():
    """Creates a login page with username and password."""
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button('Login'):
        # Replace the following placeholder with your actual authentication logic
        if username == "admin" and password == "admin":
            st.session_state["authenticated"] = True
            st.success("You are logged in!")
            st.rerun()
        elif username and password:
            st.error("Invalid username or password")

# Load the pre-trained model (replace with your actual model)
def load_model():
    model_path = "Models.pkl"  # Verify the correct path
    try:
        model = joblib.load("FI.pkl")
        st.success("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def predict():
    model = load_model()  # Load the model when the user selects the "Prediction" page
    st.title("Financial Inclusion Prediction")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        data_original = data.copy()  # Keep a copy of the original data

        data = data[['location_type', 'cellphone_access', 'household_size',
                     'age_of_respondent', 'gender_of_respondent', 'relationship_with_head',
                     'marital_status', 'education_level', 'job_type']]
        
        # Encoding categorical variables
        label_encoders = {}
        categorical_columns = ['location_type', 'cellphone_access', 'gender_of_respondent',
                               'relationship_with_head', 'marital_status', 'education_level', 'job_type']

        for column in categorical_columns:
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            label_encoders[column] = le  # Save the label encoder for inverse transformation later

        # Make predictions
        financial = model.predict(data)  # Get predictions

        # Add predictions as a new column to the DataFrame
        data_original['financial_inclusion'] = financial
        
        # Revert encoded values back to original categorical labels
        for column in categorical_columns:
            le = label_encoders[column]
            data_original[column] = le.inverse_transform(data[column])

        data_original.drop('bank_account', axis=1, inplace=True)

        # Display the updated DataFrame
        st.dataframe(data_original)

        # Save predicted data with predictions (optional)
        if st.button("Download Results"):
            data_original.to_csv("financial.csv", index=False)
            st.success("Prediction results downloaded!")

def main():
    """Main application structure."""
    if "authenticated" not in st.session_state:
        st.title("Financial Prediction App")
        login_page()
        return

    st.title("Financial Inclusion Prediction")
    st.write("Financial Inclusion ")

    page = st.sidebar.selectbox("Select a page", ["Home", "Prediction"])

    if page == "Home":
        st.header("About")
        st.write(
            "Financial Inclusion "
        )

    if page == "Prediction":
        predict()

if __name__ == "__main__":
    main()
