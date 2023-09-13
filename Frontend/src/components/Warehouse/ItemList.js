import React from 'react';
import Table from 'react-bootstrap/Table';
import { TiTick } from "react-icons/ti";
import {FcCancel} from "react-icons/fc"


const ItemList = ({ items ,query}) => {
  return (
    <Table striped bordered hover className="table styled-table">
      <thead>
        <tr>
            <th>Flag</th>
          <th>Product Id</th>
          <th>Volume</th>
        </tr>
      </thead>
      <tbody>
        {items.filter(item => {
            if(!query)return item
            return item.productID == (query)
        }
        ).map((item, index) => (
          <tr key={index}>
            <td style={{color: "green"}}>{true===true?<TiTick/>:<FcCancel/>}</td>
            {/* <td>{item.name}</td> */}
            <td>{item.productID}</td>
            <td>{item.volume}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default ItemList;
