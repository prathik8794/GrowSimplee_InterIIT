import 'react-confirm-alert/src/react-confirm-alert.css';
import React from 'react';
import Card from 'react-bootstrap/Card';

// import FancButton from "./Button";

const VehicleDetails = (props) => {
    // const { id } = useParams();
    
    // const { loading, error, data } = useQuery(PRODUCT_DETAILS, {
    //     variables: { id },
    // });

    // if (loading) return <p>Loading...</p>;
    // if (error) return <p>Error :(</p>;
    const color = 'danger'


    return (
        // <div>
        // <h2>Name: Don</h2>
        // <h3>Product Name: Bisleri Bottle</h3>
        // <h5>Address:</h5> 
        // <p>
        // <br/>
        // lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        // lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        // </p>
        // <img
        // src="https://www.bigbasket.com/media/uploads/p/l/265894-2_1-aquafina-packaged-drinking-water.jpg"
        // alt="Trees"
        // height="200"
        // />
        // <h3>Quantity Left in Bag: <br/>
        // 1213 units
        // </h3>
        // <FancButton> Delivered </FancButton>
        // </div>
        // Create a card component for the above
        // <div className='card border-secondary border border-5'>
        //     <div className='card-body'>
        //         <h3 className='card-title d-flex'>VEHICLE DETAILS</h3>
        //         <h5 className='card-title'>Vehicle number : KA 21 MA 2023</h5>
        //         <h5 className='card-title'>Total deliveries : 23</h5>
        //         <h5 className='card-title'>Completed deliveries : 6</h5>
        //         <h5 className='card-title'>Total time : 175 min</h5>
        //         <h5 className='card-title'>Total distance : 20 km</h5>
        //     </div>
        // </div>

    <Card
    bg={color}
    key={color}
    text={color === 'light' ? 'dark' : 'white'}
    style={{ width: '23vw'}}
    className="mb-5"
  >
    <Card.Header>VEHICLE DETAILS</Card.Header>
    <Card.Body>
      <Card.Title></Card.Title>
      <Card.Text>
        {console.log("Driver props", props)}
               <h6>Vehicle number : KA 21 MA 2023</h6>
                 <h6>Total deliveries :{props.data[0].locations.length}</h6>
                 <h6 >Completed deliveries : {props.number}</h6>
                 <h6>Total time : 175 min</h6>
                 <h6>Total distance : 20 km</h6>
      </Card.Text>
    </Card.Body>
  </Card>
    );
};

export default VehicleDetails;