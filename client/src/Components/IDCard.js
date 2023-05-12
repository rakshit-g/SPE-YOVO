import React from "react";

import "./IDCard.css";

import image1 from "./images/image1.png";

import { Link } from "react-router-dom";

function IDCard() {
  return (
    <div className="bg-light id-card">
      <div className="card-group">
        <div className="card bg-light bg-gradient">
          <div className="card-body">
            <p className="card-text">
              <u>You don't need to share:</u>
              <ol className="list-group">
                <li className="list-group-item text-secondary">
                  Personal details
                </li>
                <li className="list-group-item text-secondary">
                  Mobile Numbers
                </li>
                <li className="list-group-item text-secondary">
                  Credit card details
                </li>
              </ol>
            </p>
          </div>
        </div>
        <div className="card">
          <img src={image1} className="card-img-top" alt="..." />
          <div className="card-body bg-light">
            <h5 className="card-title">
              Use an ID document to privately prove your age.
            </h5>
            <ol className="list-group list-group-numbered">
              <li className="list-group-item text-secondary">
                A fast and completely anonymous process with no human
                intervention.
              </li>
              <li className="list-group-item text-secondary">
                Your image will not be stored or shared.
              </li>
              <li className="list-group-item text-secondary">
                SSL secure encryption.
              </li>
            </ol>
            <Link to="/iddoc" className="btn btn-primary">
              Verify your Age
            </Link>
            {/* <a href="#" className="btn btn-primary">Verify your Age</a> */}
            <a href="#" className="btn">
              How does it work?
            </a>
          </div>
        </div>
        <div className="card bg-light bg-gradient">
          <div className="card-body">
            <p className="card-text ">
              <u>To estimate your age:</u>
              <ol className="list-group">
                <li className="list-group-item text-secondary">
                  Ensure proper lighting
                </li>
                <li className="list-group-item text-secondary">
                  Remove any headwear
                </li>
                <li className="list-group-item text-secondary">
                  Keep your glasses on
                </li>
              </ol>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default IDCard;
