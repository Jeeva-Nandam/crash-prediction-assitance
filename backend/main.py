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

REQUIRED_COLUMNS = ["month", "revenue", "expenses", "churn_rate", "customers"]


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


# @app.post("/upload-csv")
# async def upload_csv(
#     file: UploadFile = File(...),
#     cash_in_hand: float = Form(...)
# ):

#     try:
#         df = pd.read_csv(file.file)

#         # Validate
#         errors = validate_csv(df)

#         if errors:
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": "error",
#                     "issues": errors
#                 }
#             )

#         # Extract data
#         revenue = df["revenue"].tolist()
#         expenses = df["expenses"].tolist()
#         churn = df["churn_rate"].tolist()

#         # Use existing logic
#         rev_score = revenue_risk(revenue)
#         exp_score = expense_risk(revenue, expenses)
#         churn_score = churn_risk(churn)
#         runway_score = runway_risk(cash_in_hand, revenue, expenses)

#         final_score = round(
#             rev_score * 0.35 +
#             churn_score * 0.25 +
#             exp_score * 0.20 +
#             runway_score * 0.20
#         )

#         signals = {
#             "revenue_risk": rev_score,
#             "expense_risk": exp_score,
#             "churn_risk": churn_score,
#             "runway_risk": runway_score
#         }

#         crash_date, crash_reason = predict_zero_cash_date(
#             cash_in_hand,
#             revenue,
#             expenses
#         )

#         improvement = improvement_projection(
#             cash_in_hand,
#             revenue,
#             expenses
#         )

       

#         return {
#             "status": "success",
#             "crash_score": final_score,
#             "risk_level": risk_label(final_score),
#             "predicted_zero_cash_date": crash_date,
#             "crash_reason": crash_reason,
#             "explanation": generate_explanation(signals),
#             "recommended_actions": decision_recommendations(signals),
#             "improvement_projection": improvement,

#             # 🔥 ADD THIS FOR CHARTS
#             "months": df["month"].tolist(),
#             "revenue": revenue,
#             "expenses": expenses,
#             "churn_rate": churn
#         }

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": "error",
#                 "message": str(e)
#             }
#         )

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    cash_in_hand: float = Form(...)
):
    try:
        df = pd.read_csv(file.file)

        errors = validate_csv(df)
        if errors:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "issues": errors
                }
            )

        revenue = df["revenue"].tolist()
        expenses = df["expenses"].tolist()
        churn = df["churn_rate"].tolist()

        # Optional customers column
        customers = df["customers"].tolist() if "customers" in df.columns else []

        # ---- SAME ENGINE AS /analyze ----
        rev_growth = revenue_growth_rate(revenue)
        exp_growth = expense_growth_rate(expenses)

        net_flow = net_cash_flow(revenue, expenses)
        avg_burn = burn_rate(revenue, expenses)
        runway = runway_days(cash_in_hand, avg_burn)

        rev_risk = revenue_risk_score(rev_growth)
        exp_risk = expense_risk_score(rev_growth, exp_growth)
        run_risk = runway_risk_score(runway)
        ch_risk = churn_risk_score(churn)

        final_score = round((rev_risk + exp_risk + run_risk + ch_risk) / 4)

        signals = {
            "revenue_risk": rev_risk,
            "expense_risk": exp_risk,
            "churn_risk": ch_risk,
            "runway_risk": run_risk
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

        return {
            "status": "success",
            "crash_score": final_score,
            "risk_level": risk_label(final_score),
            "predicted_zero_cash_date": crash_date,
            "crash_reason": crash_reason,
            "explanation": generate_explanation(signals),
            "recommended_actions": decision_recommendations(signals),
            "improvement_projection": improvement,

            # 🔥 Advanced metrics
            "revenue_growth_trend": rev_growth,
            "expense_growth_trend": exp_growth,
            "net_cash_flow": net_flow,
            "burn_rate": avg_burn,
            "runway_days": runway,

            "risk_sub_scores": {
                "revenue_risk": rev_risk,
                "expense_risk": exp_risk,
                "runway_risk": run_risk,
                "churn_risk": ch_risk
            },

            # Charts
            "months": df["month"].tolist(),
            "revenue": revenue,
            "expenses": expenses,
            "churn_rate": churn,
            "customers": customers
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
# Core Metric Calculations
# -----------------------------

def revenue_growth_rate(revenue):
    growth = []
    for i in range(1, len(revenue)):
        if revenue[i-1] == 0:
            growth.append(0)
        else:
            g = ((revenue[i] - revenue[i-1]) / revenue[i-1]) * 100
            growth.append(g)
    return growth

def expense_growth_rate(expenses):
    growth = []
    for i in range(1, len(expenses)):
        if expenses[i-1] == 0:
            growth.append(0)
        else:
            g = ((expenses[i] - expenses[i-1]) / expenses[i-1]) * 100
            growth.append(g)
    return growth

def net_cash_flow(revenue, expenses):
    return [r - e for r, e in zip(revenue, expenses)]

def burn_rate(revenue, expenses):
    losses = [e - r for r, e in zip(revenue, expenses) if e > r]
    if not losses:
        return 0
    return sum(losses) / len(losses)

def runway_days(cash_on_hand, burn_rate):
    if burn_rate <= 0:
        return None
    months = cash_on_hand / burn_rate
    return months * 30

def revenue_risk_score(growth):
    avg_growth = sum(growth) / len(growth) if growth else 0

    if avg_growth < -10:
        return 90
    elif -10 <= avg_growth <= 5:
        return 55
    else:
        return 20
    
def expense_risk_score(rev_growth, exp_growth):
    avg_rev = sum(rev_growth) / len(rev_growth) if rev_growth else 0
    avg_exp = sum(exp_growth) / len(exp_growth) if exp_growth else 0

    if avg_exp > avg_rev:
        return 85
    elif abs(avg_exp - avg_rev) < 3:
        return 45
    else:
        return 15


def runway_risk_score(runway_days):

    # ✅ HANDLE PROFITABLE CASE
    if runway_days is None:
        return 0   # No runway risk if company is profitable

    months = runway_days / 30

    if months < 3:
        return 90
    elif months < 6:
        return 70
    elif months < 12:
        return 40
    else:
        return 10
    
def churn_risk_score(churn_rates):
    avg_churn = sum(churn_rates) / len(churn_rates)

    if avg_churn > 10:
        return 90
    elif 5 <= avg_churn <= 10:
        return 55
    else:
        return 20


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
    customers: List[int] 

# -----------------------------
# Main API
# -----------------------------

@app.post("/analyze")
def analyze(data: CrashInput):
    rev_growth = revenue_growth_rate(data.revenue)
    exp_growth = expense_growth_rate(data.expenses)

    net_flow = net_cash_flow(data.revenue, data.expenses)
    avg_burn = burn_rate(data.revenue, data.expenses)
    runway = runway_days(data.cash_in_hand, avg_burn)

    # Risk sub scores
    rev_risk = revenue_risk_score(rev_growth)
    exp_risk = expense_risk_score(rev_growth, exp_growth)
    run_risk = runway_risk_score(runway)
    ch_risk = churn_risk_score(data.churn_rate)

    final_score = round((rev_risk + exp_risk + run_risk + ch_risk) / 4)

    return {
        "crash_score": final_score,
        "risk_level": risk_label(final_score),

        # Trends
        "revenue_growth_trend": rev_growth,
        "expense_growth_trend": exp_growth,

        # Core metrics
        "net_cash_flow": net_flow,
        "burn_rate": avg_burn,
        "runway_days": runway,

        # Risk sub scores
        "risk_sub_scores": {
            "revenue_risk": rev_risk,
            "expense_risk": exp_risk,
            "runway_risk": run_risk,
            "churn_risk": ch_risk
        },

        # Existing chart arrays
        "months": [f"M{i+1}" for i in range(len(data.revenue))],
        "revenue": data.revenue,
        "expenses": data.expenses,
        "churn_rate": data.churn_rate,
        "customers": data.customers   # 👈 NEW
    }
