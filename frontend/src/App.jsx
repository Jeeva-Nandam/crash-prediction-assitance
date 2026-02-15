import { useState } from "react";
import Header from "./components/Header";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import Charts from "./components/Charts";

export default function App() {
  const [result, setResult] = useState(null);
  const [chartData, setChartData] = useState([]);

  const handleResult = (data, payload) => {
    setResult(data);

    const combined = payload.revenue.map((rev, index) => ({
      month: `M${index + 1}`,
      revenue: rev,
      expenses: payload.expenses[index],
      churn: payload.churn_rate[index]
    }));

    setChartData(combined);
  };

  return (
    <>
      <Header />
      <InputForm onResult={handleResult} />
      {result && <ResultCard result={result} />}
      {result && <Charts data={chartData} />}
    </>
  );
}
