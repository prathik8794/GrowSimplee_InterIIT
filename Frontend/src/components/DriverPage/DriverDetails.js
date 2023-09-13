import Accordion from 'react-bootstrap/Accordion';
import Button from '../Utils/routeButton';
import { useState,useEffect } from 'react';
import RouteButton from '../Utils/routeButton';
import Deliverydata from './Deliverydata';
import Deliverylist from './Deliverylist';
import Spinner from 'react-bootstrap/Spinner';

const DriverDetails = () => {
    const [data, setData] = useState();
    const [isLoading, setIsLoading] = useState(true);
    useEffect(() => {
        async function fetchData() {
            const response = await fetch("http://localhost:5000/getdriveriddetails", {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            });
            const json = await response.json();
            console.log(json);
            setData(json.driverdata);
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
        <div style ={{ marginLeft: "10%", marginRight: "10%", marginTop: "1%"}}>
            <h2>
                Available Drivers
            </h2>
            <Deliverylist data={data} />
         </div>
         }
           
           
            
        
        </div>    
    );
}

export default DriverDetails;