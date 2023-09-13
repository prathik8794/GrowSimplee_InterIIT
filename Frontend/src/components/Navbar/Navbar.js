import React from "react";
import myImage from "../images/logo.png";
const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg shadow-sm navbar-dark bg-dark">
      <div className="container-fluid w-100">
        <a className="navbar-brand" href="/#">
        <img src={myImage} style={{ width: 50, height: 50, padding:"2px" }}></img>
           Grow Simplee 
        </a>
        <button
          className="navbar-toggler ms-auto"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarLinks"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon "></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarLinks">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item active">
              <a className="nav-link" id="home" href="/homepage">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" id="admin" href="/Admin">
                Admin
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" id="driver" href="/driverdetails">
                Driver
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
