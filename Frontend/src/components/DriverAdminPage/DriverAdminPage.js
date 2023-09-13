import { useState, useEffect } from "react";
import './DriverAdminPage.css'
import MapAPI from '../API/Map/MapAPI';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import DriverProgress from './DriverProgress/DriverProgress';
import ProgressBar from 'react-bootstrap/ProgressBar'; 
import { useParams, useHistory } from "react-router-dom";
import RouteButton from "../Utils/routeButton";
import ProductDetails from "../Utils/ProductDetails";
import VehicleDetails from "../Utils/VehicleDetails";
import Spinner from 'react-bootstrap/Spinner';
import AllProducts from "../Utils/AllProducts";



export default function DriverAdminPage() {
    const [data, setData] = useState();
    const [message, setMessage] = useState(0);  
    const [isLoading, setIsLoading] = useState(true);

    const chooseMessage = () => {
      setMessage(message+1);
    };
    console.log("message", message)
    const DriverId = useParams().bid;
    useEffect(() => {
        async function fetchData() {
            const response = await fetch("http://localhost:5000/getdriverdetails", {
                method: "POST",
                body: JSON.stringify(DriverId),
                headers: { "Content-Type": "application/json" },
            });
            const json = await response.json();
            setData(json.driverdata);
            console.log("DriverId,", DriverId, json.driverdata);
            setIsLoading(false)

            
        }
        fetchData();
    }, []);

    return (
      <div>
        {isLoading ? 
          <div>
              <h2 style={{margin:"2em"}}>
                  Loading...
                  <Spinner animation="border" variant="info" />
              </h2>
          </div> 
          :
          <div>
              {/* <div className="align-content-center">
                  <h1>DRIVER DELIVERY DETAILS</h1>
              </div> */}
              {data && message+1 && <ProgressBar variant="success" animated now={(message*100)/data[0].locations.length} /> }
              <div className="container-fluid mt-3 p-2" >
                <div className="row">
                  <div className=" col-md-3 col-12 ">
                    <h2 className="text-center">Driver Dashboard</h2>
                  
                        {data && <ProductDetails data={data}  number = {message}/>}
                    
                        {data && <VehicleDetails data = {data} number = {message}/>}
                        {data && <AllProducts data = {data} number = {message}/>}


                      
                  </div>
                  <div className="col-md-9 col-12 overflow-hidden shadow rounded-2 ">
                  {data && <MapAPI locations={data} style={{width:"100%"}} chooseMessage={chooseMessage}/>}

                  </div>
                </div>
              </div>
          </div>

        }
      </div>
    );
}


