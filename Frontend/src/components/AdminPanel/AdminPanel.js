import React from 'react';
import _3dwarehouse from '../images/3dwarehouse.png';
import deliveryman from '../images/deliveryman.png';
import input from '../images/input.png';
import india from '../images/india.png';
import analytics from "../images/analytics3.jpeg"
import RouteButton from '../Utils/routeButton';

import { useCallback } from "react";
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import Card from 'react-bootstrap/Card';
import Spinner from 'react-bootstrap/Spinner';

const AdminPanel = () => {
   
  return (
    <div className="container-fluid mt-0" 
    
  >
   
      <div className="row m-0 p-3">
        <div className="col-4">
          <h2>Admin Panel  
          <Spinner animation="grow" variant="success" style={{marginLeft:"5px"}}/>
          </h2>
        </div>
      </div>

      <div className="row">

      
        <div className="col-lg-4 col-md-4 col-12" >

          <Card style={{ width: '100%', height:"22rem", marginBottom:"1em",
           }}>
            <Container>
              <Row>
            <Col>
              <Card.Img variant="top" src={_3dwarehouse}/>
            </Col>
            <Col>

            <Card.Body>
              <Card.Title>Warehouse Details</Card.Title>
              <Card.Text>
                All the necessary details like volume,AWB of all the packages in the warehouse,their status and driver assigned to them.
              </Card.Text>
              {/* <Button variant="primary">Go somewhere</Button> */}
                <RouteButton className="btn btn-danger align-middle" special={`/Warehouse`}>
                <span className="btn btn-info" style={{width:"100%",marginTop:"5%",height:"7vh"}}>
                      <span className="fw-bold" style={{fontSize:"1.4em",color:"black"}} >Warehouse Page</span>
                    </span>
                </RouteButton>
              </Card.Body>
            </Col>
            </Row>
            </Container>

        </Card>

        </div>
        <div className="col-lg-4 col-md-4 col-12 ">
        <Card style={{ width: '100%',height:"22rem", marginBottom:"1em",
           }}>
        <Container>
           <Row>
            <Col>
              <Card.Img variant="top" src={deliveryman}/>
            </Col>
            <Col>
            <Card.Body>
              <Card.Title>Driver Details</Card.Title>
              <Card.Text>
                Information of all the drivers delivering and their current status of delivery, their location and the packages assigned to them.
              </Card.Text>
              <RouteButton className="btn btn-danger align-middle" special={`/driverdetails`}>
                <span className="btn btn-warning" style={{width:"100%",marginTop:"5%",height:"7vh"}}>
                  <span className="fw-bold" style={{fontSize:"1.4em",color:"black"}} >Delivery Data</span>
                </span>
          </RouteButton>
            </Card.Body>
            </Col>
            </Row>
            </Container>

        </Card>
          

        </div>
        <div className="col-lg-4 col-md-4 col-12">
          <Card style={{ width: '100%',height:"22rem", marginBottom:"1em",
          }}>
          <Container>
              <Row>
            <Col>
              <Card.Img variant="top" src={input} />
            </Col>
            <Col>
              <Card.Body>
                <Card.Title>Adding Data</Card.Title>
                <Card.Text >
                Use the fresh data and run the algorithm to get the best possible route for the driver and assigning the packages to the driver.
                </Card.Text>
                <RouteButton className="btn btn-danger align-middle" special={`/input`}>
                  <span className="btn btn-danger" style={{width:"100%",marginTop:"5%",height:"7vh"}}>
                    <span className="fw-bold" style={{fontSize:"1.4em",color:"black",}}>Input</span>
                  </span>
            </RouteButton>
              </Card.Body>
              </Col>
            </Row>
            </Container>

          </Card>
          
        </div>

        <div className="col-lg-12 col-md-12 col-12 my-3">
        <Card style={{ width: '100%', padding:"1%" ,
            backgroundColor: "#616381",
            backgroundAttachment: "fixed",
            backgroundSize: "contain",
            // backgroundImage: `url("https://img.freepik.com/premium-photo/white-warehouse-background-with-concrete-floor-perspective-view-3d-illustration-rendering_37129-2417.jpg?w=2000")` ,
        }}>
              {/* <Card.Body>
                <Card.Text>
                Getting the analytics
                </Card.Text>
                
              </Card.Body> */}
              <Card.Img variant="top" src={analytics} style ={{border :"2px solid black", height: "36em"}}/>

          </Card>
        {/* <img src={india} className="btn btn-outline shadow-sm border" style={{width: "100%", height: "80%"}}></img> */}

        </div>

        
      </div>
    </div>
  );
}

export default AdminPanel;
