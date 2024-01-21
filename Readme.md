# Grow Simplee - Inter IIT Tech Meet 11.0
## Team ID: 57

The statement requires us to build a solution that can optimize the Last Mile Operations
The whole Problem statement can be divided into 3 parts
The first part involves a machine Learning model which can measure the dimensions, weight and condition of the item in least possible time. A Qr code/bar code may be available for assistance but the end result is estimation of the volumetric weight and flagging the erroneous parcels
The second and the main part is a version of route optimization problem. You need to dynamically optimize the route of a driver (modeled by graphs) as during the dropping of parcels some dynamic pickup points will pop up. Furthermore the empty space in the rider’s bag is also taken into consideration. This sums up distance optimization which would be validated against the on time delivery percentage(see problem statement for more details)
The third and the last part would be to incorporate the idea into a web/app based solution and to present it as the final submission

---
## Setup and Installation
In Terminal 1:
```
cd ./Frontend
npm i
npm start

```

In Terminal 2:
```
cd ./FlaskBackend
pip3 install -r requirements.txt
.\venv\Scripts\activate
python server.py
```

