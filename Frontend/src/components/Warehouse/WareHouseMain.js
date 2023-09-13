import { useState } from 'react';
import './WareHouseMain.css';
import ItemList from './ItemList';
import {AiOutlineSearch} from "react-icons/ai"
import { useEffect } from 'react';
import Spinner from 'react-bootstrap/Spinner';


function WareHouseMain() {
    const [data, setData] = useState();
    useEffect(() => {
        setIsLoading(false);
        async function fetchData() {
            const response = await fetch("http://localhost:5000/getvolumedetails", {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            });
            const json = await response.json();
            console.log(json);
            setIsLoading(true);
            setData(json.driverdata);
        }
        fetchData();
    }, []);
    const [query, setQuery] = useState('');
    const [isLoading,setIsLoading] = useState(true);
    return (
        <div className='formStyle'>
             <h2>Warehouse Items 
          </h2>
            {isLoading?<></>:<div>
            <h2 style={{margin:"2em"}}>
                Loading...
                <Spinner animation="border" variant="info" />
            </h2>
        </div> }
            <div className='search'>
                    <input className="searchTerm"  placeholder="Search Entire Product_Id"  onChange={(e) => setQuery(e.target.value)} />
                    <button className="searchButton" type="submit"> <AiOutlineSearch /></button>
            </div>
            {data && <ItemList items={(data)} query={(query)} />}
        </div>
    );
}

export default WareHouseMain;


/**
 * icon size bigger and place middle
 * search bar css
 */