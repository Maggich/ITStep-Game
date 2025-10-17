import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const container: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  height: "100vh",
  background: "#0f0f0f",
};

const formStyle: React.CSSProperties = {
  background: "#141212",
  padding: "2rem",
  borderRadius: "8px",
  boxShadow: "0 8px 24px rgba(0,0,0,0.6)",
  color: "#fff",
  width: "360px",
};

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "0.75rem",
  margin: "0.5rem 0",
  borderRadius: "4px",
  border: "1px solid #333",
  background: "#0b0b0b",
  color: "#fff",
};

const btnStyle: React.CSSProperties = {
  width: "100%",
  padding: "0.75rem",
  background: "#a13d1e",
  color: "white",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
  fontWeight: 700,
};

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Пользователь будет взят из БД отдельно — сейчас просто переходим на главную
    navigate("/home");
  };

  return (
    <div style={container}>
      <form style={formStyle} onSubmit={handleSubmit}>
        <h2 style={{ marginTop: 0, color: "#e6a13d" }}>Login</h2>
        <input
          style={inputStyle}
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          style={inputStyle}
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button style={btnStyle} type="submit">Sign in</button>
      </form>
    </div>
  );
};

export default Login;
