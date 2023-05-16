
import React, { useState } from "react";
import axios from "axios";
import "./Otp.css";
import { useLocation } from "react-router-dom"; // Import useLocation from react-router-dom
import { Link } from "react-router-dom";
const Otp = () => {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [userEnteredOtp, setUserEnteredOtp] = useState("");
  const [message, setMessage] = useState("");
  const [isOtpVerified, setIsOtpVerified] = useState(false);
  const [isDetailsStored, setIsDetailsStored] = useState(false);

  // const location = useLocation(); // Access the location object
  // console.log(location)
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/otp", {
        email,
        password,
      });

      const data = response.data;
      setOtp(data.otp);
      setMessage(data.message);
    } catch (error) {
      console.error(error);
      setMessage("An error occurred while sending OTP.");
    }
  };

  const handleOtpVerification = async () => {
    if (otp === userEnteredOtp) {
      setMessage("OTP verification successful.");
      setIsOtpVerified(true);

      try {
        const response = await axios.post("http://127.0.0.1:5000/verifyotp", {
          email,
          password,
        });
        if (response.data) {
          setIsDetailsStored(true);
        } 
        console.log("Email and password sent to /verifyotp");
      } catch (error) {
        console.error(error);
      }
    } else {
      setMessage("Invalid OTP. Please try again.");
      setIsOtpVerified(false);
    }
  };

  return (
    <div className="otp-container">
      <h2>OTP Verification</h2>
      <form className="otp-form" onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="New Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="otp-button">
          Send OTP
        </button>
      </form>
      {otp && (
        <div className="otp-verification">
          <h3>OTP Sent</h3>
          <p>Enter the OTP received in your email:</p>
          <input
            type="text"
            placeholder="OTP"
            value={userEnteredOtp}
            onChange={(e) => setUserEnteredOtp(e.target.value)}
          />
          <button
            type="submit"
            className="otp-verify-button"
            onClick={handleOtpVerification}
          >
            Verify OTP
          </button>
        </div>
      )}
      {message && setIsDetailsStored && <p className={`message ${isOtpVerified ? "success" : "error"}`}>{message}</p>}
      {isOtpVerified && (
        <Link to="/" className="otp-link">
          You have succesfully verified your age and your details are saved. Click on this to redirect to cart.
        </Link>
      )}
      
      {/* {location.state && location.state.image && (
        <div className="image-container">
          <h3>Uploaded Image</h3>
          <img src={location.state.image} alt="Uploaded Aadhar Image" />
        </div>
      )} */}
    </div>
  );
};

export default Otp;
