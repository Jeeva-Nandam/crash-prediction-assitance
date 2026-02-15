export default function ResultCard({ result }) {
  return (
    <div style={{
      padding: 30,
      borderRadius: 10,
      margin: 40,
      background:
        result.risk_level === "HIGH RISK"
          ? "#ffdddd"
          : result.risk_level === "MEDIUM RISK"
          ? "#fff4cc"
          : "#ddffdd"
    }}>
      <h2>Crash Score: {result.crash_score}</h2>
      <h3>{result.risk_level}</h3>

      {result.predicted_zero_cash_date && (
        <p>
          <strong>Predicted Zero Cash Date:</strong>{" "}
          {result.predicted_zero_cash_date}
        </p>
      )}

      <p>{result.explanation}</p>

      <ul>
        {result.recommended_actions.map((rec, i) => (
          <li key={i}>{rec}</li>
        ))}
      </ul>

      <p><strong>Improvement Impact:</strong> {result.improvement_projection}</p>
    </div>
  );
}
