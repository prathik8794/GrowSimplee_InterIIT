import DriverDetails from "../DriverPage/DriverDetails";
import React from "react";
import MapAPI from "../API/Map/MapAPI";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.min.css";
// import "./photu.png"

import { useState } from "react";
import { FilterMatchMode } from "primereact/api";
import { inputText } from "primereact/inputtext";

const Admin = () => {
  const data = [
    {
      id: 1,
      name: "haha1",
      phone: "haha11",
      photo: "photu.png",
    },
    {
      id: 2,
      name: "haha2",
      phone: "haha12",
      photo: "photu.png",
    },
    {
      id: 3,
      name: "haha3",
      phone: "haha13",
      photo: "photu",
    },
    {
      id: 4,
      name: "haha4",
      phone: "haha14",
      photo: "photu.png",
    },
  ];

  return (
    <>
      <div className="row gx-2 m-0 mt-1">
        {/* <div className="col">
                    <DataTable 
                        value={data} responsiveLayout="scroll"
                    >
                        <Column field="id" header="ID" sortable/>
                        <Column field="name" header="Name" sortable/>
                        <Column field="phone" header="Phone" sortable/>
                    </DataTable>
                </div> */}
        <div className="col-6">
          <DataTable
            value={data}
            paginator
            rows={2}
            rowsPerPageOptions={[1, 10, 25, 50, 100]}
            totalRecords={3}
          >
            <Column field="id" header="ID" sortable />
            <Column field="name" header="Name" sortable />
            <Column field="phone" header="Phone" sortable />
            <Column body={`<img src="photu.png">`} />
          </DataTable>
          {/* <div className="card mb-3">
            <div className="row g-0">
              <div className="col-md-4">
                <img src="..." className="img-fluid rounded-start" alt="..."></img>
              </div>
              <div className="col-md-8">
                <div className="card-body">
                  <h5 className="card-title">Card title</h5>
                  <p className="card-text">
                    This is a wider card with supporting text below as a natural
                    lead-in to additional content. This content is a little bit
                    longer.
                  </p>
                  <p className="card-text">
                    <small className="text-muted">Last updated 3 mins ago</small>
                  </p>
                </div>
              </div>
            </div>
            </div> */}
        </div>
        <div className="col-6">
          <MapAPI />
        </div>
      </div>
    </>
  );
};

export default Admin;
