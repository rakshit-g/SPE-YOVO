
import React, { useState, Component } from "react";
import ReactDOM from "react-dom";
import ImageUploading from "react-images-uploading";
import axios from "axios";

import "./Otp.css";

class Otp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      emailid: "",
      OTP: "",
      response: "",
      isOTP: false,
      verified: null,
      flag1: false,
      // OTPrecieved : ''
    };

    this.updateInput = this.updateInput.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateOTP = this.updateOTP.bind(this);
    this.checkOtp = this.checkOtp.bind(this);
  }

  updateInput(event) {
    this.setState({ emailid: event.target.value });
  }
  updateOTP(event) {
    this.setState({ OTP: event.target.value });
    console.log(this.state.OTP);
  }

  handleSubmit() {
    this.setState({ isOTP: true });

    console.log("Your input value is: " + this.state.emailid);
    //Send state to the server code
    axios
      .post("http://127.0.0.1:5000/otp", {
        data: JSON.stringify(this.state.emailid),
      })
      .then((res) => {
        console.log(`response = ${res.data}`);
        this.setState({ response: res.data });
        console.log(typeof this.state.response);
        // setName(res.data);
      })
      .catch((error) => {
        console.log(`error = ${error}`);
      });
  }

  checkOtp() {
    console.log(this.state.OTP);
    if (this.state.response === Number(this.state.OTP)) {
      this.setState({ verified: true });
      axios
      .post("http://127.0.0.1:5000/token", {
        data: JSON.stringify(this.state.emailid),
      })
      .catch((error) => {
        console.log(`error = ${error}`);
      });

    } else {
      this.setState({ flag1: true });
      this.setState({ verified: false });
    }
  }

  render() {
    return (
      <div className="otp-handler">
        <center>
          <input
            className="otp-field1"
            placeholder="Enter your email id"
            type="text"
            onChange={this.updateInput}
          ></input>
          <input
            className="email-button"
            type="submit"
            onClick={this.handleSubmit}
          ></input>
          {this.state.isOTP && (
            <div>
              <input
                className="otp-field2"
                placeholder="Enter OTP"
                type="text"
                onChange={this.updateOTP}
              ></input>
              <input
                className="email-button"
                type="submit"
                onClick={this.checkOtp}
              ></input>
            </div>
          )}
          {this.state.verified && <h2> Token ID has been sent to your mail  </h2>}
          {!this.state.verified && this.state.flag1 && <h2> INVALID OTP </h2>}
        </center>
        {/* <h2>{this.state.OTP}</h2> */}
      </div>
    );
  }
}

export default Otp;