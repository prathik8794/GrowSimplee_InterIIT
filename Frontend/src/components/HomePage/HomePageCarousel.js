import Carousel from 'react-bootstrap/Carousel';
import img1 from "../images/carousel8.jpeg"
import img2 from "../images/carousel2.jpeg"
import img3 from "../images/carousel4.jpeg"
import vehicle from "../images/vehicle.jpg"
import Home from "./TimeLine";



import "./HomePageCarousel.css"

function NoTransitionExample() {
  return (
  <div className="row bg-image" style ={{backgroundImage:"url('../images/vehicle.jpg')"}}>
    <div className='col-lg-9' >
    <Carousel slide={false} className='carousel-styling w-100 justify-content-center' > 
      <Carousel.Item style={{display:"flex",justifyContent:"center"}}>
        <img
          className="w-100"
          style ={{height:"90vh"}}
          src={img1}
          alt="First slide"
        />
        <Carousel.Caption style={{color:"black", top:"1em", bottom:"auto" , backgroundColor:"white", margin:"auto", width:"35vw",borderRadius:"12px"}}>
          <h1>GROW SIMPLEE</h1>
          <h6>Gives you the optimized route with best <b>Distance</b> and <b>Time</b>.</h6>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img
          className="w-100 "
          style ={{height:"90vh"}}
          src={img2}
          alt="Second slide"
        />

        <Carousel.Caption style={{color:"white",backgroundColor:"black",borderRadius:"12px"}}>
          <h3>Best clustering for route minimization</h3>
          <p>The points are clustered according to the number of vehicles, capacity and accordingly gives the best route.</p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img
          className=" w-100"
          style ={{height:"90vh"}}
          src={img3}
          alt="Third slide"
        />

        <Carousel.Caption style={{color:"white",backgroundColor:"black",borderRadius:"12px"}}>
          <h3>Dynamic points and new route</h3>
          <p> Whenever a dynamic pickup is added, driver gets the new optimized route.<br></br>If a driver's shift is done, he gets a new set of routes for thr next shift.</p>
        </Carousel.Caption>
      </Carousel.Item>
    </Carousel>
    </div>
    <div className='col-lg-3'>
      <h1 className="text-center" style={{color:"black" }}> Workflow</h1>
    <Home/>
    </div>
    </div>
  );
}

export default NoTransitionExample;