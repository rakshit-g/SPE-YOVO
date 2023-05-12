import React, { useState, Component } from "react";
import axios from "axios";

import "./Credit.css";

class Credit extends Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      response: "",
    };

    this.updateInput = this.updateInput.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  updateInput(event) {
    this.setState({ username: event.target.value });
  }

  handleSubmit() {
    console.log("Your input value is: " + this.state.username);
    //Send state to the server code11
    axios
      .post("http://127.0.0.1:5000/credit", {
        data: JSON.stringify(this.state.username),
      })
      .then((res) => {
        console.log(`response = ${res.data}`);
        this.setState({ response: res.data });
        // setName(res.data);
      })
      .catch((error) => {
        console.log(`error = ${error}`);
      });
  }
  render() {
    return (
      <div className="credit-handler">
        <center>
          <input
            className="text-input"
            type="text"
            placeholder="Enter Credit Card number"
            onChange={this.updateInput}
          ></input>
          <input
            className="text-button"
            type="submit"
            onClick={this.handleSubmit}
          ></input>
          <h2>{this.state.response}</h2>
        </center>
      </div>
    );
  }
}

export default Credit;
