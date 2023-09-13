from firebase import firebase


url = 'firebase url'
firebase = firebase.FirebaseApplication(url, None)



def driver_schema(productId,Address,latitude,longitude,driverid):
    data = {
        'productId': productId,
        'Address': Address,
        'latitude': latitude,
        'longitude': longitude,
        'driverid': driverid
    }
    result = firebase.post(url+'/driver', data)
    print(result)

def add_route_data(time, driverphone,drivername, dist, src, dest):
    data = {
        'time': time,
        'driverphone': driverphone,
        'drivername': drivername,
        'distance': dist,
        'source': src,
        'destination': dest
    }
    result = firebase.post(url+'/routes', data)
    print(result)

def add_driver_data1(pdtid, address, vol, loc, driverphone,drivername):
    data = {
        'productID': pdtid,
        'Address': address,
        'volume': vol,
        'locations': loc,
        'driverphone': driverphone,
        'drivername': drivername
}
    result = firebase.post(url + '/driver', data)
    print(result)

