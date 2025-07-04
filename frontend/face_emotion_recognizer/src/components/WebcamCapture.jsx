import React, { useRef } from "react";
import Webcam from "react-webcam";

const WebcamCapture = ({ onCapture }) => {
  const webcamRef = useRef(null);

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    try {
      const response = await fetch("http://localhost:3001", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageSrc })
      });

      const data = await response.json();
      onCapture(data.emotion); // pass emotion to parent
    } catch (error) {
      console.error("Error detecting emotion:", error);
      onCapture("Error");
    }
  };

  return (
    <div>
      <Webcam
        ref={webcamRef}
        audio={false}
        screenshotFormat="image/jpeg"
        width={400}
      />
      <br />
      <button onClick={capture}>Capture Emotion</button>
    </div>
  );
};

export default WebcamCapture;