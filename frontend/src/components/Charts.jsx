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
  PolarRadiusAxis, Radar, Legend, Cell
} from "recharts";
import '../styles/charts.css'

import { useState } from "react";
export default function Charts({ data, summary }) {
  const [monthsToShow, setMonthsToShow] = useState(data.length);
  // Add profit/loss calculation
  const enhancedData = data.map(item => ({
    ...item,
    profit: item.revenue - item.expenses
  }));

  const filteredData = enhancedData.slice(-monthsToShow);

  const riskData = [
    { subject: "Revenue", value: summary.risk_sub_scores.revenue_risk },
    { subject: "Expense", value: summary.risk_sub_scores.expense_risk },
    { subject: "Runway", value: summary.risk_sub_scores.runway_risk },
    { subject: "Churn", value: summary.risk_sub_scores.churn_risk }
  ];

  return (
    <div style={{ padding: 40 }} className='charts-container'>
        
      {/* Revenue vs Expense + Profit Area */}
      <div className="chart-card">
        <div className="flex-box">
          <h2>📈 Revenue vs Expenses (Profit Impact)</h2>

        <div className="filter-section">
          <label>Show: </label>
          <select
            value={monthsToShow}
            onChange={(e) => setMonthsToShow(Number(e.target.value))}
          >
            <option value={6}>Last 6 Months</option>
            <option value={12}>Last 12 Months</option>
            <option value={24}>Last 24 Months</option>
            <option value={enhancedData.length}>All</option>
          </select>
        </div>
        </div>

      <ResponsiveContainer width="100%" height={350}>
        <AreaChart data={filteredData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />

        <Area
  type="monotone"
  dataKey="profit"
  stroke="#00C853"        // Green
  fill="#00C853"
  fillOpacity={0.2}
/>

<Line
  type="monotone"
  dataKey="revenue"
  stroke="#2979FF"        // Blue
  strokeWidth={3}
/>

<Line
  type="monotone"
  dataKey="expenses"
  stroke="#FF5252"
  strokeWidth={3}
/>
 </AreaChart>
      </ResponsiveContainer>
      </div>

      {/* Burn Rate Trend */}
      <div className="chart-card">
        <div className="flex-box">
        <h2 style={{ marginTop: 50 }}>🔥 Burn Rate Trend</h2>
        <div className="filter-section">
          <label>Show: </label>
          <select
            value={monthsToShow}
            onChange={(e) => setMonthsToShow(Number(e.target.value))}
          >
            <option value={6}>Last 6 Months</option>
            <option value={12}>Last 12 Months</option>
            <option value={24}>Last 24 Months</option>
            <option value={enhancedData.length}>All</option>
          </select>
        </div>
        </div>
      <ResponsiveContainer width="100%" height={300}>
        {/* <BarChart data={enhancedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          
          <Bar dataKey="profit" radius={[8, 8, 0, 0]}>
  {enhancedData.map((entry, index) => (
    <Cell
      key={`cell-${index}`}
      fill={entry.profit < 0 ? "#2979FF" : "#00C853"}
    />
  ))}
</Bar>
        </BarChart> */}

        <BarChart data={filteredData}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Bar dataKey="profit" radius={[8, 8, 0, 0]}>
    {filteredData.map((entry, index) => (
      <Cell
        key={`cell-${index}`}
        fill={entry.profit < 0 ? "#2979FF" : "#00C853"}
      />
    ))}
  </Bar>
</BarChart>
      </ResponsiveContainer>
      </div>

      {/* Churn Trend */}
      <div className="chart-card">
        <div className="flex-box">
        <h2 style={{ marginTop: 50 }}>📉 Customer Churn Trend</h2>
        <div className="filter-section">
          <label>Show: </label>
          <select
            value={monthsToShow}
            onChange={(e) => setMonthsToShow(Number(e.target.value))}
          >
            <option value={6}>Last 6 Months</option>
            <option value={12}>Last 12 Months</option>
            <option value={24}>Last 24 Months</option>
            <option value={enhancedData.length}>All</option>
          </select>
        </div>
        </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={filteredData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          {/* <Line type="monotone" dataKey="churn" stroke="#2196F3" /> */}
          <Line type="monotone" dataKey="churn" stroke="#2979FF" strokeWidth={3} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
      </div>

      {/* Risk Radar Chart */}
      <div className="chart-card">
        <h2 style={{ marginTop: 50 }}>Risk Breakdown</h2>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart data={riskData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Legend />
          {/* <Radar name="Risk" dataKey="value" stroke="#f44336" fill="#f44336" fillOpacity={0.6} /> */}
          <Radar
            name="Risk"
            dataKey="value"
            stroke="#FF3D00"
            fill="#FF3D00"
            fillOpacity={0.5}
          />
        </RadarChart>
      </ResponsiveContainer>
      </div>

    </div>
  );
}