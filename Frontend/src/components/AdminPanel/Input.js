import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import Spinner from 'react-bootstrap/Spinner';

function Input(){
  const [deliveryData, setDeliveryData] = useState([]);
  const [driverData, setDriverData] = useState([]);
  const [dimension,setdimension] = useState([]);
  const [driverId, setDriverId] = useState("0");
  const [addressData, setAddress] = useState("");
  const [capacity, setCapacity] = useState(0);
  const [isLoading,setIsLoading] = useState(true);
  const handleDelivery= (event) => {
    event.preventDefault();
    let file = event.target.files[0];

    let reader = new FileReader();
    reader.onload = (e) => {
      let csvData = e.target.result;
      let parsedData = Papa.parse(csvData).data;
      setDeliveryData(parsedData);
    };
    reader.readAsText(file);
  };
  const handleDriver= (event) => {
    event.preventDefault();
    let file = event.target.files[0];

    let reader = new FileReader();
    reader.onload = (e) => {
      let csvData = e.target.result;
      let parsedData = Papa.parse(csvData).data;
      setDriverData(parsedData);
    };
    reader.readAsText(file);
  };
  const handleDimension= (event) => {
    event.preventDefault();
    let file = event.target.files[0];

    let reader = new FileReader();
    reader.onload = (e) => {
      let csvData = e.target.result;
      let parsedData = Papa.parse(csvData).data;
      setdimension(parsedData);
    };
    reader.readAsText(file);
  };
  const handleNextRoute= (event) => {
    setDriverId(event.target.value);
  };

  const handleAddress= (event) => {
    setAddress(event.target.value);
  };

  const handleCapacity= (event) => {
    setCapacity(event.target.value);
  };

  const handleSubmit = async (event) => {
    setIsLoading(false);
    event.preventDefault();
    fetch('http://localhost:5000/csvinput', {
      method: 'POST',
      body: JSON.stringify({
        item1: deliveryData,
        item2: driverData,
        item3: dimension,
      }),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success ip1:', data);
        setIsLoading(true);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  };

  const handleDynamicPickup = async (event) => {
    setIsLoading(false);
    event.preventDefault();
    fetch('http://localhost:5000/dynamicpickup', {
      method: 'POST',
      body: JSON.stringify({
        address: addressData,
        volume: capacity,
      }),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        setIsLoading(true);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  };

  const handleSubmitNextRoute = async (event) => {
    event.preventDefault();
    fetch('http://localhost:5000/nextroute', {
      method: 'POST',
      body: JSON.stringify(driverId),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success ip2:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
  };

  return (

<div className="container">
    {isLoading?<></>:<div>
            <h2 style={{margin:"2em"}}>
                Loading...
                <Spinner animation="border" variant="info" />
            </h2>
        </div>}
  <div className="row m-3 p-md-3 justify-content-center">
    <div></div>
    <div className="col-sm-10">
      <form className="p-3 m-2 border border-1 border-dark rounded" onSubmit={handleSubmit}>
        <div className="form-row">
          <h2 className="m-3">CSV FILE INPUT</h2>
          <div className="form-group">
            <label className="m-2" for="formFile">Delivery Data</label>
            <input className="form-control" type="file" accept=".csv" onChange={handleDelivery} id="formFile" required/>
          </div>
          <div className="form-group">
            <label className="m-2" for="formFile">Driver Data</label>
            <input className="form-control" type="file" accept=".csv" onChange={handleDriver} id="formFile" required/>
          </div>
          <div className="form-group">
            <label className="m-2" for="formFile">Dimension Data</label>
            <input className="form-control" type="file" accept=".csv" onChange={handleDimension} id="formFile" required/>
          </div>
        </div>  
        <button type="submit" className="btn btn-primary m-3">Run Algorithm</button>   
      </form>
    </div>
{/* add onchange for below stuff */}
    <div className="col-sm-10">
      <form className="p-3 m-2 border border-1 border-dark rounded" onSubmit={handleDynamicPickup}>
        <div className="form-row">
          <h2 className="m-3">DYNAMIC DELIVERY INPUT</h2>
          <div className="form-group">
            <label className="m-2" for="formText">Address</label>
            <input className="form-control" type="text" onChange={handleAddress}   id="formText" required/>
          </div>
          <div className="form-group">
            <label className="m-2" for="formNumber">Volume</label>
            <input className="form-control" type="text" onChange={handleCapacity}    id="formNumber" required/>
          </div>
        </div>  
        <button type="submit" className="btn btn-primary m-3">Run Algorithm</button>   
      </form>
    </div>
    
    <div className="col-sm-10">
      <form className="p-3 m-2 border border-1 border-dark rounded" onSubmit={handleSubmitNextRoute}>
        <div className="form-row">
          <h2 className="m-3">DRIVER RE-ROUTING</h2>
          <div className="form-group">
            <label className="m-2" for="formDriverReroute">Driver ID</label>
            <input className="form-control" type="text" onChange={handleNextRoute}  id="formDriverReroute" required/>
          </div>
        </div>  
        <button type="submit" className="btn btn-primary m-3">Run Algorithm</button>   
      </form>
    </div>
  </div>
</div>
  );
}

export default Input;