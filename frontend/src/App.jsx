import { useState } from "react";
import Header from "./components/Header";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import Charts from "./components/Charts";
import UploadFile from "./components/UploadFile";
import './index.css'
export default function App() {
  const [mode, setMode] = useState("manual");
  const [result, setResult] = useState(null);
  const [chartData, setChartData] = useState([]);

// const handleResult = (response) => {
//   console.log("FULL RESPONSE:", response);

//   // Set result for ResultCard
//   setResult(response);

//   // If revenue does not exist, don't build chart
//   if (!response.revenue || !response.expenses || !response.churn_rate) {
//     setChartData([]);
//     return;
//   }

//   const combined = response.revenue.map((rev, index) => ({
//     month: response.months
//       ? response.months[index]
//       : `M${index + 1}`,
//     revenue: Number(rev),
//     expenses: Number(response.expenses[index]),
//     churn: Number(response.churn_rate[index])
//   }));

//   console.log("CHART DATA:", combined);

//   setChartData(combined);
// };


const handleResult = (response, payload = null) => {
  console.log("FULL RESPONSE:", response);

  setResult(response);

  // Decide where to get months from
  let monthsArray = response.months;

  // If backend does not return months (manual mode)
  if (!monthsArray && payload?.revenue) {
    monthsArray = payload.revenue.map((_, i) => `M${i + 1}`);
  }

  if (!response.revenue || !response.expenses || !response.churn_rate) {
    setChartData([]);
    return;
  }

  const combined = response.revenue.map((rev, index) => ({
    month: monthsArray ? monthsArray[index] : `M${index + 1}`,
    revenue: Number(rev),
    expenses: Number(response.expenses[index]),
    churn: Number(response.churn_rate[index])
  }));

  console.log("CHART DATA:", combined);

  setChartData(combined);
};

  return (
    <>
      <Header />

      <div style={{ display: "flex", gap: 10, padding: 20}} className="app-container">
        {/* <button onClick={() => setMode("manual")}>
          Manual Entry
        </button>

        <button onClick={() => setMode("upload")}>
          Upload CSV
        </button> */}
        <button onClick={() => {
  setMode("manual");
  setResult(null);
  setChartData([]);
}}>
  Manual Entry
</button>

<button onClick={() => {
  setMode("upload");
  setResult(null);
  setChartData([]);
}}>
  Upload CSV
</button>
      </div>

      {mode === "manual" && (
        <InputForm onResult={handleResult} />
      )}

      {mode === "upload" && (
        <UploadFile onResult={handleResult} />
      )}

      {result && <ResultCard result={result} />}
      {result && (
  <Charts data={chartData} summary={result} />
)}

      {/* Only render chart when data exists */}
      {/* {chartData.length > 0 && <Charts data={chartData} />} */}
    </>
  );
}
