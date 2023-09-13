import Card from 'react-bootstrap/Card';
import ProgressBar from 'react-bootstrap/ProgressBar';
import './Driverprogress.css'


export default function DriverProgress(){
return (
  <Card >
    <Card.Body>
      <Card.Title>Progress</Card.Title>
      {/* <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle> */}
      {/* <Card.Text>
        <h6>Total Package : 10</h6>
        <h6>Total Time : 23:59</h6>
      </Card.Text> */}
      {/* <hr/> */}
      <ProgressBar now={60} />
    </Card.Body>
  </Card>
);
}
