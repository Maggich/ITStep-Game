

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Story from "./pages/Story";
import Characters from "./pages/Characters";
import Evidence from "./pages/Evidence";
import DetectiveNotes from "./pages/DetectiveNotes";
import MainMenu from "./main_page/main_menu";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
  <Route path="/" element={<Login />} />
  <Route path="/home" element={<MainMenu />} />
        <Route path="/story" element={<Story />} />
        <Route path="/characters" element={<Characters />} />
        <Route path="/evidence" element={<Evidence />} />
        <Route path="/detective-notes" element={<DetectiveNotes />} />
        <Route path="/leave" element={<Home />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
