// export default function Header() {
//   return (
//     <div style={{
//       background: "#111827",
//       color: "white",
//       padding: "20px 40px",
//       fontSize: "24px",
//       fontWeight: "bold"
//     }}>
//       Startup Crash Prediction Dashboard
//     </div>
//   );
// }

import { FaUserCircle } from "react-icons/fa";
import "../styles/header.css";

export default function Header() {
  return (
    <header className="dashboard-header">
      <div className="logo-section">
        Startup Crash Prediction
      </div>

      <div className="right-section">
        <FaUserCircle className="profile-icon" />
        <button className="logout-btn">Logout</button>
      </div>
    </header>
  );
}