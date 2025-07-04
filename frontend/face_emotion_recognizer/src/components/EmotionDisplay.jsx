import React from "react";

const EmotionDisplay = ({ emotion }) => {
  const emojiMap = {
    angry: "😠",
    disgust: "🤢",
    fear: "😨",
    happy: "😊",
    neutral: "😐",
    sad: "😢",
    surprise: "😲"
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Detected Emotion:</h2>
      {emotion ? (
        <h1>
          {emojiMap[emotion.toLowerCase()] || "🤔"} {emotion}
        </h1>
      ) : (
        <p>No emotion detected yet.</p>
      )}
    </div>
  );
};

export default EmotionDisplay;