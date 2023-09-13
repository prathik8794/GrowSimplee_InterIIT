import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch,
} from "react-router-dom";

import Navbar from "./components/Navbar/Navbar";
import MapAPI from "./components/API/Map/MapAPI";
import Input from "./components/AdminPanel/Input.js";
import ProductDetails from "./components/Utils/ProductDetails";
import Homepage from "./components/AdminPanel/AdminPanel";
import DriverAdminPage from "./components/DriverAdminPage/DriverAdminPage";
import HomePageCarousel from "./components/HomePage/HomePageCarousel";
import DriverDetails from "./components/DriverPage/DriverDetails";
import Warehouse from "./components/Warehouse/WareHouseMain";
import DriverPanel from "./components/AdminPanel/DriverPanel";
import Button from "./components/Utils/routeButton";
import { useState, useEffect } from "react";
import Footer  from "./components/Footer/Footer";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function App() {

  return (
    <Router >
      <Navbar />
      <main style={{ 
      backgroundColor: "#0C969F",
      backgroundAttachment: "fixed",
      backgroundSize: "contain",
      backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 2 1'%3E%3Cdefs%3E%3ClinearGradient id='a' gradientUnits='userSpaceOnUse' x1='0' x2='0' y1='0' y2='1'%3E%3Cstop offset='0' stop-color='%23F7F5F0'/%3E%3Cstop offset='1' stop-color='%23F7FAFF'/%3E%3C/linearGradient%3E%3ClinearGradient id='b' gradientUnits='userSpaceOnUse' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0' stop-color='%2397B6EA' stop-opacity='0'/%3E%3Cstop offset='1' stop-color='%2397B6EA' stop-opacity='1'/%3E%3C/linearGradient%3E%3ClinearGradient id='c' gradientUnits='userSpaceOnUse' x1='0' y1='0' x2='2' y2='2'%3E%3Cstop offset='0' stop-color='%2397B6EA' stop-opacity='0'/%3E%3Cstop offset='1' stop-color='%2397B6EA' stop-opacity='1'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect x='0' y='0' fill='url(%23a)' width='2' height='1'/%3E%3Cg fill-opacity='0.5'%3E%3Cpolygon fill='url(%23b)' points='0 1 0 0 2 0'/%3E%3Cpolygon fill='url(%23c)' points='2 1 2 0 0 0'/%3E%3C/g%3E%3C/svg%3E")` 
    }}>


        <Switch>
          <Route path="/" exact>
            <HomePageCarousel />
              
          </Route>
          <Route path="/driver" exact>
            <DriverAdminPage />
          </Route>
          <Route path="/driverDetails" exact>
            <DriverDetails />
          </Route>
          <Route path="/homepage" exact>
            <HomePageCarousel />
            
          </Route>
          <Route path="/Admin" exact>
            <Homepage />
          </Route>
          <Route path="/Input" exact>
            <Input />
          </Route>
          <Route path="/warehouse" exact>
            <Warehouse />
          </Route>
          <Route path="/driver/:bid" exact>
            <DriverAdminPage />
          </Route>
          <Route path="/AdminDriver" exact>
            <DriverPanel />
          </Route>
          <Redirect to="/" />
        </Switch>
        {/* </Container> */}

      </main>
      <Footer/>
    </Router>
  );
}

export default App;

// <Route path="/" exact>
//             <FetchBooking />
//           </Route>
//           <Route path="/revenue" exact>
//             <Revenue />
//           </Route>
//           <Route path="/billing/invoice/:sid" exact>
//             <BillingPage />
//           </Route>
//           <Route path="/book" exact>
//             <Patient />
//           </Route>
//           <Route path="/newpatient" exact>
//             <CreatePatient/>
//           </Route>
//           <Route path="/history" exact>
//             <BookingById />
//           </Route>
//           <Route path="/billing/update" exact>
//             <CreateTreatment />
//           </Route>
//           <Route path="/getprice" exact>
//             <FetchTreatment />
//           </Route>
//           <Route path="/update/:sid" exact>
//             <UpdateTreatment />
//           </Route>
//           <Route path="/booking/:bid" exact>
//             <UpdateBooking />
//           </Route>
//           <Route path="/booking/:kid/:did" exact>
//             <BookingForm />
//           </Route>

{/* <div className="container-fluid mt-3 p-2">
                <div className="row">
                  <div className="col-6">
                    <div className="card">
                      <div className="card-body">
                        <ProductDetails />
                        <Button
                        className="btn btn-danger align-middle"
                        special={`/Input`}
                        >
                        <span className="btn btn-primary">
                          <span className="fw-bold">Update Diagnosis</span>
                        </span>
                      </Button>
                      </div>
                    </div>
                  </div>
                  <div className="col-6 overflow-hidden shadow rounded-2">
                    {/* <MapAPI /> */}
              //     </div>
              //   </div>
              // </div> */}