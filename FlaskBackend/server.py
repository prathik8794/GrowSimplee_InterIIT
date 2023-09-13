from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import math
import requests
from schema import *
from testing import *
from algo import *
app = Flask(__name__)
CORS(app)
from geosheets import *
from googleservice import *

dynamic_latitudes = []
dynamic_longitudes = []
latitudes = []
longitudes = []

def make_distance_matrix(address_df):
    
    total_locations = address_df['longitude'].shape[0]
    distance_matrix = np.zeros((total_locations, total_locations))
    time_matrix = np.zeros((total_locations, total_locations))
    API_RANGE = 100
    num_chunks = math.ceil(total_locations/API_RANGE)

    for i in range(0, num_chunks):
        no_of_address1 = API_RANGE
        if total_locations - i*API_RANGE < API_RANGE:
            no_of_address1 = total_locations - i*API_RANGE

        source = address_df['longlat'][i:i+no_of_address1]
        source = ";".join(source)
        source_idx = ";".join([str(i) for i in np.arange(no_of_address1)])

        
        for j in range(0, num_chunks):
            no_of_address2 = API_RANGE
            if total_locations - j*API_RANGE < API_RANGE:
                no_of_address2 = total_locations - j*API_RANGE

            dest = address_df['longlat'][j:j+no_of_address2]
            dest = ";".join(dest)
            dest_idx = ";".join([str(i) for i in np.arange(no_of_address1, no_of_address1+no_of_address2)])

            # Get method of requests module return response object
            url = 'http://router.project-osrm.org/table/v1/driving/' + source+ ";" +dest +"?sources=" + source_idx + "&destinations=" +dest_idx+ "&annotations=distance,duration"
            print(url)
            # url = 'http://router.project-osrm.org/table/v1/car/' + "77.5745235,12.9120799;77.5855601,12.904529;77.5857133,12.9115788;77.5855601,12.904529" + "?sources=0;1;2;3&destinations=0;1;2;3"+"&annotations=distance,duration"

            r = requests.get(url)
            res = r.json()
        
            
            # fill matrix by chunks
            print(i, res)
            for m in range(no_of_address1):
                for n in range(no_of_address2):
                # print('i j m n no_of_address1 2:', i, j, m, n, no_of_address1, no_of_address2)

                    if "distances" in res and "durations" in res:
                        distance_matrix[i*API_RANGE+m][j*API_RANGE+n] = res["distances"][m][n]
                        time_matrix[i*API_RANGE+m][j*API_RANGE+n] = res["durations"][m][n]
                    else:
                        distance_matrix[i*API_RANGE+m][j*API_RANGE+n] = -1
                        time_matrix[i*API_RANGE+m][j*API_RANGE+n] = -1

            # if (i*j) % 5000 == 0:
            # print(i, res)
            # print(time_matrix)
    print(distance_matrix)
    DF = pd.DataFrame(distance_matrix)
    DF.to_csv("distance_matrix.csv")

    DF = pd.DataFrame(time_matrix)
    DF.to_csv("time_matrix.csv")

API_RANGE = 100

def add_point_to_matrix(one_pickup_df, i,distance_matrix,time_matrix, address_df):
  """
  use global distance_matrix, time_matrix, address_df

  """

  total_locations = address_df.shape[0]
  longitude = one_pickup_df['Longitude'][i]
  latitude = one_pickup_df['Latitude'][i]

  num_chunks = math.ceil(total_locations/API_RANGE)
  no_of_address1 = 1
  source = ",".join((str(longitude),str(latitude)))

  distance_vector_1 = []
  distance_vector_2 = []
  time_vector_1 = []
  time_vector_2 = []

  for j in range(0, num_chunks):
    no_of_address2 = API_RANGE
    if total_locations - j*API_RANGE < API_RANGE:
      no_of_address2 = total_locations - j*API_RANGE

    dest = address_df['longlat'][j:j+no_of_address2]
    dest = ";".join([str(i) for i in dest])

    # 1. For src -> destinatons
    source_idx = "0"
    dest_idx = ";".join([str(i) for i in np.arange(no_of_address1, no_of_address1+no_of_address2)])

    url = 'http://router.project-osrm.org/table/v1/driving/' + source+ ";" +dest +"?sources=" + source_idx + "&destinations=" +dest_idx+ "&annotations=distance,duration"
    r = requests.get(url)
    res = r.json()  

    # get distances in chunks    
    distance_vector_1 += res["distances"][0]
    time_vector_1 += res["durations"][0]


    # 2. For destinatons -> src
    source_idx = str(no_of_address1 + no_of_address2 - 1)
    dest_idx = ";".join([str(i) for i in np.arange(0, no_of_address2)])

    url = 'http://router.project-osrm.org/table/v1/driving/' + dest + ";" + source +"?sources=" + source_idx + "&destinations=" +dest_idx+ "&annotations=distance,duration"
    print("url 2:", url)
    r = requests.get(url)
    res = r.json()  

    # get distances in chunks    
    distance_vector_2 += res["distances"][0]
    time_vector_2 += res["durations"][0]


  # distance time matrix
  distance_vector_1 = np.array(distance_vector_1).reshape(total_locations, 1)
  distance_vector_2 = np.array(distance_vector_2).reshape(total_locations, 1)
  distance_matrix = np.r_[distance_matrix, distance_vector_1.T]
  distance_vector_2  = np.append(distance_vector_2, (0))
  distance_matrix = np.c_[distance_matrix, distance_vector_2]

  time_vector_1 = np.array(time_vector_1).reshape(total_locations, 1)
  time_vector_2 = np.array(time_vector_2).reshape(total_locations, 1)
  time_matrix = np.r_[time_matrix, time_vector_1.T]
  time_vector_2  = np.append(time_vector_2, (0))
  time_matrix = np.c_[time_matrix, time_vector_2]


  # add new data
  address_df = address_df.append(one_pickup_df)

  return distance_matrix , time_matrix , address_df
  # print(distance_matrix)



def dynamic_pick_up(pickups_data):

  address_df = pd.read_csv("./bangalore_dispatch_data.csv", index_col=False)
  time_matrix = pd.read_csv("./time_matrix.csv", index_col=False)
  distance_matrix = pd.read_csv("./distance_matrix.csv", index_col=False)

  pickups_df = pd.DataFrame(data=pickups_data, columns=address_df.columns[:7])
  pickups_df['longlat'] = pickups_df[['Longitude','Latitude']].astype(str).agg(','.join, axis=1)

  time_matrix = time_matrix[time_matrix.columns[1:]]
  distance_matrix = distance_matrix[distance_matrix.columns[1:]]

  address_df['longlat'] = address_df[['Longitude','Latitude']].astype(str).agg(','.join, axis=1)



  for i in range(pickups_df.shape[0]):
    distance_matrix,time_matrix, address_df = add_point_to_matrix(pickups_df.iloc[[i]], i,distance_matrix,time_matrix, address_df)
    

  pd.DataFrame(distance_matrix).to_csv("./distance_matrix.csv")
  pd.DataFrame(time_matrix).to_csv("./time_matrix.csv")

  address_df = address_df[address_df.columns[:-1]]
  pd.DataFrame(address_df).to_csv("./bangalore_dispatch_data.csv", index=False)

  print(address_df.shape)
  print(distance_matrix.shape)
  print(time_matrix.shape)
  print(address_df)



def get_lng_lat(df):
    
    global latitudes
    global longitudes
    global dynamic_latitudes
    global dynamic_longitudes
    
    print("into function")
    update_sheet(df)
    print("updated sheets")
    run_sheets()
    print("Ran_sheets. reading data...")
    new_df = get_full_data()
    latitudes = new_df['Latitude'].to_list()
    longitudes = new_df['Longitude'].to_list()
    print(latitudes,"latitudes")
    
    dynamic_latitudes,dynamic_longitudes = get_dynamic_data()


    address_col = df['address']
    result_df = pd.DataFrame(columns=['address','location','AWB','names','product_id'])
    lat = []
    lng = []
    bad_data = []
    good_data = [] #ADD
    count = 0
    print(len(df['address'].to_list()) , len(latitudes))
    for i in df.index:
        #print(df['address'][i])
        coordinates = [latitudes[i-1],longitudes[i-1]]

        lat.append(coordinates[0])
        lng.append(coordinates[1])
        result_df = result_df.append(df.loc[i], ignore_index=True)
        good_data.append(i)
        


    for i in bad_data:
        df.drop(i, inplace=True)
    series1 = pd.Series(lat)
    series2 = pd.Series(lng)

    result = pd.concat([series1, series2], axis=1)
    df = pd.DataFrame(result)
    result.columns = ['latitude', 'longitude']
    print(result)
    print(result_df)
    return result,result_df


def geocodingBing(data):
    lat, lng = None, None
    api_key = 'enter bing geocoding'
    # Specify the address
    address = data

    # Build the URL for the API request
    url = f'http://dev.virtualearth.net/REST/v1/Locations?q={address}&key={api_key}'

    # Get the latitude and longitude from the response
    

    r =  requests.get(url)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        
        lat = r.json()['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
        lng = r.json()['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
    except:
        pass
    return lat, lng





@app.route('/getdriveriddetails',methods=['GET','POST'])
def getdriveriddetails():
    driverdata = getdriverid()
    return jsonify({'driverdata': driverdata})

@app.route('/postroutedetails',methods=['GET','POST'])
def postroutedetails():
    data = request.get_json()
    time = data["time"]
    DriverName = data["DriverName"]
    DriverPhone = data["DriverPhone"]
    source_coordinates = data["source_coordinates"]
    dest_corrdinates = data["dest_corrdinates"]

    add_route_data(time,DriverName,DriverPhone,source_coordinates,dest_corrdinates)
    return jsonify({'message': 'Data received'})

@app.route('/getdriverdetails',methods=['GET','POST'])
def getdriverdetails():
    number = request.get_json()
    driverdata = getdriver(str(number))
    print(driverdata)
    return jsonify({'driverdata': driverdata})

@app.route('/getvolumedetails',methods=['GET','POST'])
def getvolumedetails():
    volumedata = getvolume()
    return jsonify({'driverdata': volumedata})


@app.route('/nextroute',methods=['GET','POST'])
def nextroute():
    number = request.get_json()
    print(number)
    cvrptw_next(int(number))
    return jsonify({'driverdata': "driverdata"})

@app.route('/dynamicpickup',methods=['GET','POST'])
def dynamicpickup():
    data = request.get_json()
    address = data["address"]
    volume = data["volume"]
    dynamic_latitudes,dynamic_longitudes = get_dynamic_data()
    print("dynamic ",dynamic_latitudes)
    pickups_data = [[address, '900',900,'orderid','900',dynamic_latitudes[0],dynamic_longitudes[0]]]
    dynamic_pick_up(pickups_data)
    dynamic_pickup(capacity)
    return jsonify({'driverdata': "driverdata"})

@app.route('/getroutedetails',methods=['GET','POST'])
def getroutedetails():
    number = request.get_json()
    routedata = getroute(str(number))
    return jsonify({'driverdata': routedata})


@app.route('/csvinput', methods=['POST'])
def endpoint():
    global latitudes
    global longitudes
    global dynamic_latitudes
    global dynamic_longitudes
    
    data = request.get_json()
    deliverydata = data["item1"]
    driverdata = data["item2"]
    dimension = data["item3"]

   
    driverdf = pd.DataFrame(driverdata)
    driverdf.columns = driverdf.iloc[0]
    driverdf = driverdf[1:]
    driverdf.to_csv("driverdata.csv",index=False)
    for i in driverdf.index:
        print(driverdf['driver_id'][i],driverdf['driver_name'][i])
        add_driver_Id(driverdf['driver_id'][i],driverdf['driver_name'][i])

    dimensiondf = pd.DataFrame(dimension)
    dimensiondf.columns = dimensiondf.iloc[0]
    dimensiondf = dimensiondf[1:]
    dimensiondf.to_csv("dimensiondata.csv",index=False)
    count = 0
    for i in dimensiondf.index:
        add_volume_info(dimensiondf['product_id'][i],dimensiondf['volume'][i])
        count +=1
        if count ==20:
            break
    deliverydf = pd.DataFrame(deliverydata)
    deliverydf.columns = deliverydf.iloc[0]
    deliverydf = deliverydf[1:]
  
    
    # remove null values and check if each row is having a non nullvalue in both the columns of latitude and longitiude
    address_df,good_data = get_lng_lat(deliverydf)
    print("address df",address_df)

    address_df['longlat'] = address_df[['longitude','latitude']].astype(str).agg(','.join, axis=1)
    make_distance_matrix(address_df)
    Each_route = first_call()
    print(Each_route)
    count  = 1
    for route in Each_route:
        if len(route) > 1:
            addr = []
            productId = []
            locations = []
            longitude = []
            latitude = []
            for i in route:
                if i!=0:
                    addr.append(good_data['address'][i])
                    productId.append(good_data['product_id'][i])
                    locations.append(address_df['longlat'][i])
                    longitude.append(str(address_df['longitude'][i]))
                    latitude.append(str(address_df['latitude'][i]))

            driverid = driverdf['driver_id'][count]
            drivername = driverdf['driver_name'][count]
            count = count + 1
            add_driver_data(productId,addr,locations,driverid,drivername)
            driver_schema(productId,addr,latitude,longitude,driverid)

    updation_after_first(latitudes,longitudes)
    return jsonify({'message': 'Data received'})



if __name__ == '__main__':
    app.run(debug=True)
    




    ###### BING API CALL FOR LAT LONG OF ADDRESS ######

    
    #array = []
    #coordinates = []
    # for key in data:
    #     array.append(str(key))
        
    # for i in array:
    #   i = i[2:len(i)-2]
    #   clean_data.append(str(i))
    #   lat, long = geocodingBing(str(i))
    #   #coordinates.append([lat, long])
    #   print(lat,long)
   