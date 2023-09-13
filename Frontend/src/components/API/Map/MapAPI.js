import { useRef, useEffect, useState } from "react";
import * as tt from "@tomtom-international/web-sdk-maps";
import * as ttapi from "@tomtom-international/web-sdk-services";
import "./MapAPI.css";
import RouteButton from '../../Utils/routeButton'
import "@tomtom-international/web-sdk-maps/dist/maps.css";
import data from "./op.json";
//convert point onclick input to an array of lattitude and longitude coming from the backend
// add the route between two points at any instant and update

const MapAPI = (props) => {
  const mapElement = useRef();
  const result = props.locations[0].locations.map(str => str.split(',').map(Number))
  const [map, setMap] = useState({});
  const [longitude, setLongitude] = useState(77.580009);
  const [latitude, setLatitude] = useState(12.902802);
  const [count, setCount] = useState(0)
  const [delivery, setDelivery] = useState([]);


  const convertToPoints = (lngLat) => {
    return {
      latitude: lngLat[1],
      longitude: lngLat[0],
    };
  };
  const convertToLngLat = (point) => {
    return { lng: point[0], lat: point[1] };
  };

  const drawRoute = (geoJson, map) => {
    if (map.getLayer("route")) {
      map.removeLayer("route");
      map.removeSource("route");
    }
    map.addLayer({
      id: "route",
      type: "line",
      source: {
        type: "geojson",
        data: geoJson,
      },
      paint: {
        "line-color": "#1F51FF",
        "line-width": 6,
      },
    });
  };

  const addDeliveryMarker = (lngLat, map) => {
    const element = document.createElement("div");
    element.className = "marker-delivery";
    new tt.Marker({
      element: element,
    })
      .setLngLat(lngLat)
      .addTo(map);
  };

  useEffect(() => {
    const origin = {
      latitude:latitude,
      longitude:longitude,
    };
    
    
    const destinations = delivery;

    let map = tt.map({
      key: process.env.REACT_APP_TOM_TOM_API_KEY,
      container: mapElement.current,
      center: [longitude, latitude],
      zoom: 17,
      style: data,
      stylesVisibility: {
        trafficIncidents: true,
        trafficFlow: true,
      },
      pitch: 60,
      bearing: 75,
    });
    setMap(map);
   
    var nav = new tt.NavigationControl({});
    map.addControl(nav, 'bottom-right');
    map.addControl(new tt.GeolocateControl({
      positionOptions: {
          enableHighAccuracy: true
      },
      trackUserLocation: true
   }));
    const addMarker = () => {
      const popupOffset = {
        bottom: [0, -25],
      };
      const popup = new tt.Popup({ offset: popupOffset }).setHTML(
        "Driver Location"
      );
      const element = document.createElement("div");
      element.className = "marker";

      const marker = new tt.Marker({
        draggable: true,
        element: element,
      })
        .setLngLat([longitude, latitude])
        .addTo(map);

      marker.on("dragend", () => {
        const lngLat = marker.getLngLat();
        setLongitude(lngLat.lng);
        setLatitude(lngLat.lat);
      });

      marker.setPopup(popup).togglePopup();
    };
    addMarker();

    const deliveryMarker = () => {
      const locations = destinations;
      const pointsForDestinations = locations.map((destination) => {
        return convertToLngLat(destination);
      });
      //console.log(pointsForDestinations);
      pointsForDestinations.forEach((point) => {
        addDeliveryMarker(point, map);
      });
    };
    deliveryMarker();

    const changedestinations = (locations) => {
      
      if (locations.length === 1) {
        return locations;
      }
      if (locations.length > 1) {
        setLatitude(locations[0][1]);
        setLongitude(locations[0][0]);
      }
      locations.shift();
    

    };

    const recalculateRoutes = () => {
      changedestinations(destinations);
    };
    const InitialcalculateRoutes = () => {

      if(delivery.length!==0)
      {
        const array= destinations.map((destination) => {
          return convertToPoints(destination);
        });
        const nn = [];
        for (var i=0;i<1;i++)
        {
           nn[i]=destinations[i];
        }
        const ne = nn.map((destination) => {
          return convertToPoints(destination);
        });
        ne.unshift(origin);
      
        ttapi.services
          .calculateRoute({
            key: process.env.REACT_APP_TOM_TOM_API_KEY,
            traffic: true,
            locations: ne,
          })
          .then((routeData) => {
            const geoJson = routeData.toGeoJson();
            console.log(geoJson)
            drawRoute(geoJson, map);
          });

      }
    
      
    };


    map.on("click", (e) => {
      recalculateRoutes();
      setCount(count+1)
      props.chooseMessage()
    });
    InitialcalculateRoutes();
    return () => map.remove();
  }, [longitude, latitude, delivery]);

  return (
    <>
      {map && (
        <div className="OuterMapContainer border shadow">
          <div ref={mapElement} className="map" />
        </div>
      )}
      <button className="btn btn-primary w-100" onClick={() => setDelivery(result)}>Generate Route</button>
    </>
  );
};

export default MapAPI;
