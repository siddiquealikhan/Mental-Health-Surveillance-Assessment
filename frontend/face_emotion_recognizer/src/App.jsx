// src/App.jsx
import React, { useState } from "react";
import WebcamCapture from "./components/WebcamCapture";
import EmotionDisplay from "./components/EmotionDisplay";
import "./app.css";

function App() {
  const [emotion, setEmotion] = useState("");

  return (
    <div className="app-container">
      <h1>Facial Emotion Recognition</h1>
      <WebcamCapture onCapture={setEmotion} />
      <EmotionDisplay emotion={emotion} />
    </div>
  );
}

export default App;
