import React from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import "primereact/resources/themes/lara-light-indigo/theme.css";
import "primereact/resources/primereact.min.css";
import RouteButton from "../Utils/routeButton";


const AllProducts = (props) => {
  const productIDBodyTemplate = (rowData) => {
    return (
      <div>
        <span className="fw-bold" style={{ fontSize: "1.2em" }}>
          {rowData.productID}
        </span>
      </div>
    );
  };


  return (
    <div style={{ width: "100%" }}>
      {console.log("all product", props.data[0])}
      
      {props.data && (
        <DataTable
          value={props.data[0].productID.map((val1, index) => ({
                orderno: index,
                productID: val1,
                Address: props.data[0].Address[index],
                }))}
          paginator
          rows={5}
          rowsPerPageOptions={[1, 10, 25, 50, 100]}
          totalRecords={100}
        >
          <Column field="orderno" header="OrderNo" sortable></Column>
          
          <Column
            field="productID"
            header="productID"
            sortable
            body={productIDBodyTemplate}
          ></Column>
          <Column field="Address" header="Address" sortable></Column>
        </DataTable>
      )}
    </div>
  );
};

export default AllProducts;
