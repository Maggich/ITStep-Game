import React from "react";
import { Link } from "react-router-dom";
import detectiveImg from "../assets/detective_icon.png";
import knifeImg from "../assets/knife_icon.png";

const containerStyle: React.CSSProperties = {
  background: "#181515",
  minHeight: "100vh",
  minWidth: "100vw",
  width: "100vw",
  height: "100vh",
  color: "#a13d1e",
  fontFamily: "'Press Start 2P', monospace",
  textAlign: "center",
  position: "relative",
  padding: 0,
  margin: 0,
  overflow: "hidden",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "flex-start",
  backgroundSize: "cover",
};

const menuStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "flex-start",
  alignItems: "center",
  gap: "2rem",
  marginTop: "2.5rem",
  marginLeft: "3rem",
  color: "#a13d1e",
  fontSize: "2rem",
};

const leaveStyle: React.CSSProperties = {
  position: "absolute",
  right: "3rem",
  top: "2.5rem",
  color: "#a13d1e",
  fontSize: "2rem",
  textDecoration: "underline",
  fontFamily: "'Press Start 2P', monospace",
};

const titleStyle: React.CSSProperties = {
  fontSize: "5rem",
  fontWeight: "bold",
  margin: "3rem 0 1.5rem 0",
  letterSpacing: "0.2rem",
  color: "#a15d1e",
  textShadow: "2px 2px 0 #000, 4px 4px 0 #000",
};

const descStyle: React.CSSProperties = {
  fontSize: "2rem",
  marginTop: "2.5rem",
  color: "#a13d1e",
  fontWeight: 700,
};

const subDescStyle: React.CSSProperties = {
  fontSize: "1.3rem",
  marginTop: "1.5rem",
  color: "#e6a13d",
  fontWeight: 700,
};

const artRowStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  gap: "5rem",
  margin: "2rem 0 0 0",
  width: "100%",
  minHeight: "320px",
  position: "relative",
};

const detectiveBgStyle = (img: string): React.CSSProperties => ({
  width: "320px",
  height: "320px",
  backgroundImage: `url(${img})`,
  backgroundSize: "cover",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",
  filter: "drop-shadow(0 8px 16px rgba(0,0,0,0.6))",
  borderRadius: "8px",
});

const overlayStyle: React.CSSProperties = {
  position: "absolute",
  inset: 0,
  background: "linear-gradient(180deg, rgba(0,0,0,0.0) 0%, rgba(0,0,0,0.45) 100%)",
  pointerEvents: "none",
};

const navLinks = [
  { to: "/home", label: "Home" },
  { to: "/story", label: "Story" },
  { to: "/characters", label: "Characters" },
  { to: "/evidence", label: "Evidence" },
  { to: "/detective-notes", label: "Detective's Notes" },
];

function MainMenu() {
  return (
    <div style={containerStyle}>
      <nav style={menuStyle}>
        {navLinks.map((link, idx) => (
          <Link
            key={link.to}
            to={link.to}
            style={{
              color: idx === 0 ? "#a13d1e" : "#a13d1e",
              textDecoration: idx === 0 ? "underline" : "none",
              borderBottom: idx === 0 ? "3px solid #a13d1e" : "none",
              fontWeight: idx === 0 ? 700 : 400,
              paddingBottom: "2px",
            }}
          >
            {link.label}
          </Link>
        ))}
      </nav>
      <Link to="/leave" style={leaveStyle}>leave</Link>
      <div style={titleStyle}>STEPVILLE<br />MURDER</div>
      <div style={artRowStyle}>
  <div style={detectiveBgStyle(detectiveImg)} aria-hidden="true" />
  {/* Нож как иконка справа */}
  <img src={knifeImg} alt="knife" style={{ width: 140, height: 140 }} />
        <div style={overlayStyle} />
      </div>
      <div style={descStyle}>
        Вечеринка в Степ Вилл закончилась смертью.<br />
        Найди убийцу.
      </div>
      <div style={subDescStyle}>
        Настольная игра-расследование о мести, тайнах и лжи.
      </div>
    </div>
  );
}

export default MainMenu;
