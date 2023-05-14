import React, { useState } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import { Link } from "react-router-dom";

import "./Age.css";

const WebcamCapture = () => {
  const webcamRef = React.useRef(null);
  const videoConstraints = {
    width: 200,
    height: 200,
    facingMode: "user",
  };
//   //
// var validators = require('credit-card-validate');
// var card = new validators.cards.Visa('4844410114643094', new Date('2027-01'), '122');
// console.log(card.isValid() ? 'Card is valid' : 'Card is invalid');
  const [name, setName] = useState("");
  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    console.log(typeof(imageSrc));
    console.log(`imageSrc = ${imageSrc}`);
    //for deployment, you should put your backend url / api
    axios
      .post("http://127.0.0.1:5000/api", { data: imageSrc })
      .then((res) => {
        console.log(`response = ${res.data}`);
        setName(res.data);
      })
      .catch((error) => {
        console.log(`error = ${error}`);
      });
  }, [webcamRef]);

  return (
    <div className="webcam">
      <Webcam
        className="capture-box"
        audio={false}
        height={300}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={350}
        videoConstraints={videoConstraints}
      />
      <button onClick={capture}>Capture</button>

      <h2>{name}</h2>

      {name === ",Above 18" ? (
        <>
          <Link to="/idcard">If you want to further register your age token to ease the process next time, click on this to go verify your aadhar OR</Link>
        <Link to ="/">You have verified your age this one time, go to store cart</Link>
        </>
      ) : (
        <p>Try again</p>
      )}
     
    </div>
  );
};

export default WebcamCapture;
