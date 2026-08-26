from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# LOAD THE TRAINED MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(r"C:\Users\COMPUMARTS\OneDrive\Desktop\IBM AI Engineering Certification\Machine Learning with Python\Projects\Customer Segmentation Project\model\customer_segmentation_model.pkl")


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Customer Segmentation API",
    description="Customer segmentation using K-Means clustering",
    version="1.0.0"
)


# ============================================================
# INPUT DATA MODEL
# ============================================================

class CustomerData(BaseModel):

    annual_income: float
    spending_score: float


# ============================================================
# CUSTOMER SEGMENT NAMES
# ============================================================

cluster_names = {
    0: "Average Customers",
    1: "Premium Customers",
    2: "High-Spending Customers",
    3: "Careful High-Income Customers",
    4: "Low-Value Customers"
}


# ============================================================
# CUSTOMER SEGMENT DESCRIPTIONS
# ============================================================

cluster_descriptions = {
    0: "Customers with average income and average spending behavior.",

    1: "High-income customers with high spending behavior.",

    2: "Customers with lower income but high spending behavior.",

    3: "High-income customers with relatively low spending behavior.",

    4: "Customers with lower income and low spending behavior."
}


# ============================================================
# HOME ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Customer Segmentation API is running"
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(data: CustomerData):

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame([
        {
            "Annual Income (k$)": data.annual_income,
            "Spending Score (1-100)": data.spending_score
        }
    ])


    # --------------------------------------------------------
    # Predict cluster
    # --------------------------------------------------------

    cluster = int(
        model.predict(input_data)[0]
    )


    # --------------------------------------------------------
    # Convert cluster number to meaningful name
    # --------------------------------------------------------

    segment = cluster_names[cluster]


    # --------------------------------------------------------
    # Get segment description
    # --------------------------------------------------------

    description = cluster_descriptions[cluster]


    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "customer_segment": segment,
        "description": description
    }