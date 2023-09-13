import React from 'react';
import {
    AiFillFacebook,
    AiFillTwitterCircle,
    AiFillInstagram,
    AiFillApple,
} from 'react-icons/ai';
import { FaGooglePlay } from 'react-icons/fa';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import interiit from "../images/interiit.png"

const Footer = () => {
    return (
        <div>
          <Navbar bg="dark" variant="dark" style={{position:"sticky",bottom:"0",width:"100%"}}>
            
          <Navbar.Brand href="/homepage" style={{fontSize:"1.1vw", fontStyle:"italic", width:"100%", padding:"0 1em", margin:"0"}}>
        <Container style={{margin:"auto", paddingTop:"0.3rem"}}>
          <Row>
            <Col xs="2">
              <img
                alt="interiit"
                src={interiit}
                
                style={{width:"3em"}}
              />{' '}
              </Col>
            <Col xs="10">
              <p><b>Grow Simple - Route Planning for Optimized On Time Delivery</b>  is High Prep Event under <b>Inter IIT-Tech Meet 11.0</b></p>
              </Col>
            </Row>
            <Row style={{fontSize:"0.75em", display: "flex",justifyContent: "space-around", right:"0"}}>
                        © Copyright 2023 - Team 57
            </Row>
        </Container>
          </Navbar.Brand>
      </Navbar>
        </div>
    );
};

export default Footer;
