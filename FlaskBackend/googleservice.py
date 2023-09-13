
# Importing required library
import pygsheets
import time
import pandas as pd
# Create the Client
# Enter the name of the downloaded KEYS
# file in service_account_file
client = pygsheets.authorize(service_account_file="organic-totem-376807-56b420de6bd5.json")
sh = client.open(client.spreadsheet_titles()[0])
wk1 = sh.sheet1
# wk2 = sh.sheet2
wk=sh.worksheets()
wk2 = wk[1]
# deliverydf = pd.read_csv("bangalore_dispatch_data.csv") 

# Sample command to verify successful
# authorization of pygsheets
# Prints the names of the spreadsheet
# shared with or owned by the service
# account


def get_full_data():
    df = pd.DataFrame(wk1.get_all_records())
    while 1:
        if df['Latitude'].to_list()[len(df['address'].to_list())-1] == "":
            time.sleep(10)
            df = pd.DataFrame(wk1.get_all_records())
        else:
            break
    return df
     
     
def get_dynamic_data():
    df = pd.DataFrame(wk2.get_all_records())
    return df['Latitude'].to_list(),df['Longitude'].to_list()
    

def update_sheet(deliverydf):
    wk1.set_dataframe(deliverydf, 'A1')
    
# update_sheet()
print(get_dynamic_data())
