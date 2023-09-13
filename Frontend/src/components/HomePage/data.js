const data = [
    {
      title: "Object Input",
      cardTitle: "Capturing Object details",
      cardSubtitle:
        "System to provide dead and volumetric weight of object",
      cardDetailedText: `We have a system set up that captures images of the object placed on the stand at right angle, also we have a weight sensor that shall give us with 
      weight of the object. Now with the help of these details we run our ML algorithm to get the volumetric and dead weight of the object.`
    },
    {
      title: "Data Input",
      cardTitle: "Driver and Address details",
      cardSubtitle: `Input for driver details and address points`,
      cardDetailedText: `Now that we have volumetric and dead weight of the object, we ask for the address location details and driver details of the company. We have a separate
      page for this purpose in the Admin view of our web application`
    },
    {
      title: "Generating Input",
      cardTitle: "Distance & Time Matrix",
      cardSubtitle: `We are fetching distance and time matrix for input to Algorithm`,
      cardDetailedText: `Here in this step we are fetching geolocations, distance and time matrix from the given input data with the help of API which is then passed on to the algorithm.`
    },
    {
      title: "Algorithmic Step",
      cardTitle: "Running of Algorithm",
      cardSubtitle: `Algorithm runs and sends output to database`,
      cardDetailedText: `Now that input for the Algorithm is ready we pass it on to the algorithm in the backend where it generates the output and sends it to the mongodb database.`
    },
    {
      title: "Driver Details",
      cardTitle: "Delivery Task shown to driver",
      cardSubtitle: `Driver is shown the route for his round trip`,
      cardDetailedText: `Our frontend here fetches the data from the backend shows the routing information for the driver. It also allows him twith the option to begin and end the journey.`
    },
    {
      title: "Admin Control",
      cardTitle: "Admin Features",
      cardSubtitle: `Admin is given multiple features which helps him manage efficiently`,
      cardDetailedText: `Admin is given the feature of tracking all the drivers and their current locations. He is also able to see the entire product list and their current status.`
    },
    {
      title: "Dynamic Pickup",
      cardTitle: "Admin Adding Dynamic Pickup",
      cardSubtitle: `re-routing based on dynamic pick up location`,
      cardDetailedText: `Once Admin adds the dynamic pickup point, algorithm is run again and an efficient new route for some particular driver is shown.`
    }
  ];


export default data;