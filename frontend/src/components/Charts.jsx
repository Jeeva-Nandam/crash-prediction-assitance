import {
  LineChart, Line, XAxis, YAxis,
  Tooltip, CartesianGrid, ResponsiveContainer,
  BarChart, Bar
} from "recharts";

export default function Charts({ data }) {
  return (
    <div style={{ padding: 40 }}>
      <h2>Revenue vs Expenses</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#4CAF50" />
          <Line type="monotone" dataKey="expenses" stroke="#F44336" />
        </LineChart>
      </ResponsiveContainer>

      <h2 style={{ marginTop: 40 }}>Churn Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="churn" fill="#2196F3" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
