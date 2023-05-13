import React, { useState } from "react";
import axios from "axios";
import "./Otp.css";

const Otp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [userEnteredOtp, setUserEnteredOtp] = useState(""); // Add this line
  const [message, setMessage] = useState("");
  const [isOtpVerified, setIsOtpVerified] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/otp", {
        email,
        password,
      });

      const data = response.data;
      setOtp(data.otp); // assuming the server sends back an "otp" field
      setMessage(data.message); // assuming the server sends back a "message" field
    } catch (error) {
      console.error(error);
      setMessage("An error occurred while sending OTP.");
    }
  };

  const handleOtpVerification = () => {
    if (otp === userEnteredOtp) {
      setMessage("OTP verification successful.");
      setIsOtpVerified(true);
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
            value={userEnteredOtp} // Use userEnteredOtp here
            onChange={(e) => setUserEnteredOtp(e.target.value)} // Update userEnteredOtp
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
      {message && <p className={`message ${isOtpVerified ? "success" : "error"}`}>{message}</p>}
    </div>
  );
};

export default Otp;
