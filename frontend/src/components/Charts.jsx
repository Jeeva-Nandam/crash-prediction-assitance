// import {
//   LineChart, Line, XAxis, YAxis,
//   Tooltip, CartesianGrid, ResponsiveContainer,
//   BarChart, Bar
// } from "recharts";

// export default function Charts({ data }) {
  
//   return (
//     <div style={{ padding: 40 }}>
//       <h2>Revenue vs Expenses</h2>
//       <ResponsiveContainer width="100%" height={300}>
//         <LineChart data={data}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis dataKey="month" />
//           <YAxis />
//           <Tooltip />
//           <Line type="monotone" dataKey="revenue" stroke="#4CAF50" />
//           <Line type="monotone" dataKey="expenses" stroke="#F44336" />
//         </LineChart>
//       </ResponsiveContainer>

//       <h2 style={{ marginTop: 40 }}>Churn Trend</h2>
//       <ResponsiveContainer width="100%" height={300}>
//         <BarChart data={data}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis dataKey="month" />
//           <YAxis />
//           <Tooltip />
//           <Bar dataKey="churn" fill="#2196F3" />
//         </BarChart>
//       </ResponsiveContainer>
//     </div>
//   );

// }

import {
  LineChart, Line, XAxis, YAxis,
  Tooltip, CartesianGrid, ResponsiveContainer,
  BarChart, Bar, AreaChart, Area,
  RadarChart, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, Radar, Legend
} from "recharts";

export default function Charts({ data, summary }) {

  // Add profit/loss calculation
  const enhancedData = data.map(item => ({
    ...item,
    profit: item.revenue - item.expenses
  }));

  const riskData = [
    { subject: "Revenue", value: summary.risk_sub_scores.revenue_risk },
    { subject: "Expense", value: summary.risk_sub_scores.expense_risk },
    { subject: "Runway", value: summary.risk_sub_scores.runway_risk },
    { subject: "Churn", value: summary.risk_sub_scores.churn_risk }
  ];

  return (
    <div style={{ padding: 40 }}>

      {/* Revenue vs Expense + Profit Area */}
      <h2>📈 Revenue vs Expenses (Profit Impact)</h2>
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart data={enhancedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="profit" stroke="#8884d8" fill="#8884d8" />
          <Line type="monotone" dataKey="revenue" stroke="#4CAF50" />
          <Line type="monotone" dataKey="expenses" stroke="#F44336" />
        </AreaChart>
      </ResponsiveContainer>

      {/* Burn Rate Trend */}
      <h2 style={{ marginTop: 50 }}>🔥 Burn Rate Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={enhancedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="profit" fill="#FF9800" />
        </BarChart>
      </ResponsiveContainer>

      {/* Churn Trend */}
      <h2 style={{ marginTop: 50 }}>📉 Customer Churn Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={enhancedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="churn" stroke="#2196F3" />
        </LineChart>
      </ResponsiveContainer>

      {/* Risk Radar Chart */}
      <h2 style={{ marginTop: 50 }}>⚠ Risk Breakdown</h2>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart data={riskData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Legend />
          <Radar name="Risk" dataKey="value" stroke="#f44336" fill="#f44336" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>

    </div>
  );
}