import React from "react";
import "./Cards.css";
import image1 from "./images/id_verification.png";
import image2 from "./images/face.png";
import image3 from "./images/creditcard.png";
import { Link } from "react-router-dom";

function Cards() {

  function RefreshPage() {
    if(!window.location.hash) {
      window.location = window.location + '#loaded';
      window.location.reload();
    }
  }

  window.onload = RefreshPage();

  return (
    <div className="bg-light cards">
      <div className="card-group">
        <div className="card bg-light bg-gradient">
          <img src={image1} className="card-img-top" alt="..." />
          <div className="card-body">
            <h5 className="card-title">ID Verification</h5>
            <center>Scan your ID document to verify your age.</center>
            <p className="card-text">
              <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Age verification using your ID document
                  <span class="badge bg-primary rounded-pill">1</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Get verified in an instant
                  <span class="badge bg-primary rounded-pill">2</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Only show that you're over 18
                  <span class="badge bg-primary rounded-pill">3</span>
                </li>
              </ul>
            </p>
            <Link to="/idcard" className="btn btn-primary">
              SELECT
            </Link>
            <a href="#" class="btn">
              How it works?
            </a>
          </div>
        </div>
        <div className="card bg-light bg-gradient">
          <img src={image2} className="card-img-top" alt="..." />
          <div className="card-body">
            <h5 className="card-title">Age Estimation</h5>
            <center>Scan your face to get your age estimated.</center>
            <p className="card-text">
              <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  No images are stored or shared
                  <span class="badge bg-primary rounded-pill">1</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  No ID document required
                  <span class="badge bg-primary rounded-pill">2</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Verify once and re-use
                  <span class="badge bg-primary rounded-pill">3</span>
                </li>
              </ul>
            </p>
            <Link to="/age" className="btn btn-primary">
              SELECT
            </Link>
            <a href="#" class="btn">
              How it works?
            </a>
          </div>
        </div>
        <div className="card bg-light bg-gradient">
          <img src={image3} className="card-img-top" alt="..." />
          <div className="card-body">
            <h5 className="card-title">Credit Card Verification</h5>
            <center>
              Upload details of your credit card to verify your age.
            </center>
            <p className="card-text">
              <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Age verification using credit card
                  <span class="badge bg-primary rounded-pill">1</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Get verified in an instant
                  <span class="badge bg-primary rounded-pill">2</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  Only show that you're over 18
                  <span class="badge bg-primary rounded-pill">3</span>
                </li>
              </ul>
            </p>
            <Link to="/credit" className="btn btn-primary">
              SELECT
            </Link>
            <a href="#" class="btn">
              How it works?
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Cards;
