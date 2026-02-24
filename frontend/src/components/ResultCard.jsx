// import '../styles/resultcard.css'

// export default function ResultCard({ result }) {
//   return (
//     <div style={{
//       padding: 30,
//       borderRadius: 10,
//       margin: 40,
//       background:
//         result.risk_level === "HIGH RISK"
//           ? "#ffdddd"
//           : result.risk_level === "MEDIUM RISK"
//           ? "#fff4cc"
//           : "#ddffdd"
//     }}>
//       <h2 className='heading'>Crash Score: {result.crash_score}</h2>
//       <h3>{result.risk_level}</h3>

//       {result.predicted_zero_cash_date && (
//         <p>
//           <strong>Predicted Zero Cash Date:</strong>{" "}
//           {result.predicted_zero_cash_date}
//         </p>
//       )}

//       <p>{result.explanation}</p>

//       <ul>
//         {result.recommended_actions.map((rec, i) => (
//           <li key={i}>{rec}</li>
//         ))}
//       </ul>

//       <p><strong>Improvement Impact:</strong> {result.improvement_projection}</p>
//     </div>
//   );
// }

// import '../styles/resultcard.css'

// export default function ResultCard({ result }) {
//   return (
//     <div
//       style={{
//         padding: 30,
//         borderRadius: 10,
//         margin: 40,
//         background:
//           result.risk_level === "HIGH RISK"
//             ? "#ffdddd"
//             : result.risk_level === "MEDIUM RISK"
//             ? "#fff4cc"
//             : "#ddffdd"
//       }}
//     >
//       <h2 className='heading'>Crash Score: {result.crash_score}</h2>
//       <h3>{result.risk_level}</h3>

//       {/* ===== Core Financial Metrics ===== */}
//       <h4>📊 Core Metrics</h4>
//       <p><strong>Revenue Growth Trend:</strong> {result.revenue_growth_trend}</p>
//       <p><strong>Expense Growth Trend:</strong> {result.expense_growth_trend}</p>
//       <p><strong>Net Cash Flow:</strong> {result.net_cash_flow}</p>
//       <p><strong>Burn Rate:</strong> {result.burn_rate}</p>
//       <p>
//         <strong>Runway Days:</strong>{" "}
//         {result.runway_days === null
//           ? "Unlimited (Profitable)"
//           : result.runway_days}
//       </p>

//       {/* ===== Risk Breakdown ===== */}
//       <h4>⚠ Risk Breakdown</h4>
//       <ul>
//         <li>Revenue Risk: {result.risk_sub_scores?.revenue_risk}</li>
//         <li>Expense Risk: {result.risk_sub_scores?.expense_risk}</li>
//         <li>Runway Risk: {result.risk_sub_scores?.runway_risk}</li>
//         <li>Churn Risk: {result.risk_sub_scores?.churn_risk}</li>
//       </ul>

//       {/* ===== Zero Cash Prediction ===== */}
//       {result.predicted_zero_cash_date && (
//         <p>
//           <strong>Predicted Zero Cash Date:</strong>{" "}
//           {result.predicted_zero_cash_date}
//         </p>
//       )}

//       {/* ===== Explanation ===== */}
    
//        <p>{result.explanation}</p>
     
//       {/* ===== Recommended Actions ===== */}
      
//             <h4>💡 Recommended Actions</h4>
//       <ul>
//         {result.recommended_actions?.map((rec, i) => (
//           <li key={i}>{rec}</li>
//         ))}
//       </ul>
         

//       {/* ===== Improvement Projection ===== */}
      
//         <p>
//         <strong>Improvement Impact:</strong>{" "}
//         {result.improvement_projection}
//       </p>
     
//     </div>
//   );
// }


import '../styles/resultcard.css'

export default function ResultCard({ result }) {

  const metrics = result.metrics || {}

  return (
    <div
      style={{
        padding: 30,
        borderRadius: 10,
        margin: 40,
        background:
          result.risk_level === "HIGH RISK"
            ? "#ffdddd"
            : result.risk_level === "MEDIUM RISK"
            ? "#fff4cc"
            : "#ddffdd"
      }}
      
    >
      <h2 className='heading'>Crash Score: {result.crash_score}</h2>
      <h3>{result.risk_level}</h3>

      {/* ===== Core Financial Metrics ===== */}
      <h4>📊 Core Metrics</h4>

      <p>
        <strong>Revenue Trend:</strong>{" "}
        {metrics.revenue_trend?.percentage}% (
        {metrics.revenue_trend?.status})
      </p>

      <p>
        <strong>Expense Trend:</strong>{" "}
        {metrics.expense_trend?.percentage}% (
        {metrics.expense_trend?.status})
      </p>

      <p>
        <strong>Burn Rate:</strong>{" "}
        ${metrics.burn_rate?.amount_per_month} / month
      </p>

      <p>
        <strong>Runway:</strong>{" "}
        {metrics.runway?.days_remaining === null
          ? "Unlimited"
          : `${metrics.runway?.days_remaining} days`}{" "}
        ({metrics.runway?.status})
      </p>

      {/* ===== Risk Breakdown ===== */}
      <h4>⚠ Risk Breakdown</h4>
      <ul>
        <li>Revenue Risk: {result.risk_sub_scores?.revenue_risk}</li>
        <li>Expense Risk: {result.risk_sub_scores?.expense_risk}</li>
        <li>Runway Risk: {result.risk_sub_scores?.runway_risk}</li>
        <li>Churn Risk: {result.risk_sub_scores?.churn_risk}</li>
      </ul>

      {/* ===== Zero Cash Prediction ===== */}
      {result.predicted_zero_cash_date && (
        <p>
          <strong>Predicted Zero Cash Date:</strong>{" "}
          {result.predicted_zero_cash_date}
        </p>
      )}

      {/* ===== Explanation */}
      <p>{result.explanation}</p>

      {/* ===== Recommended Actions ===== */}
      <h4>💡 Recommended Actions</h4>
      <ul>
        {result.recommended_actions?.map((rec, i) => (
          <li key={i}>{rec}</li>
        ))}
      </ul>

      {/* ===== Improvement Projection ===== */}
      <p>
        <strong>Improvement Impact:</strong>{" "}
        {result.improvement_projection}
      </p>
    </div>
  )
}