import 'react-confirm-alert/src/react-confirm-alert.css';
import React from 'react';
import Card from 'react-bootstrap/Card';

// import FancButton from "./Button";

const ProductDetails = (props) => {
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
    //     <Card border="primary" style={{ width: '18rem' }}>
    //     <Card.Header>Header</Card.Header>
    //     <Card.Body>
    //       <Card.Title>Primary Card Title</Card.Title>
    //       <Card.Text>
    //         Some quick example text to build on the card title and make up the
    //         bulk of the card's content.
    //       </Card.Text>
    //     </Card.Body>
    //   </Card>
    <Card
    bg={color}
    key={color}
    text={color === 'light' ? 'dark' : 'white'}
    style={{ width: '23vw' }}
    className="mb-3 mt-3 ml-1"
  >
    <Card.Header> ORDER DETAILS</Card.Header>
    <Card.Body>
      <Card.Title>Order #{props.number+1}</Card.Title>
      <Card.Text>
               <h6 className='card-title'>Name: {props.data[0].drivername}</h6>
                 <h6 className='card-title'>Product Name: Product_{props.data[0].productID[props.number]}</h6>
                 <h6 className='card-title'>Product Id: {props.data[0].productID[props.number]}</h6>
                 <h6 className='card-title'>Address: {props.data[0].Address[props.number]}</h6>
      </Card.Text>
    </Card.Body>
  </Card>
        // <div className='card border-secondary border border-0'>
        //     <div className='card-body' style={{boxShadow:"0px 0px 3px 3px"}}>
        //          <h3 className='card-title'>ORDER DETAILS</h3>
        //         <h5 className='card-title'>Name: Don</h5>
        //         <h5 className='card-title'>Product Name: FURNITURE</h5>
        //         <h5 className='card-title'>Product Id: SKU_31</h5>
        //         <h5 className='card-title'>Address:</h5>
        //         <p>
        //         1, 24th Main Rd, 1st Phase, Girinagar, KR Layout, Muneshwara T-Block, JP Nagar, Bangalore
        //         </p>
        //     </div>
        // </div>
    );
};

export default ProductDetails;