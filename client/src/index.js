import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import "./index.css";
import MainModal from "./Components/MainModal";
import IDCard from "./Components/IDCard";
import Cards from "./Components/Cards";
import IDDoc from "./Components/IDDoc";
import Aadhar from "./Components/Aadhar";
import reportWebVitals from "./reportWebVitals";
import Age from "./Components/Age";
import * as serviceWorker from "./serviceWorker";
import Credit from "./Components/Credit";
import Otp from "./Components/Otp";
import Login from "./Components/Login";

ReactDOM.render(
  <Router>
    <Routes>
      <Route path="/login" element={<Login/>} />
      <Route path="/age" element={<Age />} />
      <Route path="/" element={<MainModal />} />
      <Route path="/cards" element={<Cards />} />
      <Route path="/idcard" element={<IDCard />} />
      <Route path="/iddoc" element={<IDDoc />} />
      <Route path="/aadhar" element={<Aadhar />} />
      <Route path="/otp" element={<Otp />} /> 
      <Route path="/credit" element={<Credit />} /> 

    </Routes>
  </Router>,
  document.getElementById("root")
);
serviceWorker.register();

reportWebVitals();
