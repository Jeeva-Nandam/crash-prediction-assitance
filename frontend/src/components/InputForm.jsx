import { useState } from "react";
import axios from "axios";

export default function InputForm({ onResult }) {
  const [months, setMonths] = useState(0);
  const [revenue, setRevenue] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [churn, setChurn] = useState([]);
  const [cash, setCash] = useState("");

  const handleMonthChange = (value) => {
    const m = Number(value);
    setMonths(m);
    setRevenue(Array(m).fill(""));
    setExpenses(Array(m).fill(""));
    setChurn(Array(m).fill(""));
  };

  const handleAnalyze = async () => {
    const payload = {
      revenue: revenue.map(Number),
      expenses: expenses.map(Number),
      churn_rate: churn.map(Number),
      cash_in_hand: Number(cash)
    };

    const response = await axios.post(
      "http://127.0.0.1:8000/analyze",
      payload
    );

    onResult(response.data, payload);
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Enter Financial Data</h2>

      <input
        type="number"
        placeholder="How many months?"
        onChange={(e) => handleMonthChange(e.target.value)}
      />

      {months > 0 &&
        [...Array(months)].map((_, i) => (
          <div key={i} style={{ marginTop: 10 }}>
            <h4>Month {i + 1}</h4>

            <input
              type="number"
              placeholder="Revenue"
              value={revenue[i]}
              onChange={(e) => {
                const copy = [...revenue];
                copy[i] = e.target.value;
                setRevenue(copy);
              }}
            />

            <input
              type="number"
              placeholder="Expenses"
              value={expenses[i]}
              onChange={(e) => {
                const copy = [...expenses];
                copy[i] = e.target.value;
                setExpenses(copy);
              }}
            />

            <input
              type="number"
              placeholder="Churn"
              value={churn[i]}
              onChange={(e) => {
                const copy = [...churn];
                copy[i] = e.target.value;
                setChurn(copy);
              }}
            />
          </div>
        ))}

      {months > 0 && (
        <>
          <div style={{ marginTop: 20 }}>
            <input
              type="number"
              placeholder="Cash in Hand"
              value={cash}
              onChange={(e) => setCash(e.target.value)}
            />
          </div>

          <button
            style={{
              marginTop: 20,
              padding: 10,
              background: "#4CAF50",
              color: "white",
              border: "none",
              borderRadius: 5
            }}
            onClick={handleAnalyze}
          >
            Analyze
          </button>
        </>
      )}
    </div>
  );
}
