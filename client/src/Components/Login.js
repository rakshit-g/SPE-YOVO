import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "./Login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/login", {
        email,
        password,
      });

      const data = response.data;
      setMessage(data.message);

      if (response.status === 200) {
        // Login successful, show the link
        setLoggedIn(true);
      } else {
        // Login unsuccessful
        setLoggedIn(false);
      }
    } catch (error) {
      console.error(error);
      setMessage("An error occurred during login.");
      setLoggedIn(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Welcome to YOVO</h2>
      <div className="login-options">
        <Link to="/cards" className="new-user-link">
          New User
        </Link>
        <form className="existing-user" onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
      </div>
      <p className="message">{message}</p>
      {loggedIn ? (
        <p>
          Login successful!{" "}
          <Link to="/" className="redirect-link">
            Click here to proceed.
          </Link>
        </p>
      ) : (
        <p>Login unsuccessful. Please retry.</p>
      )}
    </div>
  );
};

export default Login;
