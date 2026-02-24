import { useState } from "react";
import axios from "axios";
import '../styles/uploadfile.css'

export default function UploadFile({ onResult }) {
  const [file, setFile] = useState(null);
  const [cash, setCash] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setErrorMessage("Please select a CSV file.");
      return;
    }

    if (!cash) {
      setErrorMessage("Please enter cash in hand.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("cash_in_hand", cash);

    try {
      setLoading(true);
      setErrorMessage("");

      const response = await axios.post(
        "http://127.0.0.1:8000/upload-csv",
        formData
      );

      onResult(response.data,  null);
    

    } catch (error) {
      setErrorMessage(
        error.response?.data?.issues?.join("\n") ||
        "File processing error"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 40 }} className="input-container">
      <h2>Upload Financial CSV</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <input
        type="number"
        placeholder="Cash in Hand"
        value={cash}
        onChange={(e) => setCash(e.target.value)}
      />

      <button onClick={handleUpload} disabled={loading}>
        Upload & Analyze
      </button>

      {loading && <p style={{ color: "blue" }}>Processing file...</p>}

      {errorMessage && (
        <p style={{ color: "red" }}>{errorMessage}</p>
      )}
    </div>
  );
}