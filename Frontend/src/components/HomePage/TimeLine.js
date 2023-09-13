import React from "react"
import { Chrono } from "react-chrono";
import data from "./data"
import img1 from "../images/icons8-twitter.svg"
import img2 from "../images/icons8-check-inbox-30.png"
function Home(){
return (
    <div style={{
         width: "100%",
          height: "84vh" , 
         }}>
        <Chrono items={data}  theme={{
            primary: 'black',
            secondary: 'white',
            cardBgColor: 'white',
            cardForeColor: 'black',
            titleColor: 'black',
            titleColorActive: 'black',
            
        }}>
            {/* <div className="chrono-icons">
            <img src={img1} alt="image1" />
            <img src={img2} alt="image1" />
            </div> */}
        </Chrono>
    </div>
  )
}

export default Home;