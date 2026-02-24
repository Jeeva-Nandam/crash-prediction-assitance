from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd

from app.models.schemas import CrashInput
from app.utils.csv_validator import validate_csv
from app.services.calculations import *
from app.services.risk_engine import *
from app.services.recommendations import *

router = APIRouter()


@router.post("/analyze")
def analyze(data: CrashInput):
    rev_trend_value, rev_label = revenue_trend(data.revenue)
    exp_trend_value, exp_label = expense_trend(data.expenses)

    # net_flow = net_cash_flow(data.revenue, data.expenses)
    avg_burn = burn_rate(data.revenue, data.expenses)
    runway_days, runway_status = runway_analysis(
    data.cash_in_hand,
    avg_burn
)

    
    rev_risk = revenue_risk_score(rev_trend_value)
    exp_risk = expense_risk_score([rev_trend_value], [exp_trend_value])
    run_risk = runway_risk_score(runway_days)
    ch_risk = churn_risk_score(data.churn_rate)

    final_score = round((rev_risk + exp_risk + run_risk + ch_risk) / 4)

    signals = {
        "revenue_risk": rev_risk,
        "expense_risk": exp_risk,
        "churn_risk": ch_risk,
        "runway_risk": run_risk
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
        "crash_score": final_score,
        "risk_level": risk_label(final_score),
        "metrics": {
            "revenue_trend": {
                "percentage": rev_trend_value,
                "status": rev_label
            },
            "expense_trend": {
                "percentage": exp_trend_value,
                "status": exp_label
            },
            "burn_rate": {
                "amount_per_month": avg_burn
            },
            "runway": {
            "days_remaining": runway_days,
            "status": runway_status
            }
        },

        "predicted_zero_cash_date": crash_date,
        "crash_reason": crash_reason,
        "explanation": generate_explanation(signals),
        "recommended_actions": decision_recommendations(signals),
        "improvement_projection": improvement,

        "risk_sub_scores": signals,

        # Chart Data
        "months": [f"M{i+1}" for i in range(len(data.revenue))],
        "revenue": data.revenue,
        "expenses": data.expenses,
        "churn_rate": data.churn_rate,
        "customers": data.customers
    }


@router.post("/upload-csv")
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
                content={"status": "error", "issues": errors}
            )

        revenue = df["revenue"].tolist()
        expenses = df["expenses"].tolist()
        churn = df["churn_rate"].tolist()
        customers = df["customers"].tolist()

        return analyze(CrashInput(
            revenue=revenue,
            expenses=expenses,
            cash_in_hand=cash_in_hand,
            churn_rate=churn,
            customers=customers
        ))

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )