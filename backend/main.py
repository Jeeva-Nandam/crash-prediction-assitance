# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -----------------------------
# # Utility Functions
# # -----------------------------

# def percent_change(old, new):
#     if old == 0:
#         return 0
#     return (new - old) / old


# # -----------------------------
# # Risk Calculations
# # -----------------------------

# def revenue_risk(revenue):
#     declines = sum(1 for i in range(1, len(revenue)) if revenue[i] < revenue[i - 1])
#     if declines >= 3:
#         return 80
#     elif declines == 2:
#         return 60
#     elif declines == 1:
#         return 40
#     return 20


# def expense_risk(revenue, expenses):
#     rev_growth = percent_change(revenue[-2], revenue[-1])
#     exp_growth = percent_change(expenses[-2], expenses[-1])
#     if exp_growth > rev_growth and exp_growth > 0:
#         return 70
#     elif exp_growth > 0:
#         return 40
#     return 20


# def churn_risk(churn):
#     increases = sum(1 for i in range(1, len(churn)) if churn[i] > churn[i - 1])
#     if increases >= 3:
#         return 80
#     elif increases == 2:
#         return 60
#     elif increases == 1:
#         return 40
#     return 20


# def runway_risk(cash_in_hand, revenue, expenses):
#     burn = expenses[-1] - revenue[-1]
#     if burn <= 0:
#         return 10
#     runway_months = cash_in_hand / burn
#     if runway_months < 3:
#         return 90
#     elif runway_months < 6:
#         return 70
#     elif runway_months < 9:
#         return 40
#     return 20


# def risk_label(score):
#     if score < 40:
#         return "LOW RISK"
#     elif score < 70:
#         return "MEDIUM RISK"
#     return "HIGH RISK"


# def generate_explanation(signals):
#     sorted_signals = sorted(signals.items(), key=lambda x: x[1], reverse=True)
#     reasons = []

#     mapping = {
#         "revenue_risk": "continuous revenue decline",
#         "expense_risk": "expenses rising faster than revenue",
#         "churn_risk": "increasing churn",
#         "runway_risk": "short cash runway"
#     }

#     for signal, _ in sorted_signals[:2]:
#         reasons.append(mapping[signal])

#     return "Crash risk is driven by " + " and ".join(reasons) + "."


# def decision_recommendations(signals):
#     recs = []

#     if signals["revenue_risk"] >= 60:
#         recs.append("Increase revenue via upsells and prepaid plans.")

#     if signals["churn_risk"] >= 60:
#         recs.append("Focus on retention and reduce churn immediately.")

#     if signals["expense_risk"] >= 60:
#         recs.append("Control expense growth and cut non-essential costs.")

#     if signals["runway_risk"] >= 70:
#         recs.append("Extend runway by reducing burn rate or raising capital.")

#     if not recs:
#         recs.append("Maintain current trajectory but monitor monthly.")

#     return recs


# # -----------------------------
# # Input Schema
# # -----------------------------

# class CrashInput(BaseModel):
#     revenue: List[float]
#     expenses: List[float]
#     cash_in_hand: float
#     churn_rate: List[float]


# @app.post("/analyze")
# def analyze(data: CrashInput):

#     rev_score = revenue_risk(data.revenue)
#     exp_score = expense_risk(data.revenue, data.expenses)
#     churn_score = churn_risk(data.churn_rate)
#     runway_score = runway_risk(data.cash_in_hand, data.revenue, data.expenses)

#     final_score = round(
#         rev_score * 0.35 +
#         churn_score * 0.25 +
#         exp_score * 0.20 +
#         runway_score * 0.20
#     )

#     signals = {
#         "revenue_risk": rev_score,
#         "expense_risk": exp_score,
#         "churn_risk": churn_score,
#         "runway_risk": runway_score
#     }

#     return {
#         "crash_score": final_score,
#         "risk_level": risk_label(final_score),
#         "explanation": generate_explanation(signals),
#         "recommended_actions": decision_recommendations(signals)
#     }


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime, timedelta


import pandas as pd
from fastapi import UploadFile, File, Form
from fastapi.responses import JSONResponse

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# CSV Validation Function
# -----------------------------

REQUIRED_COLUMNS = ["month", "revenue", "expenses", "churn_rate"]

# def validate_csv(df):
#     errors = []

#     # Missing columns
#     for col in REQUIRED_COLUMNS:
#         if col not in df.columns:
#             errors.append(f"Missing required column: {col}")

#     # Extra columns
#     for col in df.columns:
#         if col not in REQUIRED_COLUMNS:
#             errors.append(f"Unexpected column: {col}")

#     # Check numeric values
#     for col in ["revenue", "expenses", "churn_rate"]:
#         if col in df.columns:
#             if not pd.api.types.is_numeric_dtype(df[col]):
#                 errors.append(f"Column {col} must contain numeric values")

#     return errors

def validate_csv(df):
    errors = []

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    for col in ["revenue", "expenses", "churn_rate"]:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Column {col} must contain numeric values")

    return errors


@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    cash_in_hand: float = Form(...)
):

    try:
        df = pd.read_csv(file.file)

        # Validate
        errors = validate_csv(df)

        if errors:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "issues": errors
                }
            )

        # Extract data
        revenue = df["revenue"].tolist()
        expenses = df["expenses"].tolist()
        churn = df["churn_rate"].tolist()

        # Use existing logic
        rev_score = revenue_risk(revenue)
        exp_score = expense_risk(revenue, expenses)
        churn_score = churn_risk(churn)
        runway_score = runway_risk(cash_in_hand, revenue, expenses)

        final_score = round(
            rev_score * 0.35 +
            churn_score * 0.25 +
            exp_score * 0.20 +
            runway_score * 0.20
        )

        signals = {
            "revenue_risk": rev_score,
            "expense_risk": exp_score,
            "churn_risk": churn_score,
            "runway_risk": runway_score
        }

        crash_date, crash_reason = predict_zero_cash_date(
            cash_in_hand,
            revenue,
            expenses
        )

        improvement = improvement_projection(
            cash_in_hand,
            revenue,
            expenses
        )

        # return {
        #     "status": "success",
        #     "crash_score": final_score,
        #     "risk_level": risk_label(final_score),
        #     "predicted_zero_cash_date": crash_date,
        #     "crash_reason": crash_reason,
        #     "explanation": generate_explanation(signals),
        #     "recommended_actions": decision_recommendations(signals),
        #     "improvement_projection": improvement
        # }

        return {
    "status": "success",
    "crash_score": final_score,
    "risk_level": risk_label(final_score),
    "predicted_zero_cash_date": crash_date,
    "crash_reason": crash_reason,
    "explanation": generate_explanation(signals),
    "recommended_actions": decision_recommendations(signals),
    "improvement_projection": improvement,

    # 🔥 ADD THIS FOR CHARTS
    "months": df["month"].tolist(),
    "revenue": revenue,
    "expenses": expenses,
    "churn_rate": churn
}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# -----------------------------
# Utility Functions
# -----------------------------

def percent_change(old, new):
    if old == 0:
        return 0
    return (new - old) / old


# -----------------------------
# Risk Calculations
# -----------------------------

def revenue_risk(revenue):
    declines = sum(1 for i in range(1, len(revenue)) if revenue[i] < revenue[i - 1])
    if declines >= 3:
        return 80
    elif declines == 2:
        return 60
    elif declines == 1:
        return 40
    return 20


def expense_risk(revenue, expenses):
    if len(revenue) < 2 or len(expenses) < 2:
        return 20

    rev_growth = percent_change(revenue[-2], revenue[-1])
    exp_growth = percent_change(expenses[-2], expenses[-1])

    if exp_growth > rev_growth and exp_growth > 0:
        return 70
    elif exp_growth > 0:
        return 40
    return 20


def churn_risk(churn):
    declines = sum(1 for i in range(1, len(churn)) if churn[i] > churn[i - 1])
    if declines >= 3:
        return 80
    elif declines == 2:
        return 60
    elif declines == 1:
        return 40
    return 20


def runway_risk(cash_in_hand, revenue, expenses):
    burn = expenses[-1] - revenue[-1]
    if burn <= 0:
        return 10

    runway_months = cash_in_hand / burn

    if runway_months < 3:
        return 90
    elif runway_months < 6:
        return 70
    elif runway_months < 9:
        return 40
    return 20


# -----------------------------
# Crash Date Prediction
# -----------------------------

def predict_zero_cash_date(cash_in_hand, revenue, expenses):
    burn = expenses[-1] - revenue[-1]

    if burn <= 0:
        return None, "Company is currently profitable. No crash expected."

    runway_months = cash_in_hand / burn
    runway_days = int(runway_months * 30)

    crash_date = datetime.today() + timedelta(days=runway_days)

    return crash_date.strftime("%d %B %Y"), "Cash runway exhaustion due to continuous negative burn rate."


# -----------------------------
# Risk Label
# -----------------------------

def risk_label(score):
    if score < 40:
        return "LOW RISK"
    elif score < 70:
        return "MEDIUM RISK"
    return "HIGH RISK"


# -----------------------------
# Explanation Generator
# -----------------------------

def generate_explanation(signals):
    sorted_signals = sorted(signals.items(), key=lambda x: x[1], reverse=True)

    mapping = {
        "revenue_risk": "continuous revenue decline",
        "expense_risk": "expenses rising faster than revenue",
        "churn_risk": "increasing customer churn",
        "runway_risk": "short cash runway"
    }

    reasons = []
    for signal, _ in sorted_signals[:2]:
        reasons.append(mapping[signal])

    return "Crash risk is primarily driven by " + " and ".join(reasons) + "."


# -----------------------------
# Recommendation Engine
# -----------------------------

def decision_recommendations(signals):
    recs = []

    if signals["revenue_risk"] >= 60:
        recs.append("Increase revenue through upsells, pricing optimization, or prepaid plans.")

    if signals["churn_risk"] >= 60:
        recs.append("Improve retention by enhancing product value and customer engagement.")

    if signals["expense_risk"] >= 60:
        recs.append("Control expense growth and eliminate non-essential spending.")

    if signals["runway_risk"] >= 70:
        recs.append("Extend runway by reducing burn rate or raising additional capital.")

    if not recs:
        recs.append("Maintain current growth trajectory but monitor metrics monthly.")

    return recs


# -----------------------------
# Improvement Simulation
# -----------------------------

def improvement_projection(cash_in_hand, revenue, expenses):
    current_burn = expenses[-1] - revenue[-1]

    if current_burn <= 0:
        return "Company is already profitable. Focus on scaling."

    # Simulate 15% revenue growth + 10% cost reduction
    improved_revenue = revenue[-1] * 1.15
    reduced_expense = expenses[-1] * 0.90

    new_burn = reduced_expense - improved_revenue

    if new_burn <= 0:
        return "With 15% revenue growth and 10% cost reduction, the company becomes profitable."

    current_runway = cash_in_hand / current_burn
    new_runway = cash_in_hand / new_burn

    extension = new_runway - current_runway

    return f"Strategic improvements can extend runway by approximately {round(extension,1)} months."


# -----------------------------
# Input Schema
# -----------------------------

class CrashInput(BaseModel):
    revenue: List[float]
    expenses: List[float]
    cash_in_hand: float
    churn_rate: List[float]


# -----------------------------
# Main API
# -----------------------------

@app.post("/analyze")
def analyze(data: CrashInput):

    rev_score = revenue_risk(data.revenue)
    exp_score = expense_risk(data.revenue, data.expenses)
    churn_score = churn_risk(data.churn_rate)
    runway_score = runway_risk(data.cash_in_hand, data.revenue, data.expenses)

    final_score = round(
        rev_score * 0.35 +
        churn_score * 0.25 +
        exp_score * 0.20 +
        runway_score * 0.20
    )

    signals = {
        "revenue_risk": rev_score,
        "expense_risk": exp_score,
        "churn_risk": churn_score,
        "runway_risk": runway_score
    }

    crash_date, crash_reason = predict_zero_cash_date(
        data.cash_in_hand,
        data.revenue,
        data.expenses
    )

    improvement = improvement_projection(
        data.cash_in_hand,
        data.revenue,
        data.expenses
    )

    return {
        # "crash_score": final_score,
        # "risk_level": risk_label(final_score),
        # "predicted_zero_cash_date": crash_date,
        # "crash_reason": crash_reason,
        # "explanation": generate_explanation(signals),
        # "recommended_actions": decision_recommendations(signals),
        # "improvement_projection": improvement

            "crash_score": final_score,
    "risk_level": risk_label(final_score),
    "predicted_zero_cash_date": crash_date,
    "crash_reason": crash_reason,
    "explanation": generate_explanation(signals),
    "recommended_actions": decision_recommendations(signals),
    "improvement_projection": improvement,

    # 👇 ADD THESE FOR CHARTS
    "months": [f"M{i+1}" for i in range(len(data.revenue))],
    "revenue": data.revenue,
    "expenses": data.expenses,
    "churn_rate": data.churn_rate
    }
