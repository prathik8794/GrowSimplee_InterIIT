import React, { useState } from "react";
import "./ProgressbarHS.css";
import "react-step-progress-bar/styles.css";
import { ProgressBar, Step } from "react-step-progress-bar";
import Container from 'react-bootstrap/Container';




export default function HorizontalLine(props) {
  const [points, setpoints] = useState([1,2,3,4])

  const AddPoint = () => {
    setpoints([ ...points,{
      id : points.length + 1
    }])
    
    let RSP = document.querySelector('.RSPBprogressBar');
    RSP.style.setProperty('width','100%');
  }
  return (
    <Container>
      <ProgressBar percent={75}>
        {points.map(point => (
          <Step>
            {({ accomplished, index }) => (
              <div
                className={`indexedStep ${accomplished ? "accomplished" : null}`}
              >
                {index + 1}
              </div>
            )}
          </Step>
        ))}
      </ProgressBar>
      {/* <button type="button" class="btn btn-dark my-3" onClick={AddPoint} > Add point</button> */}
      </Container>
  );

}







