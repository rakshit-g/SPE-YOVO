import React from "react";
import "./IDDoc.css";

import { Link } from "react-router-dom";

function IDDoc() {
  return (
    <div className="id-doc">
      <div className="card-group">
        <div className="card bg-light">
          <div className="card-body">
            <h5 className="card-title">
              <center>Select the type of ID document</center>
            </h5>
            <p className="card-text">
              <center>You need to upload the photo of your ID</center>
            </p>
            <Link to="/aadhar" className="btn btn-primary">
              Aadhar Card
            </Link>
            &nbsp;
            <a className="card-text btn" href="#">
              More about verification!
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default IDDoc;
