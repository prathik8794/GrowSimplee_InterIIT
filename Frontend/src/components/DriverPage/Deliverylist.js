import React from 'react';
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import "primereact/resources/themes/lara-light-indigo/theme.css"
import "primereact/resources/primereact.min.css"
import RouteButton from '../Utils/routeButton';


import { useState, useEffect } from "react";
import { FilterMatchMode} from "primereact/api"
import { inputText } from "primereact/inputtext"

const Deliverylist = (props) => {
  
  const driverBodyTemplate = (rowData) => {
    return <div>
      <RouteButton className="btn btn-primary align-middle" special={`/driver/${rowData.driverid}`}>
                    <span className="btn " >
                        <span className="fw-bold" style={{fontSize:"1.2em"}} >{rowData.driverid}</span>
                        </span>
                    </RouteButton>
    </div>;
    } 

    const indexBodyTemplate = (rowData, column) =>{
      return column.rowIndex + 1 + ""
    }

  return (
    <div>
      {props.data && 
      <DataTable 
            value={props.data} 
            paginator
            rows={10}
            rowsPerPageOptions={[1,10,25,50,100]}
            totalRecords={100}
            style = {{padding:"1%"}}
        >
            <Column field="driverid" header="S.no" sortable body={indexBodyTemplate }></Column>

            <Column field="driverid" header="ID" sortable body={driverBodyTemplate }></Column>
             <Column field="drivername" header="Name" sortable></Column>
        </DataTable>
      }
        
    </div>
  );
}

export default Deliverylist;
